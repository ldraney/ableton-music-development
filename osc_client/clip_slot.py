"""Clip slot operations for AbletonOSC.

Covers /live/clip_slot/* endpoints for clip slot management.
"""

from osc_client.client import AbletonOSCClient


class ClipSlot:
    """Clip slot operations like creating/deleting clips and checking status."""

    def __init__(self, client: AbletonOSCClient):
        self._client = client

    def has_clip(self, track_index: int, scene_index: int) -> bool:
        """Check if a clip slot contains a clip.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if the slot contains a clip
        """
        result = self._client.query(
            "/live/clip_slot/get/has_clip", track_index, scene_index
        )
        return bool(result[0])

    def create_clip(
        self, track_index: int, scene_index: int, length: float = 4.0
    ) -> None:
        """Create a new MIDI clip in the slot.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)
            length: Clip length in beats (default: 4.0)
        """
        self._client.send(
            "/live/clip_slot/create_clip", track_index, scene_index, float(length)
        )

    def delete_clip(self, track_index: int, scene_index: int) -> None:
        """Delete the clip in the slot.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)
        """
        self._client.send("/live/clip_slot/delete_clip", track_index, scene_index)

    def fire(self, track_index: int, scene_index: int) -> None:
        """Fire (launch) the clip in the slot.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)
        """
        self._client.send("/live/clip_slot/fire", track_index, scene_index)

    def stop(self, track_index: int, scene_index: int) -> None:
        """Stop the clip in the slot.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)
        """
        self._client.send("/live/clip_slot/stop", track_index, scene_index)

    def get_is_playing(self, track_index: int, scene_index: int) -> bool:
        """Check if the clip in the slot is playing.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if playing
        """
        result = self._client.query(
            "/live/clip_slot/get/is_playing", track_index, scene_index
        )
        return bool(result[0])

    def get_is_triggered(self, track_index: int, scene_index: int) -> bool:
        """Check if the clip slot is triggered (about to play).

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if triggered
        """
        result = self._client.query(
            "/live/clip_slot/get/is_triggered", track_index, scene_index
        )
        return bool(result[0])

    def get_is_recording(self, track_index: int, scene_index: int) -> bool:
        """Check if the clip slot is recording.

        Args:
            track_index: Track index (0-based)
            scene_index: Scene index (0-based)

        Returns:
            True if recording
        """
        result = self._client.query(
            "/live/clip_slot/get/is_recording", track_index, scene_index
        )
        return bool(result[0])
