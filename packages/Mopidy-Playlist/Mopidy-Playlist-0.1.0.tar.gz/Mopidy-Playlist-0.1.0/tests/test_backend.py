import logging
from unittest import mock

import pytest
import requests
import responses
from mopidy import exceptions
from mopidy.audio import scan
from mopidy.models import Track

from mopidy_playlist import backend as backend_lib


@pytest.fixture
def config():
    return {
        "proxy": {},
        "playlist": {
            "enabled": True,
            "timeout": 100,
            "max_lookups": 2,
        },
    }


@pytest.fixture
def audio():
    return mock.Mock()


@pytest.yield_fixture
def scanner():
    with mock.patch.object(scan, "Scanner") as patcher:
        yield patcher()


@pytest.fixture
def backend(audio, config, scanner):
    return backend_lib.PlaylistBackend(audio=audio, config=config)


@responses.activate
def test_playlistlibraryprovider_parse_playlist(backend, caplog):
    caplog.set_level(logging.DEBUG)
    playlist_uri = "http://example.com/playlist.m3u"
    playlist_body = """
#EXTM3U
#EXTINF:
http://example.com/track1.mp3
#EXTINF:
http://example.com/track2.mp3
#EXTINF:
http://example.com/track3.mp3
    """.strip()
    responses.add(
        responses.GET,
        playlist_uri,
        body=playlist_body,
        content_type="audio/mpegurl",
    )

    uris = backend.library._parse_playlist(playlist_uri)
    assert uris == [
        "http://example.com/track1.mp3",
        "http://example.com/track2.mp3",
        "http://example.com/track3.mp3",
    ]


@responses.activate
def test_playlistlibraryprovider_parse_playlist_empty(backend, caplog):
    caplog.set_level(logging.DEBUG)
    playlist_uri = "http://example.com/playlist.m3u"
    playlist_body = requests.exceptions.RequestException()
    responses.add(
        responses.GET,
        playlist_uri,
        body=playlist_body,
        content_type="audio/mpegurl",
    )
    uris = backend.library._parse_playlist(playlist_uri)
    assert uris == []
    assert "Error downloading URI" in caplog.text


@responses.activate
def test_playlistlibraryprovider_parse_playlist_empty2(backend, caplog):
    caplog.set_level(logging.DEBUG)
    playlist_uri = "http://example.com/playlist.m3u"
    playlist_body = """#EXTM3U"""
    responses.add(
        responses.GET,
        playlist_uri,
        body=playlist_body,
        content_type="audio/mpegurl",
    )
    uris = backend.library._parse_playlist(playlist_uri)
    assert uris == []
    assert "Failed playlist from URI" in caplog.text


def test_playlistlibraryprovider_scan_track(backend, scanner, caplog):
    caplog.set_level(logging.DEBUG)
    scanner.scan.side_effect = [
        mock.Mock(mime="audio/mpeg", playable=True, tags={}, duration=123),
    ]
    ref = Track(
        length=123, name="track1.mp3", uri="http://example.com/track1.mp3"
    )
    track = backend.library._scan_track("http://example.com/track1.mp3")
    assert track == ref


def test_playlistlibraryprovider_scan_track_error(backend, scanner, caplog):
    caplog.set_level(logging.DEBUG)
    scanner.scan.side_effect = exceptions.ScannerError(message="error")
    track = backend.library._scan_track("http://example.com/track1.mp3")
    assert track is None


def test_playlistlibraryprovider_scan_track_non_playable(
    backend, scanner, caplog
):
    caplog.set_level(logging.DEBUG)
    scanner.scan.side_effect = [
        mock.Mock(mime="text/html", playable=False, tags={}, duration=123),
    ]
    track = backend.library._scan_track("http://example.com/track1.mp3")
    assert track is None


def test_library_lookup(backend, scanner, caplog):
    caplog.set_level(logging.DEBUG)
    backend.library._parse_playlist = mock.Mock()
    backend.library._parse_playlist.return_value = [
        "http://example.com/track1.mp3",
        "http://example.com/track2.mp3",
        "http://example.com/track3.mp3",
    ]
    refs = [
        Track(
            length=123, name="track1.mp3", uri="http://example.com/track1.mp3"
        ),
        Track(
            length=123, name="track2.mp3", uri="http://example.com/track2.mp3"
        ),
    ]
    backend.library._scan_track = mock.Mock()
    backend.library._scan_track.side_effect = refs

    tracks = backend.library.lookup("pl:http://example.com/.m3u")
    assert tracks == refs


def test_library_lookup_urls(backend, scanner, caplog):
    caplog.set_level(logging.DEBUG)
    tracks = backend.library.lookup("pl:http://example.com/.m3u")
    assert tracks == []
    tracks = backend.library.lookup("playlist:http://example.com/.m3u")
    assert tracks == []
    tracks = backend.library.lookup("http://example.com/.m3u")
    assert tracks == []
