import logging

from .audion_player import State


class Locked(State):
    def click_lock(self) -> None:
        if self._player.is_playing:
            self.player.transition_to(Playing())
        else:
            self.player.transition_to(Ready())

    def click_play(self) -> None:
        logging.info(
            'The player is locked, so we cannot clieck the play button. Click the "lock" button to unlock the player.'
        )

    def click_next(self) -> None:
        logging.info(
            'The player is locked, so we cannot clieck the next button. Click the "lock" button to unlock the player.'
        )

    def click_previous(self) -> None:
        logging.info(
            'The player is locked, so we cannot clieck the previous button. Click the "lock" button to unlock the player.'
        )

    def increase_volume(self) -> None:
        self.player.increase_volume()

    def decrease_volume(self) -> None:
        self.player.decrease_volume()


class Ready(State):
    def click_lock(self) -> None:
        self.player.transition_to(Locked())

    def click_play(self) -> None:
        self.player.start_playback()
        self.player.transition_to(Playing())

    def click_next(self) -> None:
        self.player.next_song()

    def click_previous(self) -> None:
        self.player.previous_song()


class Playing(State):
    def click_lock(self) -> None:
        self.player.transition_to(Locked())

    def click_play(self) -> None:
        self.player.stop_playback()
        self.player.transition_to(Ready())

    def click_next(self) -> None:
        self.player.next_song()

    def click_previous(self) -> None:
        self.player.previous_song()
