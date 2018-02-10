from profileshare import db


class SharedProfiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    sharedProfileId = db.Column(db.String(120), unique=True, nullable=False)
    # TODO make this a JSON?
    urls = db.Column(db.String(200), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r %r>' % (self.username, self.sharedProfileId)
