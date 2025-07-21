import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(image)

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            # Get index finger tip
            x = hand.landmark[8].x  # Normalized
            y = hand.landmark[8].y
            # Convert to pixel position
            height, width, _ = frame.shape
            px, py = int(x * width), int(y * height)
            print(f"Hand at {px}, {py}")
