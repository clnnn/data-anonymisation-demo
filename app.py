import streamlit as st

st.set_page_config(page_title="PII Analyzer and Anonymizer", page_icon="🔒")
st.sidebar.success("Select a demo from the sidebar to get started.")

st.title("PII Analyzer and Anonymizer")
st.markdown(
    """
            ## Intro
            This app demonstrates how to identify and anonymize personally identifiable information (PII) from different types of sources.
            
            ## How to Use
            Select a demo from the sidebar to get started. The demos include:
            
            #### Unstructured Text
            Analyze and anonymize PII in unstructured text. In this demo, you can input text that contains PII or select a predefined example. You are able to choose from different anonymization methods.
            
            #### Images
            Analyze and anonymize PII in images. In this demo, you can upload an image that contains PII and see the anonymized version.
            
            #### Live Video
            Analyze and anonymize PII in live video. In this demo, you can use your webcam to capture live video. The video will blur faces in real-time.
            
            ## Technologies
            - Python
            - Streamlit
            - Microsoft Presidio
            - OpenCV
            - MediaPipe
            """
)
