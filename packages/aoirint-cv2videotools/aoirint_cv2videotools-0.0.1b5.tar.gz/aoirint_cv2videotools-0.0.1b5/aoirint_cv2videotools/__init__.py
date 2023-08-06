from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


import util

from .loader import FileLoader, VideoLoader, YouTubeLoader
from .searcher import YouTubeLiveVideoSearcher, YouTubeVideoEntry
