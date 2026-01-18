"""Tests for Scene operations."""


def test_get_name(scene):
    """Test getting scene name."""
    name = scene.get_name(0)
    assert isinstance(name, str)


def test_set_name(scene):
    """Test setting scene name."""
    original = scene.get_name(0)
    try:
        scene.set_name(0, "Test Scene")
        assert scene.get_name(0) == "Test Scene"
    finally:
        scene.set_name(0, original)


def test_get_color(scene):
    """Test getting scene color."""
    color = scene.get_color(0)
    assert isinstance(color, int)


def test_get_is_triggered(scene):
    """Test checking if scene is triggered."""
    is_triggered = scene.get_is_triggered(0)
    assert isinstance(is_triggered, bool)
