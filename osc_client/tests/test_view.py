"""Tests for View operations."""


def test_get_selected_track(view):
    """Test getting selected track."""
    track = view.get_selected_track()
    assert isinstance(track, int)
    assert track >= 0


def test_set_selected_track(view, song):
    """Test setting selected track."""
    original = view.get_selected_track()
    num_tracks = song.get_num_tracks()

    try:
        # Select first track
        view.set_selected_track(0)
        assert view.get_selected_track() == 0

        # Select another track if available
        if num_tracks > 1:
            view.set_selected_track(1)
            assert view.get_selected_track() == 1
    finally:
        view.set_selected_track(original)


def test_get_selected_scene(view):
    """Test getting selected scene."""
    scene = view.get_selected_scene()
    assert isinstance(scene, int)
    assert scene >= 0


def test_set_selected_scene(view, song):
    """Test setting selected scene."""
    original = view.get_selected_scene()
    num_scenes = song.get_num_scenes()

    try:
        # Select first scene
        view.set_selected_scene(0)
        assert view.get_selected_scene() == 0

        # Select another scene if available
        if num_scenes > 1:
            view.set_selected_scene(1)
            assert view.get_selected_scene() == 1
    finally:
        view.set_selected_scene(original)
