"""
Compatibility layer and utilities.
"""
import base64
import sys

PY3 = sys.version_info[0] >= 3
PY2 = sys.version_info[0] == 2

if PY3:
    from urllib.parse import unquote

    def iteritems(d):
        return iter(d.items())

    def itervalues(d):
        return iter(d.values())

    def values(d):
        return list(d.values())

    str_types = (str,)
else:
    from urllib import unquote

    def iteritems(d):
        return d.iteritems()

    def itervalues(d):
        return d.itervalues()

    def values(d):
        return d.values()

    str_types = (str, unicode)


def b64encode(bytes_or_str):
    input_bytes = bytes_or_str
    if PY3 and isinstance(bytes_or_str, str):
        input_bytes = bytes_or_str.encode('ascii')

    output_bytes = base64.b64encode(input_bytes)
    if PY3:
        return output_bytes.decode('ascii')
    return output_bytes


# Since SystemRandom is not available on all systems
try:
    # Python 3.6+, designed for this usecase
    from secrets import choice
except ImportError:
    import random
    try:
        # Python 2.4+ if available on the platform
        _sysrand = random.SystemRandom()
        choice = _sysrand.choice
    except AttributeError:
        # Fallback, really bad
        import warnings
        choice = random.choice
        warnings.warn(
            "No good random number generator available on this platform. "
            "Security tokens will be weak and guessable.",
            RuntimeWarning)