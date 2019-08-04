"""
===========
fs.datalake
===========

PythonFileSystem extension for Azure Datalake Store
"""

import logging

import pkg_resources

from .filesystem import DatalakeFS

# Custom logger
LOG = logging.getLogger(name=__name__)

# PEP 396 style version marker
try:
    __version__ = pkg_resources.get_distribution('fs.datalake').version
except pkg_resources.DistributionNotFound:
    LOG.warning("Could not get the package version from pkg_resources")
    __version__ = 'unknown'

__author__ = "Gilles Lenfant"
__author_email__ = "gilles.lenfant@gmail.com"
__license__ = "MIT"
