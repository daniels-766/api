from flask import Blueprint, request, jsonify, send_file
from models.logo import Logo
from config import db
from io import BytesIO

logo_bp = Blueprint("logo", __name__)

@logo_bp.route("/logo", methods=["GET"])
def get_logos():
    data = Logo.query.all()
    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "image_url": f"/api/logo/{d.id}/image"
        }
        for d in data
    ])


@logo_bp.route("/logo", methods=["POST"])
def create_logo():
    name = request.form.get("name")
    image = request.files.get("image")

    image_data = image.read() if image else None
    image_mime = image.mimetype if image else None

    record = Logo(name=name, image=image_data, image_mime=image_mime)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "created", "id": record.id}), 201


@logo_bp.route("/logo/<int:id>", methods=["GET"])
def get_logo(id):
    d = Logo.query.get_or_404(id)
    return jsonify({
        "id": d.id,
        "name": d.name,
        "image_url": f"/api/logo/{id}/image"
    })


@logo_bp.route("/logo/<int:id>/image", methods=["GET"])
def get_logo_image(id):
    d = Logo.query.get_or_404(id)
    if not d.image:
        return jsonify({"error": "No image"}), 404

    return send_file(
        BytesIO(d.image),
        mimetype=d.image_mime,
        as_attachment=False
    )


@logo_bp.route("/logo/<int:id>", methods=["PUT"])
def update_logo(id):
    d = Logo.query.get_or_404(id)
    name = request.form.get("name")
    image = request.files.get("image")

    if name:
        d.name = name
    if image:
        d.image = image.read()
        d.image_mime = image.mimetype

    db.session.commit()
    return jsonify({"message": "updated"})


@logo_bp.route("/logo/<int:id>", methods=["DELETE"])
def delete_logo(id):
    d = Logo.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({"message": "deleted"})
