import time
from mpyg321.mpyg321 import MPyg321Player, PlayerStatus

player = MPyg321Player(audiodevice='hw:1,0')
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
