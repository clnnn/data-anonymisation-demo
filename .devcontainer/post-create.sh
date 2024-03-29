sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install python3-opencv
pip3 install --user -r requirements.txt
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
python -m spacy download en_core_web_lg