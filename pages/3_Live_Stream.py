import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av


st.set_page_config(page_title="Live Stream", page_icon="🎥")
st.title("Live Stream")

from ultralytics import YOLO
from supervision import Detections, PixelateAnnotator

model = YOLO()
face_annotator = PixelateAnnotator(pixel_size=20)


def annonymize_faces(frame: av.VideoFrame):
    image = av.VideoFrame.to_image(frame.to_rgb())
    detections = Detections.from_ultralytics(model(image)[0])
    detections = detections[detections.class_id == 0]
    redacted_image = face_annotator.annotate(image.copy(), detections)
    return av.VideoFrame.from_image(redacted_image)


webrtc = webrtc_streamer(
    key="streamer",
    sendback_audio=False,
    async_processing=True,
    video_frame_callback=annonymize_faces,
)

st.info(
    "This demo uses your webcam to capture live video. The video will pixelate faces in real-time."
)
