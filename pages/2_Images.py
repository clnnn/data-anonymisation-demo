import streamlit as st
from PIL import Image
from presidio_image_redactor import ImageRedactorEngine
from streamlit_image_comparison import image_comparison


st.set_page_config(page_title="Images", page_icon="🖼️")
st.title("Images")

# Upload an image
image_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Get the image to redact using PIL lib (pillow)
if image_file is None:
    st.text("Please upload an image")
else:
    image = Image.open(image_file)

    # Initialize the engine
    engine = ImageRedactorEngine()

    # Redact the image with pink color
    redacted_image = engine.redact(image, (255, 192, 203))

    # Compare the original image with the redacted image
    image_comparison(img1=image, img2=redacted_image)
