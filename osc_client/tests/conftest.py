"""Pytest configuration and fixtures for OSC client tests.

These are integration tests that require a running Ableton Live instance
with AbletonOSC enabled.
"""

import pytest

from osc_client.client import AbletonOSCClient


# Global to track if we've already checked for Ableton
_ableton_available = None


@pytest.fixture(scope="session")
def client():
    """Provide a connected AbletonOSC client.

    Skips the test if Ableton is not running or AbletonOSC is not responding.
    Session-scoped to avoid port binding issues.
    """
    global _ableton_available

    c = AbletonOSCClient()
    try:
        c.query("/live/test", timeout=1.0)
        _ableton_available = True
    except TimeoutError:
        c.close()
        _ableton_available = False
        pytest.skip("Ableton not running or AbletonOSC not enabled")

    yield c
    c.close()


@pytest.fixture(scope="session")
def song(client):
    """Provide a Song instance."""
    from osc_client.song import Song

    return Song(client)


@pytest.fixture(scope="session")
def track(client):
    """Provide a Track instance."""
    from osc_client.track import Track

    return Track(client)


@pytest.fixture(scope="session")
def clip(client):
    """Provide a Clip instance."""
    from osc_client.clip import Clip

    return Clip(client)


@pytest.fixture(scope="session")
def clip_slot(client):
    """Provide a ClipSlot instance."""
    from osc_client.clip_slot import ClipSlot

    return ClipSlot(client)


@pytest.fixture(scope="session")
def device(client):
    """Provide a Device instance."""
    from osc_client.device import Device

    return Device(client)


@pytest.fixture(scope="session")
def scene(client):
    """Provide a Scene instance."""
    from osc_client.scene import Scene

    return Scene(client)


@pytest.fixture(scope="session")
def view(client):
    """Provide a View instance."""
    from osc_client.view import View

    return View(client)


@pytest.fixture(scope="session")
def application(client):
    """Provide an Application instance."""
    from osc_client.application import Application

    return Application(client)
