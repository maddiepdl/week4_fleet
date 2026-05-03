from flask import jsonify, request, Blueprint
from psycopg2.extras import RealDictCursor
from database import get_connection

package = Blueprint("package", __name__)

@package.route("/")
def get_packages():
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
                        select * from fleet.package
                """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify(rows)

@package.route("/", methods=["POST"])
def create_package():
    try:
        conn = get_connection()
        cur = conn.cursor()

        data = request.get_json()

        cur.execute("""
                    insert into fleet.package
                    (description, weight, route_id)
                    values 
                    (%s, %s, %s)
            """, (data["description"], data["weight"], data["route_id"]))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Created"}), 201

@package.route("/<int:id>", methods=["PUT"])
def update_package(id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        data = request.get_json()

        cur.execute("""
                    update fleet.package
                    set description = %s,
                        weight = %s,
                        route_id = %s
                    where package_id = %s
            """, (data["description"], data["weight"], data["route_id"], id))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"{e}"}), 500
    else:
        return jsonify({"message": "Object Updated"}), 201


@package.route("/<int:id>", methods=["DELETE"])
def delete_package(id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
                    delete from fleet.package
                    where package_id = %s
            """, (id, ))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        return jsonify({"message": f"An unexpected error occurred: {e}"}), 500
    else:
        return jsonify({"message": "Object Deleted"}), 201