"""Tests for Track operations."""


def test_get_name(track):
    """Test getting track name."""
    name = track.get_name(0)
    assert isinstance(name, str)


def test_set_name(track):
    """Test setting track name."""
    original = track.get_name(0)
    try:
        track.set_name(0, "Test Track")
        assert track.get_name(0) == "Test Track"
    finally:
        track.set_name(0, original)


def test_get_volume(track):
    """Test getting track volume."""
    volume = track.get_volume(0)
    assert 0.0 <= volume <= 1.0


def test_set_volume(track):
    """Test setting track volume."""
    original = track.get_volume(0)
    try:
        track.set_volume(0, 0.5)
        assert abs(track.get_volume(0) - 0.5) < 0.01

        track.set_volume(0, 0.85)  # 0dB
        assert abs(track.get_volume(0) - 0.85) < 0.01
    finally:
        track.set_volume(0, original)


def test_get_panning(track):
    """Test getting track pan."""
    pan = track.get_panning(0)
    assert -1.0 <= pan <= 1.0


def test_set_panning(track):
    """Test setting track pan."""
    original = track.get_panning(0)
    try:
        track.set_panning(0, -0.5)  # Pan left
        assert abs(track.get_panning(0) - (-0.5)) < 0.01

        track.set_panning(0, 0.5)  # Pan right
        assert abs(track.get_panning(0) - 0.5) < 0.01

        track.set_panning(0, 0.0)  # Center
        assert abs(track.get_panning(0)) < 0.01
    finally:
        track.set_panning(0, original)


def test_get_mute(track):
    """Test getting track mute state."""
    muted = track.get_mute(0)
    assert isinstance(muted, bool)


def test_set_mute(track):
    """Test muting/unmuting track."""
    original = track.get_mute(0)
    try:
        track.set_mute(0, True)
        assert track.get_mute(0) is True

        track.set_mute(0, False)
        assert track.get_mute(0) is False
    finally:
        track.set_mute(0, original)


def test_get_solo(track):
    """Test getting track solo state."""
    soloed = track.get_solo(0)
    assert isinstance(soloed, bool)


def test_set_solo(track):
    """Test soloing/unsoloing track."""
    original = track.get_solo(0)
    try:
        track.set_solo(0, True)
        assert track.get_solo(0) is True

        track.set_solo(0, False)
        assert track.get_solo(0) is False
    finally:
        track.set_solo(0, original)


def test_get_arm(track):
    """Test getting track arm state."""
    armed = track.get_arm(0)
    assert isinstance(armed, bool)


def test_get_color(track):
    """Test getting track color."""
    color = track.get_color(0)
    assert isinstance(color, int)


def test_get_num_devices(track):
    """Test getting device count on track."""
    num_devices = track.get_num_devices(0)
    assert num_devices >= 0
