from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db
from routes.driver import driver
from routes.vehicle import vehicle
from routes.route import route
from routes.package import package

init_db()

app = Flask(__name__)
CORS(app, origins="*")
app.register_blueprint(driver, url_prefix="/driver")
app.register_blueprint(vehicle, url_prefix="/vehicle")
app.register_blueprint(route, url_prefix="/route")
app.register_blueprint(package, url_prefix="/package")

@app.route("/")
def home():
    return jsonify({"message": "Server Online"})

if __name__ == "__main__":
    app.run(debug=True)