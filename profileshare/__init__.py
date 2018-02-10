from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_qrcode import QRcode

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# TODO
app.config['UPLOAD_FOLDER'] = '/home/pavan/profileshare'
qrcode = QRcode(app)
migrate = Migrate(app, db)
