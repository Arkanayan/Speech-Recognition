from flask import Flask, request, render_template, flash, redirect, send_file, abort
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['wav'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_mp3(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == 'mp3'

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        file_name = "sound_file"
        if file_name not in request.files:
            print("no file part")
            return redirect(request.url)
        file = request.files[file_name]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # if is_mp3(file):
            #     file = convert_mp3_to_wav(file)
            # File is accepted
            spec_img = generate_spec(file.filename)
            return render_template('index.html', spec_img=spec_img)
    
    return render_template('index.html')


def convert_mp3_to_wav(file):
    import pydub
    sound = pydub.AudioSegment.from_mp3("uploads/" + file.filename)
    output_filename = "uploads/" + file.filename + ".wav"
    if sound.export(output_filename, format="wav"):
        return output_filename
    