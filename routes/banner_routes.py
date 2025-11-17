import os
from flask import Blueprint, request, jsonify, current_app
from models.banner import Banner
from config import db

banner_bp = Blueprint("banner", __name__)

@banner_bp.route("/banner", methods=["POST"])
def create_banner():
    name = request.form.get("name")
    image = request.files.get("image")

    filename = None
    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)

    record = Banner(name=name, image=filename)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "created", "id": record.id}), 201


@banner_bp.route("/banner", methods=["GET"])
def get_all():
    data = Banner.query.all()
    return jsonify([{"id": i.id, "name": i.name, "image": i.image} for i in data])


@banner_bp.route("/banner/<int:id>", methods=["PUT"])
def update_banner(id):
    record = Banner.query.get_or_404(id)
    name = request.form.get("name")
    image = request.files.get("image")

    if name:
        record.name = name
    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)
        record.image = filename

    db.session.commit()
    return jsonify({"message": "updated"})


@banner_bp.route("/banner/<int:id>", methods=["DELETE"])
def delete_banner(id):
    record = Banner.query.get_or_404(id)

    if record.image:
        path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], record.image)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "deleted"})
