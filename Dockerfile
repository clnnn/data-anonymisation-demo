FROM mcr.microsoft.com/devcontainers/python:1-3.8-bullseye as prod

RUN sudo apt-get update
RUN sudo apt-get install -y tesseract-ocr
RUN sudo apt-get install -y python3-opencv

RUN pip install --user spacy

RUN python -m spacy download en_core_web_sm

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY . .

ENTRYPOINT ["streamlit", "run", "Home.py"]