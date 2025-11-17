from config import db

class Report1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    file = db.Column(db.LargeBinary)
    file_mime = db.Column(db.String(255))
