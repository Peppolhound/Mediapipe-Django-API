from flask import Flask, render_template, Response, request, redirect, url_for, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField
import cv2
import os
import mediapipe as mp

# Initialize MediaPipe Hands
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) 


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
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        process_frames = pose.process(rgb_frame)
        # Draw landmarks on the frame
        if process_frames.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame, 
                    process_frames.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                )
    return frame

# Function to generate video frames
def generate_frames(filename=None):
    if filename is not None:
        camera = cv2.VideoCapture(filename)
    else: 
        camera = cv2.VideoCapture(0)
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

# Release resources
pose.close()

# Route for the video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(filename=None), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for show video
@app.route('/video_input')
def video_input():
    session['streaming'] = True
    return render_template('video_stream.html')

# Route for video upload
@app.route('/video_upload', methods=['GET', 'POST'])
def video_upload():
    form = VideoUploadForm()
    if form.validate_on_submit():
        # Take file from form
        video_file = form.video.data
        filename = secure_filename(video_file.filename)
        # Save file in media folder
        # video_path = os.path.join('static/videos/', filename)
        # video_file.save(video_path)

        # Process video
        return Response(generate_frames(filename=filename), mimetype='multipart/x-mixed-replace; boundary=frame')

    #     # Get video url
    #     video_url = url_for('static', filename= f'videos/{filename}')
    #     return render_template('view_video.html', video_url=video_url)
    #     # return redirect(url_for('view_video'))
    # # Redirect user
    return render_template('video_upload.html', form=form)

# Route for show video
@app.route('/video_upload_input')
def video_upload_input():
    return render_template('view_video.html')

# Route for the main page
@app.route('/')
def index():
    camera.release()
    session['streaming'] = False
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
