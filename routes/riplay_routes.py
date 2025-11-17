import os
from flask import Blueprint, request, jsonify, current_app
from models.riplay import Riplay
from config import db

riplay_bp = Blueprint("riplay", __name__)

@riplay_bp.route("/riplay", methods=["POST"])
def create_riplay():
    name = request.form.get("name")
    file = request.files.get("file")

    filename = None
    if file:
        filename = file.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(save_path)

    record = Riplay(name=name, file=filename)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "created", "id": record.id}), 201


@riplay_bp.route("/riplay", methods=["GET"])
def get_all():
    data = Riplay.query.all()
    return jsonify([{"id": i.id, "name": i.name, "file": i.file} for i in data])


@riplay_bp.route("/riplay/<int:id>", methods=["PUT"])
def update_riplay(id):
    record = Riplay.query.get_or_404(id)
    name = request.form.get("name")
    file = request.files.get("file")

    if name:
        record.name = name
    if file:
        filename = file.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(save_path)
        record.file = filename

    db.session.commit()
    return jsonify({"message": "updated"})


@riplay_bp.route("/riplay/<int:id>", methods=["DELETE"])
def delete_riplay(id):
    record = Riplay.query.get_or_404(id)

    if record.file:
        path = os.path.join(current_app.config["UPLOAD_FOLDER_PDF"], record.file)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "deleted"})
