import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2


st.set_page_config(page_title="Live Video Face Annonimization", page_icon="📝")
st.title("Live Video Face Annonimization")

model_path = './blaze_face_short_range.tflite'
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)


def annonymize_faces(frame: av.VideoFrame):
    image = av.VideoFrame.to_image(frame.to_rgb())
    image_array = np.asarray(image, dtype=np.uint8)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_array)
    
    detection_result = detector.detect(mp_image)
    image_copy = np.copy(mp_image.numpy_view())
    for detection in detection_result.detections:
        bbox = detection.bounding_box
        x, y, w, h = int(bbox.origin_x), int(bbox.origin_y), int(bbox.width), int(bbox.height)
        face = image_copy[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face, (99, 99), 30)
        image_copy[y:y+h, x:x+w] = blurred_face
    return av.VideoFrame.from_ndarray(image_copy, format="rgb24")


webrtc = webrtc_streamer(key="streamer", sendback_audio=False, video_frame_callback=annonymize_faces,)
