from pythonosc.udp_client import SimpleUDPClient
from time import sleep
import numpy as np

osc = SimpleUDPClient("127.0.0.1", 8000)

for i in np.arange(-0.5, 0.5, 0.01):
    for j in np.arange(-1.0, 1.0, 0.01):
        osc.send_message("/pos", [i, j])
        osc.send_message("/draw", 1)
        if i*100 % 3 == 0:
            osc.send_message("/color", [255, 0, 0])
        elif i*100 % 3 == 1:
            osc.send_message("/color", [0, 255, 0])
        else:
            osc.send_message("/color", [0, 0, 255])
    
        sleep(0.001)
