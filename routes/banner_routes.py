from flask import Blueprint, request, jsonify, send_file
from models.banner import Banner
from config import db
from io import BytesIO

banner_bp = Blueprint("banner", __name__)

@banner_bp.route("/banner", methods=["GET"])
def get_all_banner():
    data = Banner.query.all()
    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "image_url": f"/api/banner/{d.id}/image"
        }
        for d in data
    ])


@banner_bp.route("/banner", methods=["POST"])
def create_banner():
    name = request.form.get("name")
    image = request.files.get("image")

    image_data = image.read() if image else None
    image_mime = image.mimetype if image else None

    d = Banner(name=name, image=image_data, image_mime=image_mime)
    db.session.add(d)
    db.session.commit()

    return jsonify({"message": "created", "id": d.id}), 201


@banner_bp.route("/banner/<int:id>/image", methods=["GET"])
def get_banner_image(id):
    d = Banner.query.get_or_404(id)
    if not d.image:
        return jsonify({"error": "No image"}), 404

    return send_file(
        BytesIO(d.image),
        mimetype=d.image_mime,
        as_attachment=False
    )


@banner_bp.route("/banner/<int:id>", methods=["PUT"])
def update_banner(id):
    d = Banner.query.get_or_404(id)

    name = request.form.get("name")
    image = request.files.get("image")

    if name:
        d.name = name
    if image:
        d.image = image.read()
        d.image_mime = image.mimetype

    db.session.commit()
    return jsonify({"message": "updated"})


@banner_bp.route("/banner/<int:id>", methods=["DELETE"])
def delete_banner(id):
    d = Banner.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({"message": "deleted"})
