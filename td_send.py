from pythonosc.udp_client import SimpleUDPClient
from time import sleep
import numpy as np

osc = SimpleUDPClient("127.0.0.1", 8000)

# # Example
# px = 0.1
# py = 0.4
# osc.send_message("/draw", 0)         # Start drawing
# osc.send_message("/pos", [px, py])   # Hand position
# osc.send_message("/color", [255, 0, 0])  # RGB color

for i in np.arange(-1.0, 1.0, 0.01):
    for j in np.arange(-0.5, 0.5, 0.01):
        osc.send_message("/pos", [i, j])
        sleep(0.005)