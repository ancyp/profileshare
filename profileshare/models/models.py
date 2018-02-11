from profileshare import db


class SharedProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    sharedProfileId = db.Column(db.String(120), unique=True, nullable=False)
    # JSON
    urls = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.sharedProfileId)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    fb = db.Column(db.String(80), unique=False, nullable=True)
    ig = db.Column(db.String(80), unique=False, nullable=True)
    mail = db.Column(db.String(80), unique=False, nullable=True)
    phone = db.Column(db.String(80), unique=False, nullable=True)
