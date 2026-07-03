# ==============================
# IMPORT LIBRARIES
# ==============================

import cv2
import numpy as np
import streamlit as st

st.write("OpenCV version:", cv2.__version__)
st.write("OpenCV file:", cv2.__file__)
st.write("Has CascadeClassifier:", hasattr(cv2, "CascadeClassifier"))
st.write("First 20 cv2 attributes:", dir(cv2)[:20])

# ==============================
# IMAGE ANALYSIS FUNCTION
# ==============================

def analyze_image(uploaded_file):

    # ==============================
    # READ IMAGE
    # ==============================

    file_bytes = np.asarray(
        bytearray(uploaded_file.read()),
        dtype=np.uint8
    )

    img = cv2.imdecode(file_bytes, 1)

    # ==============================
    # CONVERT TO GRAYSCALE
    # ==============================

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # ==============================
    # FACE DETECTION
    # ==============================

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        'haarcascade_frontalface_default.xml'
    )

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    face_detected = len(faces) > 0

    # ==============================
    # BRIGHTNESS ANALYSIS
    # ==============================

    brightness = gray.mean()

    # ==============================
    # OPEN TO WORK DETECTION
    # ==============================

    open_to_work_detected = False

    green_ratio = 0

    # Check only near detected face
    if face_detected:

        for (x, y, w, h) in faces:

            # Margin around face
            margin = 40

            x1 = max(x - margin, 0)
            y1 = max(y - margin, 0)

            x2 = min(x + w + margin, img.shape[1])
            y2 = min(y + h + margin, img.shape[0])

            # Extract face area
            face_area = img[y1:y2, x1:x2]

            # Detect LinkedIn green ring

            green_pixels = np.sum(

                (face_area[:, :, 1] > 130) &   # Green
                (face_area[:, :, 0] < 140) &   # Blue
                (face_area[:, :, 2] < 140)     # Red

            )

            total_pixels = (
                face_area.shape[0] *
                face_area.shape[1]
            )

            green_ratio = green_pixels / total_pixels

            # Detect Open To Work badge

            if green_ratio > 0.03:

                open_to_work_detected = True

    # ==============================
    # PHOTO SCORE CALCULATION
    # ==============================

    score = 30

    # Face score

    if face_detected:
        score += 30

    else:
        score -= 20

    # Brightness score

    if brightness >= 150:
        score += 25

    elif brightness >= 100:
        score += 15

    elif brightness >= 70:
        score += 5

    # Resolution score

    height, width = gray.shape

    if width >= 500 and height >= 500:
        score += 15

    elif width >= 300:
        score += 10

    # ==============================
    # OPEN TO WORK PENALTY
    # ==============================

    if open_to_work_detected:

        score -= 35

    # ==============================
    # FINAL SCORE LIMIT
    # ==============================

    score = max(0, min(score, 100))

    # ==============================
    # RETURN RESULTS
    # ==============================

    return {

        "face_detected": face_detected,

        "brightness": round(brightness, 2),

        "photo_score": score,

        "open_to_work": open_to_work_detected,

        "green_ratio": round(green_ratio, 4)

    }
