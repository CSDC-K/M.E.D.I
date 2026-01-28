# ai_model.py
import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Global variables
cap = None
counter = 0
stage = "up" 
finished = False
TARGET_REPS = 5

def calculate_angle(a, b, c):
    """3 nokta arasındaki açıyı hesaplar."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

def start_camera():
    """Kamerayı başlatır ve sayacı sıfırlar"""
    global cap, counter, stage, finished
    
    counter = 0
    stage = "up" 
    finished = False

    if cap is None:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

def stop_camera():
    """Kamerayı kapatır"""
    global cap
    if cap is not None:
        cap.release()
        cap = None

def get_ai_frame():
    global counter, stage, finished

    # --- DÜZELTME BURADA YAPILDI ---
    # start_camera() her karede çağrılmamalı, sadece kamera yoksa çağrılmalı.
    if cap is None:
        start_camera()
    # -------------------------------

    if cap is None:
        return None

    ret, frame = cap.read()
    if not ret:
        return None

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb.flags.writeable = False
    results = pose.process(frame_rgb)
    frame_rgb.flags.writeable = True

    current_angle = 0 

    if results.pose_landmarks:
        try:
            landmarks = results.pose_landmarks.landmark
            
            left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
            left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
            left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
            
            # --- Görünürlük Kontrolü ---
            if left_hip.visibility > 0.6 and left_knee.visibility > 0.6 and left_ankle.visibility > 0.6:
                
                hip_coords = [left_hip.x, left_hip.y]
                knee_coords = [left_knee.x, left_knee.y]
                ankle_coords = [left_ankle.x, left_ankle.y]
                
                angle = calculate_angle(hip_coords, knee_coords, ankle_coords)
                current_angle = int(angle)
                
                # --- SQUAT MANTIĞI ---
                
                # 1. Ayakta Durma (Reset)
                if angle > 155:
                    stage = "up"
                    
                # 2. Çömelme (Sayma Kuralı)
                if angle < 145 and stage == 'up': 
                    stage = "down" 
                    counter += 1
                    if counter >= TARGET_REPS:
                        finished = True
                
                # --- AÇIYI GÖRSELLEŞTİRME ---
                cv2.putText(frame, str(current_angle), 
                            tuple(np.multiply(knee_coords, [640, 480]).astype(int)), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3, cv2.LINE_AA)
                                
        except Exception as e:
            pass

        # İskelet Çizimi
        mp_drawing.draw_landmarks(
            frame, 
            results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0,255,255), thickness=3, circle_radius=3),
            mp_drawing.DrawingSpec(color=(255,255,255), thickness=3)
        )

    # UI Bilgi Kutusu
    cv2.rectangle(frame, (0,0), (250,85), (245,117,16), -1)
    
    cv2.putText(frame, 'Tekrarlar', (15,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(frame, str(counter), (10,75), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255,255,255), 2, cv2.LINE_AA)
    
    cv2.putText(frame, 'Aşama', (90,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(frame, stage if stage else "Start", (85,75), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)

    cv2.putText(frame, 'Oran', (170,20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1, cv2.LINE_AA)
    cv2.putText(frame, str(current_angle), (165,75), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)


    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    height, width, _ = frame_rgba.shape
    return (frame_rgba.tobytes(), width, height, counter, finished)