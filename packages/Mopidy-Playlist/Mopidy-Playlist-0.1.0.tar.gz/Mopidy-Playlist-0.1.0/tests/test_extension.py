from mopidy.ext import Registry

from mopidy_playlist import Extension
from mopidy_playlist import backend as backend_lib


def test_get_default_config():
    ext = Extension()

    config = ext.get_default_config()

    assert "[playlist]" in config
    assert "enabled = true" in config
    assert "timeout = 1000" in config
    assert "max_lookups = 100" in config


def test_get_config_schema():
    ext = Extension()

    schema = ext.get_config_schema()

    assert "enabled" in schema
    assert "timeout" in schema
    assert "max_lookups" in schema


def test_setup():
    ext = Extension()
    registry = Registry()
    ext.setup(registry)
    assert backend_lib.PlaylistBackend in registry["backend"]
