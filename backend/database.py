import sqlite3

DATABASE = "triage.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        age INTEGER,

        heart_rate INTEGER,

        systolic_blood_pressure INTEGER,

        oxygen_saturation INTEGER,

        body_temperature REAL,

        pain_level INTEGER,

        chronic_disease_count INTEGER,

        previous_er_visits INTEGER,

        arrival_mode INTEGER,

        prediction INTEGER,

        priority TEXT,

        recommendation TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()


def insert_patient(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO patients(

        age,

        heart_rate,

        systolic_blood_pressure,

        oxygen_saturation,

        body_temperature,

        pain_level,

        chronic_disease_count,

        previous_er_visits,

        arrival_mode,

        prediction,

        priority,

        recommendation

    )

    VALUES(?,?,?,?,?,?,?,?,?,?,?,?)

    """,(

        data["age"],

        data["heart_rate"],

        data["systolic_blood_pressure"],

        data["oxygen_saturation"],

        data["body_temperature"],

        data["pain_level"],

        data["chronic_disease_count"],

        data["previous_er_visits"],

        data["arrival_mode"],

        data["prediction"],

        data["priority"],

        data["recommendation"]

    ))

    conn.commit()

    conn.close()


def get_all_patients():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM patients

    ORDER BY created_at DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def delete_patient(patient_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM patients WHERE id=?",

        (patient_id,)

    )

    conn.commit()

    conn.close()


def clear_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "DELETE FROM patients"

    )

    conn.commit()

    conn.close()