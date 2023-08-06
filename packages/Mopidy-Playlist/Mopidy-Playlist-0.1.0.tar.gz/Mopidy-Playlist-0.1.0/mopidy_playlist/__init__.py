import logging
import pathlib

import pkg_resources
from mopidy import config, ext

__version__ = pkg_resources.get_distribution("Mopidy-Playlist").version

logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = "Mopidy-Playlist"
    ext_name = "playlist"
    version = __version__

    def get_default_config(self):
        return config.read(pathlib.Path(__file__).parent / "ext.conf")

    def get_config_schema(self):
        schema = super().get_config_schema()
        schema["timeout"] = config.Integer(minimum=100, maximum=10000)
        schema["max_lookups"] = config.Integer(minimum=1, maximum=1000)
        return schema

    def setup(self, registry):
        from .backend import PlaylistBackend

        registry.add("backend", PlaylistBackend)
