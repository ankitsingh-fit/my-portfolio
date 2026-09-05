from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Ankit@1983",
    "database": "portfolio_db"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/api/ratings", methods=["GET"])
def get_ratings():

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT name, rating, feedback, created_at
        FROM ratings
        ORDER BY id DESC
    """)

    reviews = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) AS count,
               COALESCE(AVG(rating), 0) AS average
        FROM ratings
    """)

    result = cursor.fetchone()

    cursor.close()
    db.close()

    return jsonify({
        "count": result["count"],
        "average": float(result["average"]),
        "reviews": reviews
    })


@app.route("/api/ratings", methods=["POST"])
def add_rating():

    data = request.get_json()

    name = data.get("name", "").strip()
    rating = int(data.get("rating", 0))
    feedback = data.get("feedback", "").strip()

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if rating < 1 or rating > 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO ratings (name, rating, feedback)
        VALUES (%s, %s, %s)
        """,
        (name, rating, feedback)
    )

    db.commit()

    cursor.close()
    db.close()

    return jsonify({"message": "Rating saved successfully"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)