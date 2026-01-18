"""OSC client wrapper for AbletonOSC.

Provides a Pythonic interface to control Ableton Live via OSC.
"""

from osc_client.application import Application
from osc_client.client import AbletonOSCClient
from osc_client.clip import Clip
from osc_client.clip_slot import ClipSlot
from osc_client.device import Device
from osc_client.scene import Scene
from osc_client.song import Song
from osc_client.track import Track
from osc_client.view import View

__all__ = [
    "AbletonOSCClient",
    "Application",
    "Clip",
    "ClipSlot",
    "Device",
    "Scene",
    "Song",
    "Track",
    "View",
    "connect",
]


def connect(
    host: str = "127.0.0.1",
    send_port: int = 11000,
    receive_port: int = 11001,
) -> AbletonOSCClient:
    """Create and return an AbletonOSC client.

    Convenience function to create a client with default settings.

    Args:
        host: Ableton host address (default: localhost)
        send_port: Port to send OSC messages (default: 11000)
        receive_port: Port to receive OSC responses (default: 11001)

    Returns:
        Connected AbletonOSCClient instance
    """
    return AbletonOSCClient(host, send_port, receive_port)
