"""Tests for Clip operations.

Note: Many tests require an existing clip in track 0, slot 0.
Tests will be skipped if no clip exists.
"""

import pytest

from osc_client.clip import Note


@pytest.fixture
def clip_exists(clip, clip_slot):
    """Check if a clip exists in track 0, slot 0."""
    if not clip_slot.has_clip(0, 0):
        pytest.skip("No clip in track 0, slot 0")
    return True


def test_get_name(clip, clip_exists):
    """Test getting clip name."""
    name = clip.get_name(0, 0)
    assert isinstance(name, str)


def test_set_name(clip, clip_exists):
    """Test setting clip name."""
    original = clip.get_name(0, 0)
    try:
        clip.set_name(0, 0, "Test Clip")
        assert clip.get_name(0, 0) == "Test Clip"
    finally:
        clip.set_name(0, 0, original)


def test_get_length(clip, clip_exists):
    """Test getting clip length."""
    length = clip.get_length(0, 0)
    assert length > 0


def test_get_is_playing(clip, clip_exists):
    """Test checking if clip is playing."""
    is_playing = clip.get_is_playing(0, 0)
    assert isinstance(is_playing, bool)


def test_get_color(clip, clip_exists):
    """Test getting clip color."""
    color = clip.get_color(0, 0)
    assert isinstance(color, int)


def test_note_creation():
    """Test Note namedtuple creation."""
    note = Note(pitch=60, start_time=0.0, duration=0.5, velocity=100)
    assert note.pitch == 60
    assert note.start_time == 0.0
    assert note.duration == 0.5
    assert note.velocity == 100
    assert note.mute is False

    muted_note = Note(pitch=60, start_time=0.0, duration=0.5, velocity=100, mute=True)
    assert muted_note.mute is True


def test_get_loop_start(clip, clip_exists):
    """Test getting loop start."""
    loop_start = clip.get_loop_start(0, 0)
    assert isinstance(loop_start, float)
    assert loop_start >= 0


def test_get_loop_end(clip, clip_exists):
    """Test getting loop end."""
    loop_end = clip.get_loop_end(0, 0)
    assert isinstance(loop_end, float)
    assert loop_end > 0
