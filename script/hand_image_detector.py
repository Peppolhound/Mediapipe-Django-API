import cv2
import mediapipe as mp
import subprocess
import os


def hand_detection(video_path):
    # Setting algoritmo MediaPipe
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode = False,
        max_num_hands = 2,
        min_detection_confidence = 0.5, 
        min_tracking_confidence = 0.5)
    
    # Pre-processing: rimozione audio dal video
    temp_path = 'media/video_temp.mp4'
    command = ['ffmpeg', '-i', video_path, '-c:v', 'copy', '-an', temp_path]
    subprocess.run(command)
    print("Pre-processing terminato")

    # Lettura video
    cap = cv2.VideoCapture(temp_path)
    if not cap.isOpened():
        print("ERRORE: impossibile aprire il video")

    while cap.isOpened():
        # Lettura frame
        ret, frame = cap.read()
        if not ret: 
            print("Fine del video o errore nella lettura del frame")
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Processing con algoritmo MediaPipe
        results = hands.process(frame_rgb)
        
        # Disegno skeleton
        if results.multi_hand_landmarks: 
            for hand_landmark in results.multi_hand_landmarks: 
                mp_drawing.draw_landmarks(
                    frame, hand_landmark, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2))
        else: 
            print("Mani non identificate")
        
        # cv2.imshow("Frame", frame)

        # if cv2.waitKey(1) & 0XFF == ord('q'):
        #   break
    
    cap.release()
    cv2.destroyAllWindows()
    hands.close()
    # Eliminazione file temporaneo (video senza audio)
    os.remove(temp_path)