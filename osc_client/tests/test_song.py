"""Tests for Song operations."""


def test_get_tempo(song):
    """Test getting current tempo."""
    tempo = song.get_tempo()
    assert 20 <= tempo <= 999  # Valid BPM range


def test_set_tempo(song):
    """Test setting tempo."""
    original = song.get_tempo()
    try:
        song.set_tempo(120.0)
        assert song.get_tempo() == 120.0

        song.set_tempo(140.5)
        assert song.get_tempo() == 140.5
    finally:
        song.set_tempo(original)  # Restore


def test_get_is_playing(song):
    """Test getting play state."""
    is_playing = song.get_is_playing()
    assert isinstance(is_playing, bool)


def test_start_stop_playing(song):
    """Test transport controls."""
    original_playing = song.get_is_playing()
    try:
        song.stop_playing()
        assert song.get_is_playing() is False

        song.start_playing()
        assert song.get_is_playing() is True

        song.stop_playing()
        assert song.get_is_playing() is False
    finally:
        if original_playing:
            song.start_playing()
        else:
            song.stop_playing()


def test_get_num_tracks(song):
    """Test getting track count."""
    num_tracks = song.get_num_tracks()
    assert num_tracks >= 1  # Always at least one track


def test_get_num_scenes(song):
    """Test getting scene count."""
    num_scenes = song.get_num_scenes()
    assert num_scenes >= 1  # Always at least one scene


def test_get_signature(song):
    """Test getting time signature."""
    numerator = song.get_signature_numerator()
    denominator = song.get_signature_denominator()

    assert 1 <= numerator <= 99
    assert denominator in [1, 2, 4, 8, 16]  # Powers of 2


def test_set_signature(song):
    """Test setting time signature."""
    original_num = song.get_signature_numerator()
    original_denom = song.get_signature_denominator()
    try:
        song.set_signature_numerator(3)
        song.set_signature_denominator(4)

        assert song.get_signature_numerator() == 3
        assert song.get_signature_denominator() == 4
    finally:
        song.set_signature_numerator(original_num)
        song.set_signature_denominator(original_denom)


def test_get_metronome(song):
    """Test getting metronome state."""
    metronome = song.get_metronome()
    assert isinstance(metronome, bool)


def test_set_metronome(song):
    """Test toggling metronome."""
    original = song.get_metronome()
    try:
        song.set_metronome(True)
        assert song.get_metronome() is True

        song.set_metronome(False)
        assert song.get_metronome() is False
    finally:
        song.set_metronome(original)


def test_get_current_song_time(song):
    """Test getting playback position."""
    position = song.get_current_song_time()
    assert isinstance(position, float)
    assert position >= 0
