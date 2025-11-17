from flask import Blueprint, request, jsonify, send_file
from models.report1 import Report1
from config import db
from io import BytesIO

report1_bp = Blueprint("report1", __name__)

@report1_bp.route("/report-1", methods=["GET"])
def get_reports():
    data = Report1.query.all()
    return jsonify([
        {
            "id": r.id,
            "name": r.name,
            "file_url": f"/api/report-1/{r.id}/file"
        } for r in data
    ])


@report1_bp.route("/report-1", methods=["POST"])
def create_report():
    name = request.form.get("name")
    file = request.files.get("file")

    file_data = file.read() if file else None
    file_mime = file.mimetype if file else None

    r = Report1(name=name, file=file_data, file_mime=file_mime)
    db.session.add(r)
    db.session.commit()

    return jsonify({"message": "created", "id": r.id}), 201


@report1_bp.route("/report-1/<int:id>", methods=["GET"])
def get_report(id):
    r = Report1.query.get_or_404(id)
    return jsonify({
        "id": r.id,
        "name": r.name,
        "file_url": f"/api/report-1/{r.id}/file"
    })


@report1_bp.route("/report-1/<int:id>/file", methods=["GET"])
def get_report_file(id):
    r = Report1.query.get_or_404(id)
    if not r.file:
        return jsonify({"error": "No file"}), 404

    return send_file(
        BytesIO(r.file),
        mimetype=r.file_mime,
        as_attachment=False,
        download_name=f"report1_{id}.pdf"
    )


@report1_bp.route("/report-1/<int:id>", methods=["PUT"])
def update_report(id):
    r = Report1.query.get_or_404(id)

    name = request.form.get("name")
    file = request.files.get("file")

    if name:
        r.name = name
    if file:
        r.file = file.read()
        r.file_mime = file.mimetype

    db.session.commit()
    return jsonify({"message": "updated"})


@report1_bp.route("/report-1/<int:id>", methods=["DELETE"])
def delete_report(id):
    r = Report1.query.get_or_404(id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"message": "deleted"})
