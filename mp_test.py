import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

# Start camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to RGB for MediaPipe
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    # Draw skeleton if detected
    if results.pose_landmarks:
        # mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Example: Get nose position (landmark 0)
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        h, w, _ = frame.shape
        cx, cy = int(nose.x * w), int(nose.y * h)
        cv2.circle(frame, (cx, cy), 8, (0, 255, 0), -1)
        cv2.putText(frame, f"NOSE: {cx},{cy}", (cx+10, cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

    # Show output
    cv2.imshow("MediaPipe Skeleton", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
