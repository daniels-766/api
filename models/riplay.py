from config import db

class Riplay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    file = db.Column(db.String(255))  # PDF
