import logging
import pykka
import urllib

from mopidy import backend, exceptions
from mopidy.audio import scan, tags
from mopidy.internal import http, playlists
from mopidy.models import Track

import mopidy_playlist

logger = logging.getLogger(__name__)


class PlaylistBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(PlaylistBackend, self).__init__()

        self.scanner = scan.Scanner(
            timeout=config["stream"]["timeout"], proxy_config=config["proxy"]
        )

        self.session = http.get_requests_session(
            proxy_config=config["proxy"],
            user_agent=(
                f"{mopidy_playlist.Extension.dist_name}/{mopidy_playlist.Extension.version}"
            ),
        )
        print(config, config["playlist"]["timeout"], 1000)
        self.timeout = config["playlist"]["timeout"] / 1000

        self.library = PlaylistLibraryProvider(backend=self)

        self.uri_schemes = {"playlist", "pl"}


class PlaylistLibraryProvider(backend.LibraryProvider):
    def lookup(self, uri):
        logger.info("Looking up playlist %s", uri)
        if uri.startswith("pl:"):
            url = uri[3:]
        elif uri.startswith("playlist:"):
            url = uri[9:]

        content = http.download(
            self.backend.session, url, timeout=self.backend.timeout
        )

        if content is None:
            logger.info(
                "Error downloading URI %s while unwrapping playlist",
                uri,
            )
            return None
        uris = playlists.parse(content)
        if not uris:
            logger.warning(
                "Failed playlist from URI %s.",
                uri,
            )
            return [Track(uri=uri)]

        tracks = []
        for u in uris:
            logger.debug("Found new URI %s in parsed playlist %s", u, uri)
            u = urllib.parse.urljoin(url, u)
            try:
                scan_result = self.backend.scanner.scan(u, timeout=self.backend.timeout)
            except exceptions.ScannerError as exc:
                logger.warning("GStreamer failed scanning URI (%s): %s %s", uri, exc, self.backend.timeout)
                scan_result = None

            if scan_result:
                has_interesting_mime = (
                        scan_result.mime is not None
                        and not scan_result.mime.startswith("text/")
                        and not scan_result.mime.startswith("application/")
                )
                if scan_result.playable or has_interesting_mime:
                    logger.debug(
                        "Unwrapped potential %s stream: %s", scan_result.mime, uri
                    )
                    track = tags.convert_tags_to_track(scan_result.tags).replace(
                        uri=u, length=scan_result.duration
                    )
                else:
                    logger.debug(
                        "Unwrapped potential %s inner playlist: %s", scan_result.mime, uri
                    )
                    track = Track(uri=uri)
            else:
                logger.warning("Problem looking up %s", uri)
                track = Track(uri=uri)

            tracks.append(track)

        return tracks
