"""Tests for Song operations."""

import time

SETTLE_TIME = 0.1  # Time for Ableton to process changes


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
        time.sleep(SETTLE_TIME)
        assert song.get_is_playing() is False

        song.start_playing()
        time.sleep(SETTLE_TIME)
        assert song.get_is_playing() is True

        song.stop_playing()
        time.sleep(SETTLE_TIME)
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


def test_create_and_delete_midi_track(song):
    """Test creating and deleting a MIDI track."""
    original_count = song.get_num_tracks()

    # Create MIDI track at end
    song.create_midi_track(-1)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count + 1

    # Delete the new track
    song.delete_track(original_count)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count


def test_create_and_delete_audio_track(song):
    """Test creating and deleting an audio track."""
    original_count = song.get_num_tracks()

    # Create audio track at end
    song.create_audio_track(-1)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count + 1

    # Delete the new track
    song.delete_track(original_count)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count


def test_duplicate_track(song):
    """Test duplicating a track."""
    original_count = song.get_num_tracks()

    # Duplicate track 0
    song.duplicate_track(0)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count + 1

    # Delete the duplicate (it appears at index 1)
    song.delete_track(1)
    time.sleep(SETTLE_TIME)
    assert song.get_num_tracks() == original_count


def test_get_groove_amount(song):
    """Test getting groove amount."""
    groove = song.get_groove_amount()
    assert 0.0 <= groove <= 1.0


def test_set_groove_amount(song):
    """Test setting groove amount."""
    original = song.get_groove_amount()
    try:
        song.set_groove_amount(0.5)
        time.sleep(SETTLE_TIME)
        assert abs(song.get_groove_amount() - 0.5) < 0.01

        song.set_groove_amount(0.0)
        time.sleep(SETTLE_TIME)
        assert abs(song.get_groove_amount()) < 0.01
    finally:
        song.set_groove_amount(original)


def test_can_undo_redo(song):
    """Test undo/redo availability checks."""
    can_undo = song.can_undo()
    can_redo = song.can_redo()

    # These return bools regardless of state
    assert isinstance(can_undo, bool)
    assert isinstance(can_redo, bool)


def test_undo_redo(song):
    """Test undo and redo functionality."""
    # Make a change we can undo
    original_tempo = song.get_tempo()
    new_tempo = 130.0 if original_tempo != 130.0 else 125.0

    song.set_tempo(new_tempo)
    time.sleep(SETTLE_TIME)
    assert song.get_tempo() == new_tempo

    # Undo should revert
    if song.can_undo():
        song.undo()
        time.sleep(SETTLE_TIME)
        # Tempo should be back to original
        assert song.get_tempo() == original_tempo

        # Redo should reapply
        if song.can_redo():
            song.redo()
            time.sleep(SETTLE_TIME)
            assert song.get_tempo() == new_tempo

            # Clean up - undo back to original
            song.undo()
            time.sleep(SETTLE_TIME)


def test_stop_all_clips(song):
    """Test stopping all clips."""
    # Just verify the method executes without error
    # We can't easily verify clips stopped without playing one first
    song.stop_all_clips()


def test_capture_midi(song):
    """Test MIDI capture (just verify no error)."""
    # capture_midi requires recently played MIDI, so we just
    # verify it doesn't raise an exception
    song.capture_midi()


# Scene management tests


def test_create_and_delete_scene(song):
    """Test creating and deleting a scene."""
    original_count = song.get_num_scenes()

    # Create scene at end
    song.create_scene(-1)
    time.sleep(SETTLE_TIME)
    assert song.get_num_scenes() == original_count + 1

    # Delete the new scene
    song.delete_scene(original_count)
    time.sleep(SETTLE_TIME)
    assert song.get_num_scenes() == original_count


def test_duplicate_scene(song):
    """Test duplicating a scene."""
    original_count = song.get_num_scenes()

    # Duplicate scene 0
    song.duplicate_scene(0)
    time.sleep(SETTLE_TIME)
    assert song.get_num_scenes() == original_count + 1

    # Delete the duplicate (it appears at index 1)
    song.delete_scene(1)
    time.sleep(SETTLE_TIME)
    assert song.get_num_scenes() == original_count


def test_get_song_length(song):
    """Test getting song length."""
    length = song.get_song_length()
    assert isinstance(length, float)
    assert length >= 0


# Loop control tests


def test_get_loop(song):
    """Test getting loop state."""
    loop = song.get_loop()
    assert isinstance(loop, bool)


def test_set_loop(song):
    """Test setting loop state."""
    original = song.get_loop()
    try:
        song.set_loop(True)
        time.sleep(SETTLE_TIME)
        assert song.get_loop() is True

        song.set_loop(False)
        time.sleep(SETTLE_TIME)
        assert song.get_loop() is False
    finally:
        song.set_loop(original)


def test_get_loop_start(song):
    """Test getting loop start."""
    start = song.get_loop_start()
    assert isinstance(start, float)
    assert start >= 0


def test_set_loop_start(song):
    """Test setting loop start."""
    original = song.get_loop_start()
    try:
        song.set_loop_start(4.0)
        time.sleep(SETTLE_TIME)
        assert abs(song.get_loop_start() - 4.0) < 0.01
    finally:
        song.set_loop_start(original)


def test_get_loop_length(song):
    """Test getting loop length."""
    length = song.get_loop_length()
    assert isinstance(length, float)
    assert length > 0


def test_set_loop_length(song):
    """Test setting loop length."""
    original = song.get_loop_length()
    try:
        song.set_loop_length(8.0)
        time.sleep(SETTLE_TIME)
        assert abs(song.get_loop_length() - 8.0) < 0.01
    finally:
        song.set_loop_length(original)


# Quantization tests


def test_get_midi_recording_quantization(song):
    """Test getting MIDI recording quantization."""
    quant = song.get_midi_recording_quantization()
    assert isinstance(quant, int)
    assert 0 <= quant <= 8


def test_set_midi_recording_quantization(song):
    """Test setting MIDI recording quantization."""
    original = song.get_midi_recording_quantization()
    try:
        song.set_midi_recording_quantization(2)  # 1/8
        time.sleep(SETTLE_TIME)
        assert song.get_midi_recording_quantization() == 2
    finally:
        song.set_midi_recording_quantization(original)


def test_get_clip_trigger_quantization(song):
    """Test getting clip trigger quantization."""
    quant = song.get_clip_trigger_quantization()
    assert isinstance(quant, int)
    assert 0 <= quant <= 13


def test_set_clip_trigger_quantization(song):
    """Test setting clip trigger quantization."""
    original = song.get_clip_trigger_quantization()
    try:
        song.set_clip_trigger_quantization(4)  # 1 bar
        time.sleep(SETTLE_TIME)
        assert song.get_clip_trigger_quantization() == 4
    finally:
        song.set_clip_trigger_quantization(original)


# Session recording tests


def test_get_session_record(song):
    """Test getting session record state."""
    recording = song.get_session_record()
    assert isinstance(recording, bool)


def test_set_session_record(song):
    """Test setting session record state."""
    original = song.get_session_record()
    try:
        song.set_session_record(False)
        time.sleep(SETTLE_TIME)
        assert song.get_session_record() is False
    finally:
        song.set_session_record(original)


def test_trigger_session_record(song):
    """Test triggering session record (just verify no error)."""
    # Just verify method executes without error
    # Actual recording behavior depends on track state
    song.trigger_session_record()
    time.sleep(SETTLE_TIME)
    # Turn it off to clean up
    song.set_session_record(False)


# Arrangement recording tests


def test_get_arrangement_overdub(song):
    """Test getting arrangement overdub state."""
    overdub = song.get_arrangement_overdub()
    assert isinstance(overdub, bool)


def test_set_arrangement_overdub(song):
    """Test setting arrangement overdub state."""
    original = song.get_arrangement_overdub()
    try:
        song.set_arrangement_overdub(True)
        time.sleep(SETTLE_TIME)
        assert song.get_arrangement_overdub() is True

        song.set_arrangement_overdub(False)
        time.sleep(SETTLE_TIME)
        assert song.get_arrangement_overdub() is False
    finally:
        song.set_arrangement_overdub(original)


# Punch in/out tests


def test_get_punch_in(song):
    """Test getting punch-in state."""
    punch_in = song.get_punch_in()
    assert isinstance(punch_in, bool)


def test_set_punch_in(song):
    """Test setting punch-in state."""
    original = song.get_punch_in()
    try:
        song.set_punch_in(True)
        time.sleep(SETTLE_TIME)
        assert song.get_punch_in() is True

        song.set_punch_in(False)
        time.sleep(SETTLE_TIME)
        assert song.get_punch_in() is False
    finally:
        song.set_punch_in(original)


def test_get_punch_out(song):
    """Test getting punch-out state."""
    punch_out = song.get_punch_out()
    assert isinstance(punch_out, bool)


def test_set_punch_out(song):
    """Test setting punch-out state."""
    original = song.get_punch_out()
    try:
        song.set_punch_out(True)
        time.sleep(SETTLE_TIME)
        assert song.get_punch_out() is True

        song.set_punch_out(False)
        time.sleep(SETTLE_TIME)
        assert song.get_punch_out() is False
    finally:
        song.set_punch_out(original)
