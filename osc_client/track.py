"""Track operations for AbletonOSC.

Covers /live/track/* endpoints for individual track control.
"""

from osc_client.client import AbletonOSCClient


class Track:
    """Track operations like volume, pan, mute, solo."""

    def __init__(self, client: AbletonOSCClient):
        self._client = client

    # Name

    def get_name(self, track_index: int) -> str:
        """Get the track name.

        Args:
            track_index: Track index (0-based)

        Returns:
            Track name
        """
        result = self._client.query("/live/track/get/name", track_index)
        return str(result[0]) if result else ""

    def set_name(self, track_index: int, name: str) -> None:
        """Set the track name.

        Args:
            track_index: Track index (0-based)
            name: New track name
        """
        self._client.send("/live/track/set/name", track_index, name)

    # Volume

    def get_volume(self, track_index: int) -> float:
        """Get the track volume.

        Args:
            track_index: Track index (0-based)

        Returns:
            Volume level (0.0-1.0, where 0.85 is 0dB)
        """
        result = self._client.query("/live/track/get/volume", track_index)
        return float(result[0])

    def set_volume(self, track_index: int, volume: float) -> None:
        """Set the track volume.

        Args:
            track_index: Track index (0-based)
            volume: Volume level (0.0-1.0, where 0.85 is 0dB)
        """
        self._client.send("/live/track/set/volume", track_index, float(volume))

    # Pan

    def get_panning(self, track_index: int) -> float:
        """Get the track pan position.

        Args:
            track_index: Track index (0-based)

        Returns:
            Pan position (-1.0 left to 1.0 right, 0.0 center)
        """
        result = self._client.query("/live/track/get/panning", track_index)
        return float(result[0])

    def set_panning(self, track_index: int, pan: float) -> None:
        """Set the track pan position.

        Args:
            track_index: Track index (0-based)
            pan: Pan position (-1.0 left to 1.0 right, 0.0 center)
        """
        self._client.send("/live/track/set/panning", track_index, float(pan))

    # Mute

    def get_mute(self, track_index: int) -> bool:
        """Check if track is muted.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if muted
        """
        result = self._client.query("/live/track/get/mute", track_index)
        return bool(result[0])

    def set_mute(self, track_index: int, muted: bool) -> None:
        """Mute or unmute a track.

        Args:
            track_index: Track index (0-based)
            muted: True to mute
        """
        self._client.send("/live/track/set/mute", track_index, int(muted))

    # Solo

    def get_solo(self, track_index: int) -> bool:
        """Check if track is soloed.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if soloed
        """
        result = self._client.query("/live/track/get/solo", track_index)
        return bool(result[0])

    def set_solo(self, track_index: int, soloed: bool) -> None:
        """Solo or unsolo a track.

        Args:
            track_index: Track index (0-based)
            soloed: True to solo
        """
        self._client.send("/live/track/set/solo", track_index, int(soloed))

    # Arm

    def get_arm(self, track_index: int) -> bool:
        """Check if track is armed for recording.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if armed
        """
        result = self._client.query("/live/track/get/arm", track_index)
        return bool(result[0])

    def set_arm(self, track_index: int, armed: bool) -> None:
        """Arm or disarm a track for recording.

        Args:
            track_index: Track index (0-based)
            armed: True to arm
        """
        self._client.send("/live/track/set/arm", track_index, int(armed))

    # Track info

    def get_color(self, track_index: int) -> int:
        """Get the track color.

        Args:
            track_index: Track index (0-based)

        Returns:
            Color as integer
        """
        result = self._client.query("/live/track/get/color", track_index)
        return int(result[0])

    def set_color(self, track_index: int, color: int) -> None:
        """Set the track color.

        Args:
            track_index: Track index (0-based)
            color: Color as integer
        """
        self._client.send("/live/track/set/color", track_index, color)

    def get_is_foldable(self, track_index: int) -> bool:
        """Check if track is a group track (foldable).

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track is a group
        """
        result = self._client.query("/live/track/get/is_foldable", track_index)
        return bool(result[0])

    def get_is_grouped(self, track_index: int) -> bool:
        """Check if track is inside a group.

        Args:
            track_index: Track index (0-based)

        Returns:
            True if track is in a group
        """
        result = self._client.query("/live/track/get/is_grouped", track_index)
        return bool(result[0])

    # Devices

    def get_num_devices(self, track_index: int) -> int:
        """Get the number of devices on a track.

        Args:
            track_index: Track index (0-based)

        Returns:
            Number of devices
        """
        result = self._client.query("/live/track/get/num_devices", track_index)
        return int(result[0])
