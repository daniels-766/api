import os
from flask import Blueprint, request, jsonify, current_app
from models.report1 import Report1
from config import db

report1_bp = Blueprint("report1", __name__)

@report1_bp.route("/report-1", methods=["POST"])
def create_report():
    name = request.form.get("name")
    file = request.files.get("file")

    filename = None
    if file:
        filename = file.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(save_path)

    record = Report1(name=name, file=filename)
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "created", "id": record.id}), 201


@report1_bp.route("/report-1", methods=["GET"])
def get_reports():
    data = Report1.query.all()
    return jsonify([{"id": i.id, "name": i.name, "file": i.file} for i in data])


@report1_bp.route("/report-1/<int:id>", methods=["PUT"])
def update_report(id):
    record = Report1.query.get_or_404(id)
    name = request.form.get("name")
    file = request.files.get("file")

    if name:
        record.name = name

    if file:
        filename = file.filename
        save_path = os.path.join(current_app.config["UPLOAD_FOLDER_PDF"], filename)
        file.save(save_path)
        record.file = filename

    db.session.commit()
    return jsonify({"message": "updated"})


@report1_bp.route("/report-1/<int:id>", methods=["DELETE"])
def delete_report(id):
    record = Report1.query.get_or_404(id)

    if record.file:
        path = os.path.join(current_app.config["UPLOAD_FOLDER_PDF"], record.file)
        if os.path.exists(path):
            os.remove(path)

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "deleted"})
