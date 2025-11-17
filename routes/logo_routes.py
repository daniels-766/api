import os
from flask import Blueprint, request, jsonify, current_app
from models.logo import Logo
from config import db

logo_bp = Blueprint("logo", __name__)

@logo_bp.route("/logo", methods=["POST"])
def create_logo():
    name = request.form.get("name")
    image = request.files.get("image")

    filename = None
    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)

    logo = Logo(name=name, image=filename)
    db.session.add(logo)
    db.session.commit()

    return jsonify({"message": "created", "id": logo.id}), 201


@logo_bp.route("/logo", methods=["GET"])
def get_logo_all():
    data = Logo.query.all()
    result = [{"id": i.id, "name": i.name, "image": i.image} for i in data]
    return jsonify(result)


@logo_bp.route("/logo/<int:id>", methods=["GET"])
def get_logo(id):
    i = Logo.query.get_or_404(id)
    return jsonify({"id": i.id, "name": i.name, "image": i.image})


@logo_bp.route("/logo/<int:id>", methods=["PUT"])
def update_logo(id):
    logo = Logo.query.get_or_404(id)
    name = request.form.get("name")
    image = request.files.get("image")

    if name:
        logo.name = name

    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)
        logo.image = filename

    db.session.commit()
    return jsonify({"message": "updated"})


@logo_bp.route("/logo/<int:id>", methods=["DELETE"])
def delete_logo(id):
    logo = Logo.query.get_or_404(id)

    if logo.image:
        path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], logo.image)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(logo)
    db.session.commit()
    return jsonify({"message": "deleted"})
