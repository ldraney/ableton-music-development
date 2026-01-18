"""Device operations for AbletonOSC.

Covers /live/device/* endpoints for device and parameter control.
"""

from typing import NamedTuple

from osc_client.client import AbletonOSCClient


class Parameter(NamedTuple):
    """Represents a device parameter.

    Attributes:
        index: Parameter index within the device
        name: Parameter name
        value: Current value
        min: Minimum value
        max: Maximum value
    """

    index: int
    name: str
    value: float
    min: float
    max: float


class Device:
    """Device operations like getting/setting parameters."""

    def __init__(self, client: AbletonOSCClient):
        self._client = client

    def get_name(self, track_index: int, device_index: int) -> str:
        """Get the device name.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            Device name
        """
        result = self._client.query(
            "/live/device/get/name", track_index, device_index
        )
        return str(result[0]) if result else ""

    def get_class_name(self, track_index: int, device_index: int) -> str:
        """Get the device class name (type).

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            Device class name (e.g., "Compressor", "Reverb")
        """
        result = self._client.query(
            "/live/device/get/class_name", track_index, device_index
        )
        return str(result[0]) if result else ""

    def get_is_active(self, track_index: int, device_index: int) -> bool:
        """Check if the device is active (enabled).

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            True if device is active
        """
        result = self._client.query(
            "/live/device/get/is_active", track_index, device_index
        )
        return bool(result[0])

    def set_is_active(
        self, track_index: int, device_index: int, active: bool
    ) -> None:
        """Enable or disable a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            active: True to enable, False to bypass
        """
        self._client.send(
            "/live/device/set/is_active", track_index, device_index, int(active)
        )

    def get_num_parameters(self, track_index: int, device_index: int) -> int:
        """Get the number of parameters on a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            Number of parameters
        """
        result = self._client.query(
            "/live/device/get/num_parameters", track_index, device_index
        )
        return int(result[0])

    def get_parameter_value(
        self, track_index: int, device_index: int, parameter_index: int
    ) -> float:
        """Get a parameter value.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Current parameter value
        """
        result = self._client.query(
            "/live/device/get/parameter/value",
            track_index,
            device_index,
            parameter_index,
        )
        return float(result[0])

    def set_parameter_value(
        self,
        track_index: int,
        device_index: int,
        parameter_index: int,
        value: float,
    ) -> None:
        """Set a parameter value.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)
            value: New parameter value
        """
        self._client.send(
            "/live/device/set/parameter/value",
            track_index,
            device_index,
            parameter_index,
            float(value),
        )

    def get_parameter_name(
        self, track_index: int, device_index: int, parameter_index: int
    ) -> str:
        """Get a parameter name.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Parameter name
        """
        result = self._client.query(
            "/live/device/get/parameter/name",
            track_index,
            device_index,
            parameter_index,
        )
        return str(result[0]) if result else ""

    def get_parameter_min(
        self, track_index: int, device_index: int, parameter_index: int
    ) -> float:
        """Get a parameter's minimum value.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Minimum parameter value
        """
        result = self._client.query(
            "/live/device/get/parameter/min",
            track_index,
            device_index,
            parameter_index,
        )
        return float(result[0])

    def get_parameter_max(
        self, track_index: int, device_index: int, parameter_index: int
    ) -> float:
        """Get a parameter's maximum value.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)
            parameter_index: Parameter index (0-based)

        Returns:
            Maximum parameter value
        """
        result = self._client.query(
            "/live/device/get/parameter/max",
            track_index,
            device_index,
            parameter_index,
        )
        return float(result[0])

    def get_parameters(
        self, track_index: int, device_index: int
    ) -> list[Parameter]:
        """Get all parameters for a device.

        Args:
            track_index: Track index (0-based)
            device_index: Device index on track (0-based)

        Returns:
            List of Parameter objects
        """
        num_params = self.get_num_parameters(track_index, device_index)
        parameters = []

        for i in range(num_params):
            name = self.get_parameter_name(track_index, device_index, i)
            value = self.get_parameter_value(track_index, device_index, i)
            min_val = self.get_parameter_min(track_index, device_index, i)
            max_val = self.get_parameter_max(track_index, device_index, i)
            parameters.append(
                Parameter(index=i, name=name, value=value, min=min_val, max=max_val)
            )

        return parameters
