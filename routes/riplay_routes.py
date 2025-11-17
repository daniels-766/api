from flask import Blueprint, request, jsonify, send_file
from models.riplay import Riplay
from config import db
from io import BytesIO

riplay_bp = Blueprint("riplay", __name__)

@riplay_bp.route("/riplay", methods=["GET"])
def get_riplays():
    data = Riplay.query.all()
    return jsonify([
        {"id": r.id, "name": r.name, "file_url": f"/api/riplay/{r.id}/file"}
        for r in data
    ])


@riplay_bp.route("/riplay", methods=["POST"])
def create_riplay():
    name = request.form.get("name")
    file = request.files.get("file")

    file_data = file.read() if file else None
    file_mime = file.mimetype if file else None

    r = Riplay(name=name, file=file_data, file_mime=file_mime)
    db.session.add(r)
    db.session.commit()

    return jsonify({"message": "created", "id": r.id}), 201


@riplay_bp.route("/riplay/<int:id>", methods=["GET"])
def get_riplay(id):
    r = Riplay.query.get_or_404(id)
    return jsonify({
        "id": r.id,
        "name": r.name,
        "file_url": f"/api/riplay/{r.id}/file"
    })


@riplay_bp.route("/riplay/<int:id>/file", methods=["GET"])
def get_riplay_file(id):
    r = Riplay.query.get_or_404(id)
    if not r.file:
        return jsonify({"error": "No file"}), 404

    return send_file(
        BytesIO(r.file),
        mimetype=r.file_mime,
        as_attachment=False,
        download_name=f"riplay_{id}.pdf"
    )


@riplay_bp.route("/riplay/<int:id>", methods=["PUT"])
def update_riplay(id):
    r = Riplay.query.get_or_404(id)

    name = request.form.get("name")
    file = request.files.get("file")

    if name:
        r.name = name
    if file:
        r.file = file.read()
        r.file_mime = file.mimetype

    db.session.commit()
    return jsonify({"message": "updated"})


@riplay_bp.route("/riplay/<int:id>", methods=["DELETE"])
def delete_riplay(id):
    r = Riplay.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"message": "deleted"})
