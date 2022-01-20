""""
pip install -r requirements.txt
to run file
set FLASK_APP=app.py
flask run
"""

from flask import Flask, render_template, request
from PIL import Image

import pytesseract

UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def read_img(img):
    # pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
    # /app/.apt/usr/bin/tesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(Image.open(img))
    return(text)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template("index.html")
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', msg='1')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('index.html', msg='2')

        if file and allowed_file(file.filename):

            # call the OCR function on it
            extracted_text = read_img(file)

            # extract the text and display it
            return render_template('index.html',
                                   msg='true',
                                   extracted_text=extracted_text)


if __name__ == '__main__':
    app.run(debug=True)
