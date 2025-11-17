import yaml
import os
from flask import Blueprint, jsonify, request

swagger_dynamic = Blueprint("swagger_dynamic", __name__)

@swagger_dynamic.route("/swagger.json")
def swagger_json():

    base = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(base, "static", "swagger.yaml")

    try:
        with open(yaml_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    server_url = f"{request.scheme}://{request.host}/api"
    spec["servers"] = [{"url": server_url}]

    return jsonify(spec)
