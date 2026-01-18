"""Clip operations for AbletonOSC.

Covers /live/clip/* endpoints for individual clip control and note editing.
"""

from typing import NamedTuple

from osc_client.client import AbletonOSCClient


class Note(NamedTuple):
    """Represents a MIDI note in a clip.

    Attributes:
        pitch: MIDI pitch (0-127)
        start_time: Start position in beats
        duration: Duration in beats
        velocity: Velocity (0-127)
        mute: Whether the note is muted
    """

    pitch: int
    start_time: float
    duration: float
    velocity: int
    mute: bool = False


class Clip:
    """Clip operations like notes, properties, and playback."""

    def __init__(self, client: AbletonOSCClient):
        self._client = client

    # Name

    def get_name(self, track_index: int, clip_index: int) -> str:
        """Get the clip name.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Clip name
        """
        result = self._client.query("/live/clip/get/name", track_index, clip_index)
        # Response format: (track_index, clip_index, name)
        return str(result[2]) if len(result) > 2 else ""

    def set_name(self, track_index: int, clip_index: int, name: str) -> None:
        """Set the clip name.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            name: New clip name
        """
        self._client.send("/live/clip/set/name", track_index, clip_index, name)

    # Playback

    def fire(self, track_index: int, clip_index: int) -> None:
        """Fire (launch) a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
        """
        self._client.send("/live/clip/fire", track_index, clip_index)

    def stop(self, track_index: int, clip_index: int) -> None:
        """Stop a clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
        """
        self._client.send("/live/clip/stop", track_index, clip_index)

    # Clip properties

    def get_length(self, track_index: int, clip_index: int) -> float:
        """Get the clip length in beats.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Clip length in beats
        """
        result = self._client.query("/live/clip/get/length", track_index, clip_index)
        # Response format: (track_index, clip_index, length)
        return float(result[2])

    def get_is_midi_clip(self, track_index: int, clip_index: int) -> bool:
        """Check if clip is a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if MIDI clip, False if audio clip
        """
        result = self._client.query(
            "/live/clip/get/is_midi_clip", track_index, clip_index
        )
        # Response format: (track_index, clip_index, is_midi_clip)
        return bool(result[2])

    def get_is_audio_clip(self, track_index: int, clip_index: int) -> bool:
        """Check if clip is an audio clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if audio clip, False if MIDI clip
        """
        result = self._client.query(
            "/live/clip/get/is_audio_clip", track_index, clip_index
        )
        # Response format: (track_index, clip_index, is_audio_clip)
        return bool(result[2])

    def get_is_playing(self, track_index: int, clip_index: int) -> bool:
        """Check if clip is currently playing.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            True if playing
        """
        result = self._client.query(
            "/live/clip/get/is_playing", track_index, clip_index
        )
        # Response format: (track_index, clip_index, is_playing)
        return bool(result[2])

    def get_color(self, track_index: int, clip_index: int) -> int:
        """Get the clip color.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Color as integer
        """
        result = self._client.query("/live/clip/get/color", track_index, clip_index)
        # Response format: (track_index, clip_index, color)
        return int(result[2])

    def set_color(self, track_index: int, clip_index: int, color: int) -> None:
        """Set the clip color.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            color: Color as integer
        """
        self._client.send("/live/clip/set/color", track_index, clip_index, color)

    # Notes (MIDI clips only)

    def get_notes(self, track_index: int, clip_index: int) -> list[Note]:
        """Get all notes from a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            List of Note objects
        """
        result = self._client.query("/live/clip/get/notes", track_index, clip_index)
        notes = []

        # Result format: (track_index, scene_index, pitch, start_time, duration, velocity, mute, ...)
        # Skip first 2 values (indices), then each note is 5 values
        if result and len(result) > 2:
            values = list(result)[2:]  # Skip track_index, scene_index
            for i in range(0, len(values), 5):
                if i + 4 < len(values):
                    notes.append(
                        Note(
                            pitch=int(values[i]),
                            start_time=float(values[i + 1]),
                            duration=float(values[i + 2]),
                            velocity=int(values[i + 3]),
                            mute=bool(values[i + 4]),
                        )
                    )
        return notes

    def add_notes(self, track_index: int, clip_index: int, notes: list[Note]) -> None:
        """Add notes to a MIDI clip.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            notes: List of Note objects to add
        """
        # Build flat list: pitch, start_time, duration, velocity, mute for each note
        args = [track_index, clip_index]
        for note in notes:
            args.extend(
                [note.pitch, note.start_time, note.duration, note.velocity, int(note.mute)]
            )
        self._client.send("/live/clip/add/notes", *args)

    def remove_notes(
        self,
        track_index: int,
        clip_index: int,
        start_time: float = 0.0,
        end_time: float = 128.0,
        pitch_start: int = 0,
        pitch_end: int = 127,
    ) -> None:
        """Remove notes from a MIDI clip within a range.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            start_time: Start of time range in beats
            end_time: End of time range in beats
            pitch_start: Lowest pitch to remove
            pitch_end: Highest pitch to remove
        """
        self._client.send(
            "/live/clip/remove/notes",
            track_index,
            clip_index,
            start_time,
            pitch_start,
            end_time - start_time,  # duration
            pitch_end - pitch_start + 1,  # pitch span
        )

    # Loop settings

    def get_loop_start(self, track_index: int, clip_index: int) -> float:
        """Get the loop start position in beats.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Loop start position in beats
        """
        result = self._client.query(
            "/live/clip/get/loop_start", track_index, clip_index
        )
        # Response format: (track_index, clip_index, loop_start)
        return float(result[2])

    def set_loop_start(
        self, track_index: int, clip_index: int, start: float
    ) -> None:
        """Set the loop start position.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            start: Loop start in beats
        """
        self._client.send(
            "/live/clip/set/loop_start", track_index, clip_index, float(start)
        )

    def get_loop_end(self, track_index: int, clip_index: int) -> float:
        """Get the loop end position in beats.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)

        Returns:
            Loop end position in beats
        """
        result = self._client.query("/live/clip/get/loop_end", track_index, clip_index)
        # Response format: (track_index, clip_index, loop_end)
        return float(result[2])

    def set_loop_end(self, track_index: int, clip_index: int, end: float) -> None:
        """Set the loop end position.

        Args:
            track_index: Track index (0-based)
            clip_index: Clip/scene index (0-based)
            end: Loop end in beats
        """
        self._client.send(
            "/live/clip/set/loop_end", track_index, clip_index, float(end)
        )
