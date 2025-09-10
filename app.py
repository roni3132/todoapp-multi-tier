import os
import urllib.parse
from datetime import datetime
import psutil
import pymysql
from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

# -------------------
# Env vars (fallbacks included)
# -------------------
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = urllib.parse.quote_plus(os.getenv("DB_PASSWORD", ""))
DB_HOST = os.getenv("DB_SERVER", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_NAME = os.getenv("DB_NAME", "todo_db")

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

# -------------------
# Ensure DB exists
# -------------------
def ensure_database():
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=os.getenv("DB_PASSWORD", ""),
        port=DB_PORT,
        database="mysql",
    )
    cur = conn.cursor()
    cur.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
    if not cur.fetchone():
        cur.execute(
            f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
        print(f"✅ Database {DB_NAME} created")
    cur.close()
    conn.close()

ensure_database()
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# -------------------
# Flask app
# -------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# -------------------
# Models
# -------------------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="Pending")
    priority = db.Column(db.String(20), default="Low")
    created_at = db.Column(db.DateTime, default=datetime.now)
    completed_at = db.Column(db.DateTime, nullable=True)

with app.app_context():
    db.create_all()

# -------------------
# Helpers
# -------------------
def get_counts():
    return {
        "total": Task.query.count(),
        "pending": Task.query.filter_by(status="Pending").count(),
        "progress": Task.query.filter_by(status="In Progress").count(),
        "completed": Task.query.filter_by(status="Completed").count(),
    }

def get_health():
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
    }

# -------------------
# Routes
# -------------------
@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks, counts=get_counts(), **get_health())

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    priority = request.form.get("priority", "Low")
    if title:
        db.session.add(Task(title=title, priority=priority))
        db.session.commit()
    return redirect("/")

@app.route("/update_status/<int:task_id>", methods=["POST"])
def update_status(task_id):
    new_status = request.form.get("status")
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task.status = new_status
    if new_status == "Completed":
        task.completed_at = datetime.now()
    db.session.commit()
    return jsonify({"success": True, "counts": get_counts()})

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": True, "counts": get_counts()})

# -------------------
# Run
# -------------------
if __name__ == "__main__":
    print(f"🚀 Starting Flask app with DB {DB_NAME} on {DB_HOST}:{DB_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)
