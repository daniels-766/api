from config import create_app, db
from routes.logo_routes import logo_bp
from routes.banner_routes import banner_bp
from routes.mitra_routes import mitra_bp
from routes.report1_routes import report1_bp
from routes.director_routes import director_bp
from routes.shareholders_routes import shareholders_bp
from routes.riplay_routes import riplay_bp
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

SWAGGER_URL = "/docs"
API_URL = "/static/swagger.yaml"
swagger_ui = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui, url_prefix=SWAGGER_URL)

app.register_blueprint(logo_bp, url_prefix="/api")
app.register_blueprint(banner_bp, url_prefix="/api")
app.register_blueprint(mitra_bp, url_prefix="/api")
app.register_blueprint(report1_bp, url_prefix="/api")
app.register_blueprint(director_bp, url_prefix="/api")
app.register_blueprint(shareholders_bp, url_prefix="/api")
app.register_blueprint(riplay_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, port=5003, host='0.0.0.0')
