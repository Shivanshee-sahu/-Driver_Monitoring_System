import cv2
import face_recognition
import numpy as np
import serial
import time

print("--- Environment Check ---")
print(f"✅ Face Rec: {face_recognition.__version__}")
print(f"✅ OpenCV: {cv2.__version__}")

# ==========================================
# 1. SERIAL SETUP
# ==========================================
try:
    ser = serial.Serial('COM1', 9600, timeout=1)  # CHANGE if needed
    print("✅ Connected to Virtual Microcontroller (COM1)")
except:
    print("❌ Serial not connected. Running vision only.")
    ser = None

# ==========================================
# 2. FUNCTIONS
# ==========================================
def eye_aspect_ratio(eye):
    A = np.linalg.norm(np.array(eye[1]) - np.array(eye[5]))
    B = np.linalg.norm(np.array(eye[2]) - np.array(eye[4]))
    C = np.linalg.norm(np.array(eye[0]) - np.array(eye[3]))
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(landmarks):
    top = landmarks['top_lip']
    bottom = landmarks['bottom_lip']
    v1 = np.linalg.norm(np.array(top[9]) - np.array(bottom[9]))
    v2 = np.linalg.norm(np.array(top[8]) - np.array(bottom[10]))
    v3 = np.linalg.norm(np.array(top[10]) - np.array(bottom[8]))
    h = np.linalg.norm(np.array(top[0]) - np.array(top[6]))
    return (v1 + v2 + v3) / (3.0 * h)

def process_image(frame):
    EYE_THRESH = 0.25
    MOUTH_THRESH = 0.5

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_recognition.face_locations(rgb)

    for face in faces:
        landmarks = face_recognition.face_landmarks(rgb, [face])[0]

        ear = (eye_aspect_ratio(landmarks['left_eye']) +
               eye_aspect_ratio(landmarks['right_eye'])) / 2.0

        mar = mouth_aspect_ratio(landmarks)

        eye_flag = ear < EYE_THRESH
        mouth_flag = mar > MOUTH_THRESH

        return eye_flag, mouth_flag

    return False, False

# ==========================================
# 3. MAIN LOOP
# ==========================================
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

score = 0
eye_closed_counter = 0
prev_state = None

FRAME_THRESHOLD = 15   # blink vs drowsy
prev_time = time.time()

print("🚀 Starting... Press 'q' to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (800, 500))

    eye_flag, mouth_flag = process_image(frame)

    # -------------------------------
    # TEMPORAL LOGIC
    # -------------------------------
    if eye_flag:
        eye_closed_counter += 1
        score += 1
    else:
        eye_closed_counter = 0
        score -= 1

    # clamp score
    score = max(0, min(score, 15))

    # -------------------------------
    # FINAL STATE DECISION
    # -------------------------------
    if eye_closed_counter > FRAME_THRESHOLD or score > 10:
        state = "DROWSY"
    else:
        state = "AWAKE"

    # -------------------------------
    # SERIAL (EDGE TRIGGERED)
    # -------------------------------
    if state != prev_state:
        if ser:
            if state == "DROWSY":
                ser.write(b'\xFF')
            else:
                ser.write(b'\x00')
        prev_state = state

    # -------------------------------
    # FPS CALCULATION
    # -------------------------------
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # -------------------------------
    # DISPLAY
    # -------------------------------
    color = (0, 0, 255) if state == "DROWSY" else (0, 255, 0)

    cv2.putText(frame, f"State: {state}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.putText(frame, f"Score: {score}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

    cv2.imshow("Driver Monitoring", frame)

    if cv2.waitKey(1) & 0xFF in [27, ord('q')]:
        break

cap.release()
if ser:
    ser.close()
cv2.destroyAllWindows()