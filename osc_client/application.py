"""Application-level operations for AbletonOSC.

Covers /live/application/* and /live/api/* endpoints.
"""

from osc_client.client import AbletonOSCClient


class Application:
    """Application-level operations like version info and connection testing."""

    def __init__(self, client: AbletonOSCClient):
        self._client = client

    def test(self, timeout: float = 2.0) -> bool:
        """Test the connection to AbletonOSC.

        Args:
            timeout: How long to wait for response

        Returns:
            True if connection is working

        Raises:
            TimeoutError: If Ableton/AbletonOSC not responding
        """
        self._client.query("/live/test", timeout=timeout)
        return True

    def get_version(self) -> str:
        """Get the Ableton Live version string.

        Returns:
            Version string (e.g., "12.0.1")
        """
        result = self._client.query("/live/application/get/version")
        return str(result[0]) if result else ""

    def get_api_version(self) -> int:
        """Get the AbletonOSC API version.

        Returns:
            API version number
        """
        result = self._client.query("/live/api/get/version")
        return int(result[0]) if result else 0
