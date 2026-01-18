"""Song-level operations for AbletonOSC.

Covers /live/song/* endpoints for global song properties and transport.
"""

from typing import Callable

from osc_client.client import AbletonOSCClient


class Song:
    """Song-level operations like tempo, transport, and song structure."""

    def __init__(self, client: AbletonOSCClient):
        self._client = client

    # Tempo

    def get_tempo(self) -> float:
        """Get the current song tempo in BPM.

        Returns:
            Tempo in beats per minute (20-999)
        """
        result = self._client.query("/live/song/get/tempo")
        return float(result[0])

    def set_tempo(self, bpm: float) -> None:
        """Set the song tempo.

        Args:
            bpm: Tempo in beats per minute (20-999)
        """
        self._client.send("/live/song/set/tempo", float(bpm))

    # Transport

    def get_is_playing(self) -> bool:
        """Check if the song is currently playing.

        Returns:
            True if playing, False if stopped
        """
        result = self._client.query("/live/song/get/is_playing")
        return bool(result[0])

    def start_playing(self) -> None:
        """Start playback."""
        self._client.send("/live/song/start_playing")

    def stop_playing(self) -> None:
        """Stop playback."""
        self._client.send("/live/song/stop_playing")

    def continue_playing(self) -> None:
        """Continue playback from current position."""
        self._client.send("/live/song/continue_playing")

    # Time signature

    def get_signature_numerator(self) -> int:
        """Get the time signature numerator.

        Returns:
            Time signature numerator (e.g., 4 for 4/4)
        """
        result = self._client.query("/live/song/get/signature_numerator")
        return int(result[0])

    def get_signature_denominator(self) -> int:
        """Get the time signature denominator.

        Returns:
            Time signature denominator (e.g., 4 for 4/4)
        """
        result = self._client.query("/live/song/get/signature_denominator")
        return int(result[0])

    def set_signature_numerator(self, numerator: int) -> None:
        """Set the time signature numerator.

        Args:
            numerator: Time signature numerator
        """
        self._client.send("/live/song/set/signature_numerator", int(numerator))

    def set_signature_denominator(self, denominator: int) -> None:
        """Set the time signature denominator.

        Args:
            denominator: Time signature denominator (must be power of 2)
        """
        self._client.send("/live/song/set/signature_denominator", int(denominator))

    # Song structure

    def get_num_tracks(self) -> int:
        """Get the number of tracks in the song.

        Returns:
            Number of tracks (including return tracks and master)
        """
        result = self._client.query("/live/song/get/num_tracks")
        return int(result[0])

    def get_num_scenes(self) -> int:
        """Get the number of scenes in the song.

        Returns:
            Number of scenes
        """
        result = self._client.query("/live/song/get/num_scenes")
        return int(result[0])

    # Position

    def get_current_song_time(self) -> float:
        """Get the current playback position in beats.

        Returns:
            Current position in beats
        """
        result = self._client.query("/live/song/get/current_song_time")
        return float(result[0])

    def set_current_song_time(self, beats: float) -> None:
        """Set the playback position.

        Args:
            beats: Position in beats
        """
        self._client.send("/live/song/set/current_song_time", float(beats))

    # Metronome

    def get_metronome(self) -> bool:
        """Check if the metronome is enabled.

        Returns:
            True if metronome is on
        """
        result = self._client.query("/live/song/get/metronome")
        return bool(result[0])

    def set_metronome(self, enabled: bool) -> None:
        """Enable or disable the metronome.

        Args:
            enabled: True to enable metronome
        """
        self._client.send("/live/song/set/metronome", int(enabled))

    # Record

    def get_record_mode(self) -> bool:
        """Check if record mode is enabled.

        Returns:
            True if record mode is on
        """
        result = self._client.query("/live/song/get/record_mode")
        return bool(result[0])

    def set_record_mode(self, enabled: bool) -> None:
        """Enable or disable record mode.

        Args:
            enabled: True to enable record mode
        """
        self._client.send("/live/song/set/record_mode", int(enabled))

    # Listeners

    def on_tempo_change(self, callback: Callable[[float], None]) -> None:
        """Register a callback for tempo changes.

        Args:
            callback: Function(tempo) called when tempo changes
        """
        self._client.send("/live/song/start_listen/tempo")
        self._client.start_listener(
            "/live/song/get/tempo", lambda addr, *args: callback(float(args[0]))
        )

    def stop_tempo_listener(self) -> None:
        """Stop listening for tempo changes."""
        self._client.send("/live/song/stop_listen/tempo")
        self._client.stop_listener("/live/song/get/tempo")

    def on_is_playing_change(self, callback: Callable[[bool], None]) -> None:
        """Register a callback for play state changes.

        Args:
            callback: Function(is_playing) called when play state changes
        """
        self._client.send("/live/song/start_listen/is_playing")
        self._client.start_listener(
            "/live/song/get/is_playing", lambda addr, *args: callback(bool(args[0]))
        )

    def stop_is_playing_listener(self) -> None:
        """Stop listening for play state changes."""
        self._client.send("/live/song/stop_listen/is_playing")
        self._client.stop_listener("/live/song/get/is_playing")
