
from axon.version import VERSION
from axon.client import Client

__version__ = VERSION

"""Settings."""
write_key = None
device_info = None
on_error = None
debug = False

default_client = None


def track(*args, **kwargs):
    """Send a track call."""
    _proxy('track', *args, **kwargs)


def shutdown():
    """Disconnect from Axon Infrastructure and cleanly shutdown the client."""
    _proxy('disconnect')


def _proxy(method, *args, **kwargs):
    """Create an Axon client if one doesn't exist and send to it."""
    global default_client
    if not default_client:
        default_client = Client(write_key, device_info=device_info, debug=debug,
                                on_error=on_error)

    fn = getattr(default_client, method)
    fn(*args, **kwargs)