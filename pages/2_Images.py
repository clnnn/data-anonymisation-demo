import streamlit as st
from streamlit_image_comparison import image_comparison

from PIL import Image
from presidio_image_redactor import ImageRedactorEngine


from ultralytics import YOLOWorld
from supervision import Detections, PixelateAnnotator


def annonymize_pii_text(image: Image.Image):
    # Initialize the engine for redacting text in images
    engine = ImageRedactorEngine()

    # Redact the image with pink color if the images contains PII in text format
    redacted_image = engine.redact(image, (255, 192, 203))

    return redacted_image


model = YOLOWorld()
annotator = PixelateAnnotator()


def annonymize_license_plate(image: Image.Image):
    model.set_classes(["license plate", ""])

    licence_plate_detection = Detections.from_ultralytics(
        model(image, conf=0.1)[0]
    ).with_nms(threshold=0.5, class_agnostic=True)

    return annotator.annotate(image, licence_plate_detection)


def annonymize_person(image: Image.Image):
    model.set_classes(["person"])
    person_detections = Detections.from_ultralytics(model(image)[0])
    redacted_image = annotator.annotate(image, person_detections)
    return redacted_image


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
    redacted_image = annonymize_pii_text(image)
    redacted_image = annonymize_license_plate(image)
    redacted_image = annonymize_person(redacted_image)

    # Compare the original image with the redacted image
    image_comparison(img1=image, img2=redacted_image)
