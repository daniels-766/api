from config import db

class Mitra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    image = db.Column(db.LargeBinary)
    image_mime = db.Column(db.String(100))
    link = db.Column(db.String(255))
    desc = db.Column(db.Text)
