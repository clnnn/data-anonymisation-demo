import streamlit as st
from streamlit_image_comparison import image_comparison

from PIL import Image
from presidio_image_redactor import ImageRedactorEngine


from ultralytics import YOLOWorld
from supervision import Detections, PixelateAnnotator


st.set_page_config(page_title="Images", page_icon="🖼️")
st.title("Images")

model = YOLOWorld()
annotator = PixelateAnnotator()

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

    # Detect license plates
    model.set_classes(["license_plate"])
    license_plate_detections = Detections.from_ultralytics(model(redacted_image)[0])

    model.set_classes(["license_plate", ""])
    license_plate_background_detections = Detections.from_ultralytics(
        model(redacted_image)[0]
    ).with_nms(0.1, class_agnostic=True)

    # Detect persons
    model.set_classes(["person"])
    person_detections = Detections.from_ultralytics(model(redacted_image)[0])

    # Combine the detections

    # Pixelate each face in the image
    redacted_image = annotator.annotate(redacted_image, license_plate_detections)
    redacted_image = annotator.annotate(
        redacted_image, license_plate_background_detections
    )
    redacted_image = annotator.annotate(redacted_image, person_detections)

    # Compare the original image with the redacted image
    image_comparison(img1=image, img2=redacted_image)
