import os
from flask import Blueprint, request, jsonify, current_app
from models.mitra import Mitra
from config import db

mitra_bp = Blueprint("mitra", __name__)

@mitra_bp.route("/mitra", methods=["POST"])
def create_mitra():
    name = request.form.get("name")
    link = request.form.get("link")
    desc = request.form.get("desc")
    image = request.files.get("image")

    filename = None
    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)

    record = Mitra(name=name, link=link, desc=desc, image=filename)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "created", "id": record.id}), 201


@mitra_bp.route("/mitra", methods=["GET"])
def get_all_mitra():
    data = Mitra.query.all()
    return jsonify([
        {"id": i.id, "name": i.name, "image": i.image, "link": i.link, "desc": i.desc}
        for i in data
    ])


@mitra_bp.route("/mitra/<int:id>", methods=["PUT"])
def update_mitra(id):
    record = Mitra.query.get_or_404(id)
    name = request.form.get("name")
    link = request.form.get("link")
    desc = request.form.get("desc")
    image = request.files.get("image")

    if name:
        record.name = name
    if link:
        record.link = link
    if desc:
        record.desc = desc

    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)
        record.image = filename

    db.session.commit()
    return jsonify({"message": "updated"})


@mitra_bp.route("/mitra/<int:id>", methods=["DELETE"])
def delete_mitra(id):
    record = Mitra.query.get_or_404(id)

    if record.image:
        path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], record.image)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "deleted"})
