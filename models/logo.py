from config import db

class Logo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    image = db.Column(db.LargeBinary)  # BLOB
    image_mime = db.Column(db.String(255))  # MIME type
