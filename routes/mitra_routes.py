from flask import Blueprint, request, jsonify, send_file
from models.mitra import Mitra
from config import db
from io import BytesIO

mitra_bp = Blueprint("mitra", __name__)

@mitra_bp.route("/mitra", methods=["GET"])
def get_all_mitra():
    data = Mitra.query.all()
    return jsonify([
        {
            "id": d.id,
            "name": d.name,
            "link": d.link,
            "desc": d.desc,
            "image_url": f"/api/mitra/{d.id}/image"
        }
        for d in data
    ])


@mitra_bp.route("/mitra", methods=["POST"])
def create_mitra():
    name = request.form.get("name")
    link = request.form.get("link")
    desc = request.form.get("desc")
    image = request.files.get("image")

    image_data = image.read() if image else None
    image_mime = image.mimetype if image else None

    d = Mitra(
        name=name,
        link=link,
        desc=desc,
        image=image_data,
        image_mime=image_mime
    )
    db.session.add(d)
    db.session.commit()

    return jsonify({"message": "created", "id": d.id}), 201


@mitra_bp.route("/mitra/<int:id>/image", methods=["GET"])
def get_mitra_image(id):
    d = Mitra.query.get_or_404(id)
    if not d.image:
        return jsonify({"error": "No image"}), 404

    return send_file(
        BytesIO(d.image),
        mimetype=d.image_mime,
        as_attachment=False
    )


@mitra_bp.route("/mitra/<int:id>", methods=["PUT"])
def update_mitra(id):
    d = Mitra.query.get_or_404(id)

    name = request.form.get("name")
    link = request.form.get("link")
    desc = request.form.get("desc")
    image = request.files.get("image")

    if name: d.name = name
    if link: d.link = link
    if desc: d.desc = desc
    if image:
        d.image = image.read()
        d.image_mime = image.mimetype

    db.session.commit()
    return jsonify({"message": "updated"})


@mitra_bp.route("/mitra/<int:id>", methods=["DELETE"])
def delete_mitra(id):
    d = Mitra.query.get_or_404(id)
    db.session.delete(d)
    db.session.commit()
    return jsonify({"message": "deleted"})
