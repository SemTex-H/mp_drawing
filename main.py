import cv2
import numpy as np
import mediapipe as mp
from pythonosc.udp_client import SimpleUDPClient
from time import sleep
import numpy as np

osc = SimpleUDPClient("127.0.0.1", 8000)

# Global variables to store x, y values
x_ = 1920
y_ = 1080
min_x = max_x = min_y = max_y = None
cx = cy = None
detected_once = False  # Flag


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils


def value_mapping(value, in_min, in_max, out_min, out_max):
    return ((value - in_min) / (in_max - in_min)) * (out_max - out_min) + out_min

def detect_green_box(frame):
    global min_x, max_x, min_y, max_y, detected_once

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green color range
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest) > 500:
            points = largest.reshape(-1, 2)
            min_x = int(np.min(points[:, 0]))
            max_x = int(np.max(points[:, 0]))
            min_y = int(np.min(points[:, 1]))
            max_y = int(np.max(points[:, 1]))
            detected_once = True

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Only detect once at the start
    if not detected_once:
        detect_green_box(frame)
        if detected_once:
            print("Green box detected.")
            print(f"min_x = {min_x}, max_x = {max_x}")
            print(f"min_y = {min_y}, max_y = {max_y}")

    
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        # mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        h, w, _ = frame.shape
        cx, cy = int(nose.x * w), int(nose.y * h)
        cv2.circle(frame, (cx, cy), 8, (0, 255, 0), -1)
        cv2.putText(frame, f"HAND: {cx},{cy}", (cx+10, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    if cx and cy:
        if min_x < cx < max_x and min_y < cy < max_y:
            # print(f"HAND is inside the box")
            x_ = value_mapping(cx, min_x, max_x, -0.5, 0.5)
            y_ = value_mapping(cy, min_y, max_y, 1, -1)
            osc.send_message("/pos", [x_, y_])
            # osc.send_message("/draw", 1)
            # osc.send_message("/color", [255, 255, 2551])
            
    # Draw box once it's detected
    # if detected_once:
    #     cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

    cv2.imshow("Live Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
