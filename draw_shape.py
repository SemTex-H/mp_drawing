from pythonosc.udp_client import SimpleUDPClient
import math
import time
import numpy as np

ip = "127.0.0.1"
port = 8000

client = SimpleUDPClient(ip, port)

radius = 0.25  
center_x = 0.0
center_y = 0.0


def send_xy(x, y):
    client.send_message("/pos", [x, y])

def draw_square(center_x=0.5, center_y=0.5, size=0.8, steps_per_edge=20):
    half = size / 2
    corners = [
        (center_x - half, center_y - half),
        (center_x + half, center_y - half),
        (center_x + half, center_y + half),
        (center_x - half, center_y + half),
    ]

    for i in range(4):
        x0, y0 = corners[i]
        x1, y1 = corners[(i + 1) % 4]
        for j in range(steps_per_edge):
            t = j / steps_per_edge
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            send_xy(x / 2, y)
            time.sleep(0.05)

def draw_triangle(center_x=0.5, center_y=0.5, size=0.8, steps_per_edge=20):
    h = math.sqrt(3) / 2 * size
    corners = [
        (center_x, center_y - 2/3 * h),
        (center_x - size/2, center_y + h/3),
        (center_x + size/2, center_y + h/3),
    ]

    for i in range(3):
        x0, y0 = corners[i]
        x1, y1 = corners[(i + 1) % 3]
        for j in range(steps_per_edge):
            t = j / steps_per_edge
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            send_xy(x / 2, y)
            time.sleep(0.05)

time.sleep(5)
client.send_message("/drawing", 1)

client.send_message("/color", [1, 0, 0])
for angle in np.arange(0, 360, 0.005):
    rad = math.radians(angle)
    x = center_x + radius * math.cos(rad) /2
    y = center_y + radius * math.sin(rad)

    # Send as two floats
    client.send_message("/pos", [x, y])



client.send_message("/color", [0, 1, 0])
draw_square(-0.5, 0, 0.25, 20)

client.send_message("/color", [0, 0, 1])
draw_triangle(0.5, 0, 0.25, 20)


client.send_message("/drawing", 0)