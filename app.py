from flask import Flask, jsonify
from database.store import db
from routes.deal_routes import deals_bp


def create_app():
    app = Flask(__name__)

    # SQLite database config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///travel_deals.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    
    db.init_app(app)

    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()


    app.register_blueprint(deals_bp)

    # Global error handler
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Endpoint not found."}), 404

    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "message": "Method not allowed."}), 405

   
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"success": False, "message": "Internal server error."}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)