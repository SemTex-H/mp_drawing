import cv2
import numpy as np
import mediapipe as mp


# Global variables to store x, y values
min_x = max_x = min_y = max_y = None
detected_once = False  # Flag

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

# Open camera
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

    # Draw box once it's detected
    if detected_once:
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (0, 255, 0), 2)

    cv2.putText(frame, f"HAND", (500, 720), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
    # Show live feed
    cv2.imshow("Live Feed", frame)

    # Exit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
