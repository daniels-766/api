import os
from flask import Blueprint, request, jsonify, current_app
from models.shareholders import Shareholder
from config import db

shareholders_bp = Blueprint("shareholders", __name__)

@shareholders_bp.route("/shareholders", methods=["POST"])
def create_shareholder():
    name = request.form.get("name")
    position = request.form.get("position")
    desc = request.form.get("desc")
    image = request.files.get("image")

    filename = None
    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)

    record = Shareholder(name=name, position=position, desc=desc, image=filename)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "created", "id": record.id}), 201


@shareholders_bp.route("/shareholders", methods=["GET"])
def get_shareholders():
    data = Shareholder.query.all()
    return jsonify([{
        "id": i.id,
        "name": i.name,
        "image": i.image,
        "position": i.position,
        "desc": i.desc
    } for i in data])


@shareholders_bp.route("/shareholders/<int:id>", methods=["PUT"])
def update_shareholder(id):
    record = Shareholder.query.get_or_404(id)
    name = request.form.get("name")
    position = request.form.get("position")
    desc = request.form.get("desc")
    image = request.files.get("image")

    if name:
        record.name = name
    if position:
        record.position = position
    if desc:
        record.desc = desc

    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)
        record.image = filename

    db.session.commit()
    return jsonify({"message": "updated"})


@shareholders_bp.route("/shareholders/<int:id>", methods=["DELETE"])
def delete_shareholder(id):
    record = Shareholder.query.get_or_404(id)

    if record.image:
        path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], record.image)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "deleted"})
