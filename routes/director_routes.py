import os
from flask import Blueprint, request, jsonify, current_app
from models.director import Director
from config import db

director_bp = Blueprint("director", __name__)

@director_bp.route("/director", methods=["POST"])
def create_director():
    name = request.form.get("name")
    position = request.form.get("position")
    desc = request.form.get("desc")
    image = request.files.get("image")

    filename = None
    if image:
        filename = image.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], filename)
        image.save(save_path)

    record = Director(name=name, position=position, desc=desc, image=filename)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "created", "id": record.id}), 201


@director_bp.route("/director", methods=["GET"])
def get_directors():
    data = Director.query.all()
    return jsonify([{
        "id": i.id,
        "name": i.name,
        "image": i.image,
        "position": i.position,
        "desc": i.desc
    } for i in data])


@director_bp.route("/director/<int:id>", methods=["PUT"])
def update_director(id):
    record = Director.query.get_or_404(id)
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


@director_bp.route("/director/<int:id>", methods=["DELETE"])
def delete_director(id):
    record = Director.query.get_or_404(id)

    if record.image:
        path = os.path.join(current_app.config["UPLOAD_FOLDER_IMAGES"], record.image)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "deleted"})
