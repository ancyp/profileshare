from flask import Flask, send_file, request, render_template, url_for
from flask_qrcode import QRcode

app = Flask(__name__)
qrcode = QRcode(app)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
