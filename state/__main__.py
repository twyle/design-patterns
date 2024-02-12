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
