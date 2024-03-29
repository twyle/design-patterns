# State Design Pattern in Python
This is a pattern that enables an object to behave differently depending on its internal state. By behaving differently, I mean when a particular methods is called, how the object handles the method call.

<p align=center>
  <img src="../assets/player.png" />
</p>

Think of an ``Audio Player``. It has three definate states:
- ```Locked```: in this state, the user cannot access the player UI. Same as when you lock your phone by clicking the lock button
- ```Ready```: when you click on the lock button, when your phone was locked. This unlocks it and gives you access to the phones user interface.
- ```Playing```: this is when the player is actually playing some music.

As a simple example consider this workflow. Assume that the only application that your phone has is the music player:
1. Your phone is initially locked. At this point, you cannot use any functionality except click on the lock button or the volume buttons. This is the initial ```State```, that we refer to as the ```Locked State```.
2. So you click on the ```lock button```. This unlocks your phone and now you can interact with the phone via the User Interface besides the volume and lock buttons. This is the ```Ready state```. At this point, you can once again lock the phone, adjust the volume, scroll through the playlist or even start playing music.
3. To start playing music, you click on the ```play button```. This takes the ```Player``` to the ```Playing State```. In this state, you can also adjust the volume, scroll through the playlist or even decide to lock the phone.

Depending on the particular state, the player may behave differently. For example, when ```locked```, clicking the ```lock button``` unlocks the phone. However clicking the ```next button``` or ```previous button``` does nothing(in this case we cannot even access them). However when the player is in a ```playing state```, clicking on the ```next button``` plays the next song. When in the ```Ready State```, clicking the ```play button``` starts playing music and takes the player to the ```Playing State```, whereas while in the ```Playing State```, this pauses the music playing and takes the ```Player``` to the ```Ready State```.

This pattern has two major components:
- ``Context`` which is the object whose behavior changes based on its internal state.
- ``State`` which describes the various states that the ``Context`` can assume.

The ``Context`` receives various requests. In this example, these could include:
- Lock or unlock
- Set the previous or next song
- Play or pause current song
- Adjust the volume

The ``Context`` keeps track of its current ``State``. It then uses the underlying state object to handle these requests. The assumption is that each ``State`` object knows how to handle each request.

Here is the state interface:
```py
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

```

Each concrete state will have to implement those four abstract methods. In addition, each receives a refrence to the ``Context`` that can be used to change the ``Context's`` state.

Here is the ```Playing State```:
```py
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
```

For the ``Context``, in this case the ``AudioPlayer``, here is the code:
```py
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
```
It simply passes the various requests to the underlying state. It also implements a couple of methods to make the whole solution work. To set it up, we set a workflow:
```py
from .audion_player import AudioPlayer
from .states import Locked

if __name__ == "__main__":
    playlist: list[str] = ["first", "second", "third", "fourth", "fifth"]
    player: AudioPlayer = AudioPlayer(state=Locked(), playlist=playlist)
    player.click_lock()  # Unlock the player from locked to ready
    player.click_play()  # play the current song at index 0
    player.increase_volume()  # increase teh volume
    player.increase_volume()  # increase teh volume
    player.click_next()  # move to the song at index 1
    player.increase_volume()  # increase teh volume
    player.increase_volume()  # increase teh volume
    player.click_next()  # move to the song at index 2
    player.click_previous()  # move to the song at index 1
    player.click_play()  # pause the playback
    player.click_lock()  # lock the player
    player.click_play()  # does nothing, player is currently lokced
    player.click_lock()  # unlock the player, ready state
    player.click_play()  # resume playing
    player.click_lock()  # lock the player
    player.click_lock()  # unlock the player and resume playing
```

Run this workflow:
```sh
python -m state
```

Here is the output:
```sh
2024-02-12 21:35:37,311 - root - INFO - Transitioning to state: Locked
2024-02-12 21:35:37,311 - root - INFO - Transitioning to state: Ready
2024-02-12 21:35:37,312 - root - INFO - Starting the player.
2024-02-12 21:35:37,312 - root - INFO - The current song is: first
2024-02-12 21:35:37,312 - root - INFO - The volume is: 0.20
2024-02-12 21:35:37,312 - root - INFO - Transitioning to state: Playing
2024-02-12 21:35:37,312 - root - INFO - Increasing the volume.
2024-02-12 21:35:37,312 - root - INFO - The initial volume is: 0.20
2024-02-12 21:35:37,312 - root - INFO - The final volume is: 0.30
2024-02-12 21:35:37,312 - root - INFO - Increasing the volume.
2024-02-12 21:35:37,312 - root - INFO - The initial volume is: 0.30
2024-02-12 21:35:37,312 - root - INFO - The final volume is: 0.40
2024-02-12 21:35:37,312 - root - INFO - Setting the next song: second
2024-02-12 21:35:37,312 - root - INFO - Increasing the volume.
2024-02-12 21:35:37,312 - root - INFO - The initial volume is: 0.40
2024-02-12 21:35:37,312 - root - INFO - The final volume is: 0.50
2024-02-12 21:35:37,312 - root - INFO - Increasing the volume.
2024-02-12 21:35:37,312 - root - INFO - The initial volume is: 0.50
2024-02-12 21:35:37,312 - root - INFO - The final volume is: 0.60
2024-02-12 21:35:37,313 - root - INFO - Setting the next song: third
2024-02-12 21:35:37,313 - root - INFO - Setting the previous song: second
2024-02-12 21:35:37,313 - root - INFO - Stopping the player.
2024-02-12 21:35:37,313 - root - INFO - The current song is: second
2024-02-12 21:35:37,313 - root - INFO - The volume is: 0.60
2024-02-12 21:35:37,313 - root - INFO - Transitioning to state: Ready
2024-02-12 21:35:37,313 - root - INFO - Transitioning to state: Locked
2024-02-12 21:35:37,313 - root - INFO - The player is locked, so we cannot clieck the play button. Click the "lock" button to unlock the player.
2024-02-12 21:35:37,313 - root - INFO - Transitioning to state: Ready
2024-02-12 21:35:37,313 - root - INFO - Starting the player.
2024-02-12 21:35:37,313 - root - INFO - The current song is: second
2024-02-12 21:35:37,313 - root - INFO - The volume is: 0.60
2024-02-12 21:35:37,313 - root - INFO - Transitioning to state: Playing
2024-02-12 21:35:37,314 - root - INFO - Transitioning to state: Locked
2024-02-12 21:35:37,314 - root - INFO - Transitioning to state: Playing
```