import psycopg2, os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),  # FIXED HERE
        sslmode=os.getenv("DB_SSLMODE")
    )

    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(""" 

                create table if not exists fleet.driver (
                    driver_id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    license_type VARCHAR(50)
                );

                create table if not exists fleet.vehicle (
                    vehicle_id SERIAL PRIMARY KEY,
                    license_plate VARCHAR(20),
                    model VARCHAR(100),
                    driver_id INT UNIQUE REFERENCES fleet.driver(driver_id)
                );

                create table if not exists fleet.route (
                    route_id SERIAL PRIMARY KEY,
                    date DATE,
                    service_zone VARCHAR(100),
                    driver_id INT REFERENCES fleet.driver(driver_id)
                );

                create table if not exists fleet.package (
                    package_id SERIAL PRIMARY KEY,
                    description TEXT,
                    weight DECIMAL,
                    route_id INT REFERENCES fleet.route(route_id)
                );

        """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database Ready!")