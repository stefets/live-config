import time

from mpyg321.MPyg123Player import MPyg123Player
from mpyg321.consts import PlayerStatus

player = MPyg123Player("mpg123", audiodevice='SD90')
time.sleep(3)
player.quit()
#player.silence()
#player.volume(40)
#time.sleep(3)
#player.set_song ("/tmp/theme.mp3")
#player.play()
#time.sleep(3)
#player.volume(80)
#player.set_song ("/tmp/theme.mp3")
#player.play()
#time.sleep(3)
