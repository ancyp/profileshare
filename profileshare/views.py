from flask import Flask, send_file, request, render_template, url_for, redirect, flash
import os
from werkzeug.utils import secure_filename
import uuid
# for decode
import json
from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image
import pyqrcode
from profileshare.models.models import SharedProfile, User
from profileshare import app, db, qrcode

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# utility method
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# used to test QR code  - not part of app
@app.route('/qrcode', methods=['GET'])
def get_qrcode():
    # please get /qrcode?data=<qrcode_data>
    data = request.args.get('data', '')
    return send_file(
        qrcode(data, mode='raw'),
        mimetype='image/png'
    )


# upload QR code image and check response
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


# dummy method
@app.route('/test', methods=['GET'])
def testdb():
    c = db.session.query(SharedProfile).all()
    for profile in c:
        print(profile)
    return '', 204


# create a new user
@app.route('/newuser', methods=['GET'])
def newUser():
    return render_template('new_user.html')


# called when the form at /newuser is submitted
@app.route('/createuser', methods=['POST'])
def createUser():
    name = request.form.get("username")
    fb = request.form.get("fb", None)
    ig = request.form.get("ig", None)
    mail = request.form.get("mail", None)
    phone = request.form.get("phone", None)
    userobj = User(username=name, mail=mail, fb=fb, ig=ig, phone=phone)
    db.session.add(userobj)
    db.session.flush()
    db.session.commit()
    return render_template('create_user_success.html', user=userobj)


# show card details
@app.route('/card/<string:username>/<string:sharedProfileId>')
def displaycard(username, sharedProfileId):
    card = db.session.query(SharedProfile).filter(SharedProfile.sharedProfileId == sharedProfileId).all()[0]
    return render_template('response.html', user=username, uniqID=sharedProfileId, links=json.loads(card.urls))


# Enter valid username and select which profiles to shares
@app.route('/share')
def index():
    return render_template('create_qr.html')


# This is called when the form on /share is submitted
# Returns a QR code for the user & their profiles
@app.route('/create', methods=['POST'])
def createQr():
    name = request.form.get("username")
    # TODO include based on checkbox
    # TODO duplicate checks
    fb = request.form.get("fb", None)
    ig = request.form.get("ig", None)
    mail = request.form.get("mail", None)
    phone = request.form.get("phone", None)

    userProfile = db.session.query(User).filter(User.username == name).all()
    userProfile = userProfile[0]
    url = {
        'fb': userProfile.fb,
        'ig': userProfile.ig,
        'mail': userProfile.mail,
        'phone': userProfile.phone
    }
    shared = SharedProfile(username=userProfile.username, sharedProfileId=uuid.uuid4().hex, urls=json.dumps(url))
    db.session.add(shared)
    db.session.flush()
    db.session.commit()

    qr = pyqrcode.create("http://172.16.5.82:5000/card/" + shared.username + "/" + shared.sharedProfileId)
    qr.png("horn.png", scale=6)
    return send_file(
        'horn.png',
        mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
