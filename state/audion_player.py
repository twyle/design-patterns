from __future__ import annotations

import logging
from abc import ABC, abstractmethod

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


class AudioPlayer:
    """This class represents an audio player such as a mobile phone.

    The assumption is that the device has a button for locking or unlocking it and
    another for adjusting the volume.
    """

    def __init__(self, state: State, playlist: list[str]) -> None:
        self._state = state
        self._playlist = playlist
        self._current_song_index = 0
        self._current_song = self._playlist[self._current_song_index]
        self._volume = 0.2
        self._is_playing: bool = False
        self.transition_to(state=state)

    @property
    def is_playing(self) -> bool:
        """Check if the audio player is currently playing a song."""
        return self._is_playing

    @is_playing.setter
    def is_playing(self, is_playing: bool) -> None:
        """Mark the audio player as playing or not playing."""
        self._is_playing = is_playing

    def transition_to(self, state: State) -> None:
        """Change the audio players current state."""
        logging.info("Transitioning to state: %s", type(state).__name__)
        self._state = state
        self._state.player = self

    def click_lock(self) -> None:
        """Locks the audio player user interface.

        Think of this as locking your phone.
        """
        self._state.click_lock()

    def click_play(self) -> None:
        """Click the play button."""
        self._state.click_play()

    def click_next(self) -> None:
        """Click the next button."""
        self._state.click_next()

    def click_previous(self) -> None:
        """Clieck the previous button."""
        self._state.click_previous()

    def start_playback(self):
        """Start playing a song."""
        logging.info("Starting the player.")
        logging.info(
            "The current song is: %s", self._playlist[self._current_song_index]
        )
        logging.info("The volume is: %.2f", self._volume)
        self._is_playing = True

    def stop_playback(self):
        """Pause a song that was playing."""
        logging.info("Stopping the player.")
        logging.info(
            "The current song is: %s", self._playlist[self._current_song_index]
        )
        logging.info("The volume is: %.2f", self._volume)
        self._is_playing = False

    def next_song(self):
        """Move to the next song in the playlist."""
        next_song_index: int = self._current_song_index + 1
        self._current_song_index = next_song_index % len(self._playlist)
        logging.info(
            "Setting the next song: %s", self._playlist[self._current_song_index]
        )

    def previous_song(self):
        """Move to the previous song in the playlist."""
        previous_song_index: int = self._current_song_index - 1
        self._current_song_index = (previous_song_index + len(self._playlist)) % len(
            self._playlist
        )
        logging.info(
            "Setting the previous song: %s", self._playlist[self._current_song_index]
        )

    def increase_volume(self) -> None:
        """Increase the audio player volume."""
        logging.info("Increasing the volume.")
        logging.info("The initial volume is: %.2f", self._volume)
        self._volume += 0.1
        self._volume = min(1.0, self._volume)
        logging.info("The final volume is: %.2f", self._volume)

    def decrease_volume(self) -> None:
        """Decrease the audio player volume."""
        logging.info("Deacresing the volume.")
        logging.info("The initial volume is: %.2f", self._volume)
        self._volume -= 0.1
        self._volume = max(1.0, self._volume)
        logging.info("The final volume is: %.2f", self._volume)


class State(ABC):
    @property
    def player(self) -> AudioPlayer:
        return self._player

    @player.setter
    def player(self, player: AudioPlayer) -> None:
        self._player = player

    @abstractmethod
    def click_lock(self) -> None:
        pass

    @abstractmethod
    def click_play(self) -> None:
        pass

    @abstractmethod
    def click_next(self) -> None:
        pass

    @abstractmethod
    def click_previous(self) -> None:
        pass
