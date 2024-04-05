import streamlit as st
from streamlit_image_comparison import image_comparison

from PIL import Image
from presidio_image_redactor import ImageRedactorEngine


from ultralytics import YOLO
from supervision import Detections, PixelateAnnotator


st.set_page_config(page_title="Images", page_icon="🖼️")
st.title("Images")

# Load the YOLOv5 model and the bounding box annotator
model = YOLO()
face_annotator = PixelateAnnotator()

# Upload an image
image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Get the image to redact using PIL lib (pillow)
if image_file is None:
    st.text("Please upload an image")
else:
    image = Image.open(image_file)

    # Initialize the engine for redacting text in images
    engine = ImageRedactorEngine()

    # Redact the image with pink color if the images contains PII in text format
    redacted_image = engine.redact(image, (255, 192, 203))

    # Detect faces in the image
    detections = Detections.from_ultralytics(model(redacted_image)[0])
    detections = detections[detections.class_id == 0]

    # Pixelate each face in the image
    redacted_image = face_annotator.annotate(redacted_image, detections)

    # Compare the original image with the redacted image
    image_comparison(img1=image, img2=redacted_image)
