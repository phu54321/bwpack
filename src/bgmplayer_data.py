from eudplib import *

bgmContent = open('src/bgm22050.wav', 'rb').read()
MPQAddWave('staredit\\wav\\bgmmain.wav', bgmContent)
