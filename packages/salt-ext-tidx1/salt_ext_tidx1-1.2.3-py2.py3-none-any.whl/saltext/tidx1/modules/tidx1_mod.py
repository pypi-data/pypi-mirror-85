"""
Salt execution module
"""
import logging

log = logging.getLogger(__name__)

__virtualname__ = "tidx1"


def __virtual__():
    # To force a module not to load return something like:
    #   return (False, "The tidx1 execution module is not implemented yet")
    return __virtualname__
