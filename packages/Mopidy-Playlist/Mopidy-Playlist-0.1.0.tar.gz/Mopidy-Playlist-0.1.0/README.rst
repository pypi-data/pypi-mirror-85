****************************
Mopidy-Playlist
****************************

.. image:: https://img.shields.io/pypi/v/Mopidy-Playlist
    :target: https://pypi.org/project/Mopidy-Playlist/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/circleci/build/gh/peterlisak/mopidy-playlist
    :target: https://circleci.com/gh/peterlisak/mopidy-playlist
    :alt: CircleCI build status

.. image:: https://img.shields.io/codecov/c/gh/peterlisak/mopidy-playlist
    :target: https://codecov.io/gh/peterlisak/mopidy-playlist
    :alt: Test coverage

Mopidy extension for remote playlist expansion. Extension uses Mopidy's built-in
playlist parsers to extract tracks from a remote playlist. Unlike Mopify-Stream,
Mopidy-Playlist extract and add all tracks into playback queue.


Installation
============

Install by running::

    python3 -m pip install Mopidy-Playlist

See https://mopidy.com/ext/playlist/ for alternative installation methods.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-Playlist to your Mopidy configuration file::

    [playlist]
    enabled = true
    timeout = 1000
    max_lookups = 100


Project resources
=================

- `Source code <https://github.com/peterlisak/mopidy-playlist>`_
- `Issue tracker <https://github.com/peterlisak/mopidy-playlist/issues>`_
- `Changelog <https://github.com/peterlisak/mopidy-playlist/blob/master/CHANGELOG.rst>`_


Credits
=======

- Original author: `Peter Lisák <https://github.com/peterlisak>`__
- Current maintainer: `Peter Lisák <https://github.com/peterlisak>`__
- `Contributors <https://github.com/peterlisak/mopidy-playlist/graphs/contributors>`_
