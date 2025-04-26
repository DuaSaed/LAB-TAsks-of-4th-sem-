import os
import cv2
import numpy as np
import mediapipe as mp
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config[r'c:\Users\CWW\Desktop\Face profiling\static'] = r'c:\Users\CWW\Desktop\Face profiling\static\Screenshot 2025-04-26 161714.png'

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)


def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def get_measurements(landmarks, image_shape):
    h, w = image_shape

  
    points = {
        'left_jaw': 234, 
        'right_jaw': 454,  
        'nose_tip': 1,
        'chin': 152,
        'left_eye': 33,
        'right_eye': 263,
        'mouth_left': 61,
        'mouth_right': 291
    }

   
    coords = {name: (int(landmarks[idx].x * w), int(landmarks[idx].y * h)) for name, idx in points.items()}


    measurements = {
        'Jaw Width': euclidean_distance(coords['left_jaw'], coords['right_jaw']),
        'Nose Length': euclidean_distance(coords['nose_tip'], coords['chin']),
        'Eye Distance': euclidean_distance(coords['left_eye'], coords['right_eye']),
        'Mouth Width': euclidean_distance(coords['mouth_left'], coords['mouth_right']),
    }

    return measurements, coords

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config[r'c:\Users\CWW\Desktop\Face profiling\static'], r"c:\Users\CWW\Desktop\Face profiling\static\Screenshot 2025-04-26 161714.png'result.html")
            file.save(filepath)

            img = cv2.imread(filepath)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            results = face_mesh.process(img_rgb)

            if not results.multi_face_landmarks:
                return render_template('result.html', error="No face detected!")

            face_landmarks = results.multi_face_landmarks[0].landmark
            measurements, coords = get_measurements(face_landmarks, img.shape[:2])

            
            for point in coords.values():
                cv2.circle(img, point, 2, (0, 255, 0), -1)

            output_path = os.path.join(app.config[r'c:\Users\CWW\Desktop\Face profiling\static'], 'output_' +r"c:\Users\CWW\Desktop\Face profiling\static\Screenshot 2025-04-26 161714.png")
            cv2.imwrite(output_path, img)

            return render_template('result.html', measurements=measurements, image_path=output_path)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
