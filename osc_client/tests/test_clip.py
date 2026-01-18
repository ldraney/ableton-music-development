"""Tests for Clip operations.

Uses the test_clip_with_notes fixture which creates a temporary MIDI track
with an audible clip for testing. This ensures tests are self-contained
and don't require manual setup.
"""

import pytest

from osc_client.clip import Note


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


def test_get_name(clip, test_clip_with_notes):
    """Test getting clip name."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    name = clip.get_name(t, s)
    assert isinstance(name, str)


def test_set_name(clip, test_clip_with_notes):
    """Test setting clip name."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    original = clip.get_name(t, s)
    try:
        clip.set_name(t, s, "Test Clip")
        assert clip.get_name(t, s) == "Test Clip"
    finally:
        clip.set_name(t, s, original)


def test_get_length(clip, test_clip_with_notes):
    """Test getting clip length."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    length = clip.get_length(t, s)
    assert length == 4.0  # We created a 4-beat clip


def test_get_is_playing(clip, test_clip_with_notes):
    """Test checking if clip is playing."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    is_playing = clip.get_is_playing(t, s)
    assert isinstance(is_playing, bool)


def test_get_color(clip, test_clip_with_notes):
    """Test getting clip color."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    color = clip.get_color(t, s)
    assert isinstance(color, int)


def test_get_loop_start(clip, test_clip_with_notes):
    """Test getting loop start."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    loop_start = clip.get_loop_start(t, s)
    assert isinstance(loop_start, float)
    assert loop_start >= 0


def test_get_loop_end(clip, test_clip_with_notes):
    """Test getting loop end."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    loop_end = clip.get_loop_end(t, s)
    assert isinstance(loop_end, float)
    assert loop_end > 0


def test_get_notes(clip, test_clip_with_notes):
    """Test getting notes from a clip."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    notes = clip.get_notes(t, s)
    assert len(notes) == 3  # C major chord (C, E, G)
    pitches = [n.pitch for n in notes]
    assert 60 in pitches  # C4
    assert 64 in pitches  # E4
    assert 67 in pitches  # G4


def test_is_midi_clip(clip, test_clip_with_notes):
    """Test checking if clip is a MIDI clip."""
    t, s = test_clip_with_notes["track"], test_clip_with_notes["scene"]
    assert clip.get_is_midi_clip(t, s) is True
    assert clip.get_is_audio_clip(t, s) is False
