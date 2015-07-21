import os
from flask import Flask, make_response, request, redirect, render_template, url_for
from werkzeug import secure_filename
from pdf import extract_data

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello Zach!!"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['resume']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))  # app.config['']
            return str(extract_data(file))

    return render_template('form.html')


@app.route('/download', methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        response = make_response()
        response.headers['Content-Description'] = 'File Transfer'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Content-Disposition'] = 'attachment; filename=%s' % 'ZachWieandResume.pdf'
        response.headers['X-Accel-Redirect'] = UPLOAD_FOLDER
        return response
    
    return render_template('button.html')

if __name__ == '__main__':
        app.run()