from __future__ import absolute_import
import string

from ..compat import choice


def rndstr(size=16):
    """
    Returns a string of random ascii characters or digits
    :param size: The length of the string
    :return: string
    """
    _basech = string.ascii_letters + string.digits
    return "".join([choice(_basech) for _ in range(size)])