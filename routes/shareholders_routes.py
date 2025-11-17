from flask import Blueprint, request, jsonify, send_file
from models.shareholders import Shareholder
from config import db
from io import BytesIO

shareholders_bp = Blueprint("shareholders", __name__)

@shareholders_bp.route("/shareholders", methods=["GET"])
def get_shareholders():
    data = Shareholder.query.all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "position": s.position,
            "desc": s.desc,
            "image_url": f"/api/shareholders/{s.id}/image"
        } for s in data
    ])


@shareholders_bp.route("/shareholders", methods=["POST"])
def create_shareholder():
    name = request.form.get("name")
    position = request.form.get("position")
    desc = request.form.get("desc")
    image = request.files.get("image")

    image_data = image.read() if image else None
    image_mime = image.mimetype if image else None

    s = Shareholder(
        name=name,
        position=position,
        desc=desc,
        image=image_data,
        image_mime=image_mime
    )
    db.session.add(s)
    db.session.commit()

    return jsonify({"message": "created", "id": s.id}), 201


@shareholders_bp.route("/shareholders/<int:id>", methods=["GET"])
def get_shareholder(id):
    s = Shareholder.query.get_or_404(id)
    return jsonify({
        "id": s.id,
        "name": s.name,
        "position": s.position,
        "desc": s.desc,
        "image_url": f"/api/shareholders/{s.id}/image"
    })


@shareholders_bp.route("/shareholders/<int:id>/image", methods=["GET"])
def get_shareholder_image(id):
    s = Shareholder.query.get_or_404(id)
    if not s.image:
        return jsonify({"error": "No image"}), 404

    return send_file(
        BytesIO(s.image),
        mimetype=s.image_mime,
        as_attachment=False,
        download_name=f"shareholder_{id}"
    )


@shareholders_bp.route("/shareholders/<int:id>", methods=["PUT"])
def update_shareholder(id):
    s = Shareholder.query.get_or_404(id)

    name = request.form.get("name")
    position = request.form.get("position")
    desc = request.form.get("desc")
    image = request.files.get("image")

    if name:
        s.name = name
    if position:
        s.position = position
    if desc:
        s.desc = desc
    if image:
        s.image = image.read()
        s.image_mime = image.mimetype

    db.session.commit()
    return jsonify({"message": "updated"})


@shareholders_bp.route("/shareholders/<int:id>", methods=["DELETE"])
def delete_shareholder(id):
    s = Shareholder.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"message": "deleted"})
