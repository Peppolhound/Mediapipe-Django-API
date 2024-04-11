
from flask import Flask, render_template, Response, request, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField
import cv2
import os
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# Setting
app = Flask(__name__)
app.secret_key = '1234'

camera = cv2.VideoCapture(0)


# Function to upload video
class VideoUploadForm(FlaskForm):
    video = FileField('Video', validators=[FileRequired()])
    submit = SubmitField('Upload')

# Function to process frames and detect hand landmarks
def detect_sign_language(frame):
    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the frame
    with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        process_frames = hands.process(rgb_frame)
        # Draw landmarks on the frame
        if process_frames.multi_hand_landmarks:
            for lm in process_frames.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
    return frame
# Release resources
hands.close()


# Function to generate video frames
def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = detect_sign_language(frame)  # Use the function from Step 1
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_input')
def video_input():
    # Questa route ora renderizza un template HTML
    return render_template('video_stream.html')

# Route for the main page
@app.route('/')
def index():
    return render_template('home.html')

# Route for video upload
@app.route('/video_upload', methods=['GET', 'POST'])
def video_upload():
    form = VideoUploadForm()
    if form.validate_on_submit():
        # Take file from form
        video_file = form.video.data
        filename = secure_filename(video_file.filename)
        # Save file in media folder
        video_path = os.path.join('static/videos/', filename)
        video_file.save(video_path)

        # Process video
        ### 
        # Get vide url
        video_url = url_for('static', filename= f'videos/{filename}')
        return render_template('view_video.html', video_url=video_url)
        # return redirect(url_for('view_video'))
    # Redirect user
    return render_template('video_upload.html', form=form)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
