from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db
from routes.driver import driver
from routes.vehicle import vehicle
from routes.route import route
from routes.package import package

init_db()

app=Flask(__name__, static_folder = "dist", static_url_path="")
CORS(app, origins="*")
app.register_blueprint(driver, url_prefix="/driver")
app.register_blueprint(vehicle, url_prefix="/vehicle")
app.register_blueprint(route, url_prefix="/route")
app.register_blueprint(package, url_prefix="/package")

@app.route("/")
@app.route("/<path:path>")
def serve_front_end():
    return app.send_static_file("index.html")

@app.route("/health")
def get_health():
    return jsonify({"message": "Server Online"}) , 200


if __name__ == "__main__":
    app.run(debug=True)