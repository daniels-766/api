from flask import Blueprint, request, jsonify, send_file
from models.director import Director
from config import db
from io import BytesIO

director_bp = Blueprint("director", __name__)

@director_bp.route("/director", methods=["GET"])
def get_directors():
    data = Director.query.all()
    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "position": d.position,
            "desc": d.desc,
            "image_url": f"/api/director/{d.id}/image"
        }
        for d in data
    ])


@director_bp.route("/director", methods=["POST"])
def create_director():
    name = request.form.get("name")
    position = request.form.get("position")
    desc = request.form.get("desc")
    image = request.files.get("image")

    image_data = image.read() if image else None
    image_mime = image.mimetype if image else None

    d = Director(
        name=name,
        position=position,
        desc=desc,
        image=image_data,
        image_mime=image_mime
    )
    db.session.add(d)
    db.session.commit()

    return jsonify({"message": "created", "id": d.id}), 201


@director_bp.route("/director/<int:id>", methods=["GET"])
def get_director(id):
    d = Director.query.get_or_404(id)
    return jsonify({
        "id": d.id,
        "name": d.name,
        "position": d.position,
        "desc": d.desc,
        "image_url": f"/api/director/{d.id}/image"
    })


@director_bp.route("/director/<int:id>/image", methods=["GET"])
def get_director_image(id):
    d = Director.query.get_or_404(id)
    if not d.image:
        return jsonify({"error": "No image"}), 404

    return send_file(
        BytesIO(d.image),
        mimetype=d.image_mime,
        as_attachment=False,
        download_name=f"director_{id}"
    )


@director_bp.route("/director/<int:id>", methods=["PUT"])
def update_director(id):
    d = Director.query.get_or_404(id)

    name = request.form.get("name")
    position = request.form.get("position")
    desc = request.form.get("desc")
    image = request.files.get("image")

    if name:
        d.name = name
    if position:
        d.position = position
    if desc:
        d.desc = desc
    if image:
        d.image = image.read()
        d.image_mime = image.mimetype

    db.session.commit()
    return jsonify({"message": "updated"})


@director_bp.route("/director/<int:id>", methods=["DELETE"])
def delete_director(id):
    d = Director.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({"message": "deleted"})
