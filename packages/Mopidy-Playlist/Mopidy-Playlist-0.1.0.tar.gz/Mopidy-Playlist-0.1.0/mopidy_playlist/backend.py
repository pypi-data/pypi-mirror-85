import logging
import os
import urllib.parse

import pykka
from mopidy import backend, exceptions
from mopidy.audio import scan, tags
from mopidy.internal import http, playlists

import mopidy_playlist

logger = logging.getLogger(__name__)


class PlaylistBackend(pykka.ThreadingActor, backend.Backend):
    def __init__(self, config, audio):
        super(PlaylistBackend, self).__init__()
        self.scanner = scan.Scanner(
            timeout=config["playlist"]["timeout"], proxy_config=config["proxy"]
        )
        self.session = http.get_requests_session(
            proxy_config=config["proxy"],
            user_agent=(
                f"{mopidy_playlist.Extension.dist_name}/"
                f"{mopidy_playlist.Extension.version}"
            ),
        )
        self.timeout = config["playlist"]["timeout"]
        self.max_lookups = config["playlist"]["max_lookups"]
        self.library = PlaylistLibraryProvider(backend=self)
        self.uri_schemes = {"playlist", "pl"}


class PlaylistLibraryProvider(backend.LibraryProvider):
    def _parse_playlist(self, uri):
        """Fetch and parse playlist from uri."""
        content = http.download(
            self.backend.session, uri, timeout=self.backend.timeout / 1000
        )

        if content is None:
            logger.warning(
                "Error downloading URI %s while unwrapping playlist",
                uri,
            )
            return []

        uris = playlists.parse(content)
        if not uris:
            logger.warning("Failed playlist from URI %s.", uri)
            return []

        return uris

    def _scan_track(self, uri):
        """Identify playable tracks."""
        try:
            scan_result = self.backend.scanner.scan(
                uri, timeout=self.backend.timeout
            )
        except exceptions.ScannerError as exc:
            logger.warning(
                "GStreamer failed scanning URI (%s): %s %s",
                uri,
                exc,
                self.backend.timeout,
            )
            return

        has_interesting_mime = (
            scan_result.mime is not None
            and not scan_result.mime.startswith("text/")
            and not scan_result.mime.startswith("application/")
        )
        if scan_result.playable or has_interesting_mime:
            logger.debug(
                "Unwrapped potential %s stream: %s",
                scan_result.mime,
                uri,
            )
            name = os.path.basename(urllib.parse.urlparse(uri).path)
            track = tags.convert_tags_to_track(scan_result.tags).replace(
                uri=uri, length=scan_result.duration
            )
            if not track.name:
                track = track.replace(name=name)

            return track
        else:
            logger.warning(
                "Unwrapped potential %s non-playable stream: %s",
                scan_result.mime,
                uri,
            )
        return

    def lookup(self, uri):
        logger.info("Looking up playlist %s", uri)
        if uri.startswith("pl:"):
            playlist_url = uri[3:]
        elif uri.startswith("playlist:"):
            playlist_url = uri[9:]
        else:
            playlist_url = uri

        uris = self._parse_playlist(playlist_url)

        tracks = []
        # Limit max inspected/scanned items in playlist.
        for u in uris[: self.backend.max_lookups]:
            # TODO skip already inspected/scanned items
            # TODO parse inner playlists recursively
            logger.debug("Found new URI %s in parsed playlist %s", u, uri)
            u = urllib.parse.urljoin(playlist_url, u)
            track = self._scan_track(u)
            if track:
                tracks.append(track)

        return tracks
