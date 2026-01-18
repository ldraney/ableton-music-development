"""Scene operations for AbletonOSC.

Covers /live/scene/* endpoints for scene control.
"""

from osc_client.client import AbletonOSCClient


class Scene:
    """Scene operations like firing scenes and getting/setting names."""

    def __init__(self, client: AbletonOSCClient):
        self._client = client

    def get_name(self, scene_index: int) -> str:
        """Get the scene name.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Scene name
        """
        result = self._client.query("/live/scene/get/name", scene_index)
        return str(result[0]) if result else ""

    def set_name(self, scene_index: int, name: str) -> None:
        """Set the scene name.

        Args:
            scene_index: Scene index (0-based)
            name: New scene name
        """
        self._client.send("/live/scene/set/name", scene_index, name)

    def fire(self, scene_index: int) -> None:
        """Fire (launch) a scene.

        This launches all clips in the scene row.

        Args:
            scene_index: Scene index (0-based)
        """
        self._client.send("/live/scene/fire", scene_index)

    def get_color(self, scene_index: int) -> int:
        """Get the scene color.

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Color as integer
        """
        result = self._client.query("/live/scene/get/color", scene_index)
        return int(result[0])

    def set_color(self, scene_index: int, color: int) -> None:
        """Set the scene color.

        Args:
            scene_index: Scene index (0-based)
            color: Color as integer
        """
        self._client.send("/live/scene/set/color", scene_index, color)

    def get_tempo(self, scene_index: int) -> float:
        """Get the scene tempo (if set).

        Args:
            scene_index: Scene index (0-based)

        Returns:
            Scene tempo in BPM, or 0 if not set
        """
        result = self._client.query("/live/scene/get/tempo", scene_index)
        return float(result[0]) if result else 0.0

    def set_tempo(self, scene_index: int, tempo: float) -> None:
        """Set the scene tempo.

        Args:
            scene_index: Scene index (0-based)
            tempo: Tempo in BPM
        """
        self._client.send("/live/scene/set/tempo", scene_index, float(tempo))

    def get_is_triggered(self, scene_index: int) -> bool:
        """Check if the scene is triggered (about to play).

        Args:
            scene_index: Scene index (0-based)

        Returns:
            True if triggered
        """
        result = self._client.query("/live/scene/get/is_triggered", scene_index)
        return bool(result[0])
