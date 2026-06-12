from flask import Flask, jsonify



def create_app():
    app = Flask(__name__)

   

    #Global Error Handlers

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
