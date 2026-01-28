import cv2
import mediapipe as mp
import math
import time
from collections import deque

# ----------------- AYARLAR -----------------
DOWN_ANGLE_THRESHOLD = 95     # squat aşağıda sayılması için maksimum diz açısı
UP_ANGLE_THRESHOLD = 160      # squat yukarıda sayılması için minimum diz açısı
SMOOTHING_WINDOW = 5          # açı ortalaması için pencere boyutu
MIN_BOTTOM_TIME = 0.15        # down pozunda en az bekleme süresi (s)
MIN_TIME_BETWEEN_REPS = 0.7   # tekrarlar arası min süre (s)
# -------------------------------------------

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """Üç nokta arasındaki açıyı derece cinsinden hesaplar."""
    xa, ya = a
    xb, yb = b
    xc, yc = c
    v1 = (xa - xb, ya - yb)
    v2 = (xc - xb, yc - yb)
    dot = v1[0]*v2[0] + v1[1]*v2[1]
    mag1 = math.hypot(*v1)
    mag2 = math.hypot(*v2)
    if mag1 == 0 or mag2 == 0:
        return 180
    cosang = dot / (mag1 * mag2)
    cosang = max(-1.0, min(1.0, cosang))
    return math.degrees(math.acos(cosang))

class SquatCounter:
    def __init__(self):
        self.state = "up"
        self.count = 0
        self.angle_buffer = deque(maxlen=SMOOTHING_WINDOW)
        self.last_down_time = None
        self.last_rep_time = 0

    def update(self, angle):
        self.angle_buffer.append(angle)
        smooth_angle = sum(self.angle_buffer) / len(self.angle_buffer)
        now = time.time()

        if self.state == "up":
            if smooth_angle < DOWN_ANGLE_THRESHOLD:
                self.state = "down"
                self.last_down_time = now
        elif self.state == "down":
            if smooth_angle > UP_ANGLE_THRESHOLD:
                bottom_time = now - (self.last_down_time or now)
                if bottom_time >= MIN_BOTTOM_TIME and (now - self.last_rep_time) >= MIN_TIME_BETWEEN_REPS:
                    self.count += 1
                    self.last_rep_time = now
                self.state = "up"

        return self.count, self.state, smooth_angle

# ----------------- ANA PROGRAM -----------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1680)

counter = SquatCounter()

with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # Mediapipe ile işleme
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            # Sağ diz açısı (hip-knee-ankle)
            hip = (int(lm[24].x * w), int(lm[24].y * h))
            knee = (int(lm[26].x * w), int(lm[26].y * h))
            ankle = (int(lm[28].x * w), int(lm[28].y * h))

            angle = calculate_angle(hip, knee, ankle)
            count, state, smooth_angle = counter.update(angle)

            # çizim
            cv2.putText(frame, f"Squats: {count}", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 3)
            cv2.putText(frame, f"State: {state}", (30, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,200,255), 2)
            cv2.putText(frame, f"Angle: {int(smooth_angle)}", (30, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200,200,200), 2)

            cv2.circle(frame, hip, 6, (0,0,255), -1)
            cv2.circle(frame, knee, 6, (0,255,0), -1)
            cv2.circle(frame, ankle, 6, (255,0,0), -1)
            cv2.line(frame, hip, knee, (255,255,255), 2)
            cv2.line(frame, knee, ankle, (255,255,255), 2)

        cv2.imshow("Squat Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
