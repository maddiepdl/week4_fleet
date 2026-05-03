from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

driver = Blueprint("driver", __name__)

@driver.route("/")
def get_drivers():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
                        select * from fleet.driver
                """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify(rows)


@driver.route("/", methods=["POST"])
def create_driver():
    try:
        conn = get_connection()
        cur = conn.cursor()

        data = request.get_json()

        cur.execute("""
                    insert into fleet.driver
                    (name, license_type)
                    values 
                    (%s, %s)
            """, (data["name"], data["license_type"]))

        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Created"}), 201


@driver.route("/<int:id>", methods=["PUT"])
def update_driver(id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        data = request.get_json()

        cur.execute("""
                    update fleet.driver
                    set name = %s,
                        license_type = %s
                    where driver_id = %s
            """, (data["name"], data["license_type"], id))

        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"{e}"}), 500
    else:
        return jsonify({"message": "Object Updated"}), 201


@driver.route("/<int:id>", methods=["DELETE"])
def delete_driver(id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
                    delete from fleet.driver
                    where driver_id = %s
            """, (id, ))

        conn.commit()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Deleted"}), 201