from flask import Flask, send_file, request, render_template, url_for, redirect, flash
import os
from werkzeug.utils import secure_filename

# for decode
from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image

from profileshare.models.models import SharedProfiles
from profileshare import app, db

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route('/')
def index():
    return render_template('sample_qr_application.html')


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get('data', '')
    return send_file(
        qrcode(data, mode='raw'),
        mimetype='image/png'
    )


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data = decode(Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)), symbols=[ZBarSymbol.QRCODE])
            # TODO lookup in DB & render profile page
            # request.form['username'] to extract
            profile = data[0].data
            return render_template('response.html', fb="pavankm", ig="pavanmutt", user=profile, uniqID=profile)
    return '', 204


@app.route('/test', methods=['GET'])
def testdb():
    c = db.session.query(SharedProfiles).all()
    for profile in c:
        print(profile)
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
