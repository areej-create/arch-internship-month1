from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import time

app = Flask(__name__)
CORS(app)

DB = "todo.db"


# ── DB SETUP ──────────────────────────────────────────────────────────────────

def get_db():
    """Open a connection to the SQLite database."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row   # rows behave like dicts
    return conn


def init_db():
    """Create the tasks table if it doesn't exist yet."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                text      TEXT    NOT NULL,
                done      INTEGER NOT NULL DEFAULT 0,
                priority  TEXT    NOT NULL DEFAULT 'medium',
                created   INTEGER NOT NULL
            )
        """)
        conn.commit()


# ── HELPER ────────────────────────────────────────────────────────────────────

def row_to_dict(row):
    """Convert a sqlite3.Row to a plain Python dict."""
    return {
        "id":       row["id"],
        "text":     row["text"],
        "done":     bool(row["done"]),
        "priority": row["priority"],
        "created":  row["created"],
    }


# ── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Return all tasks, newest first."""
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks ORDER BY created DESC"
        ).fetchall()
    return jsonify([row_to_dict(r) for r in rows]), 200


@app.route("/tasks", methods=["POST"])
def add_task():
    """Add a new task. Expects JSON: { text, priority }"""
    data = request.get_json()

    # basic validation
    if not data or not data.get("text", "").strip():
        return jsonify({"error": "Task text is required"}), 400

    text     = data["text"].strip()
    priority = data.get("priority", "medium")
    created  = int(time.time() * 1000)   # ms timestamp

    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (text, done, priority, created) VALUES (?, 0, ?, ?)",
            (text, priority, created)
        )
        conn.commit()
        new_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()

    return jsonify(row_to_dict(row)), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Edit a task. Expects JSON: { text?, done?, priority? }"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    with get_db() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            return jsonify({"error": "Task not found"}), 404

        # only update fields that were sent
        text     = data.get("text",     row["text"]).strip()
        done     = int(data.get("done",     bool(row["done"])))
        priority = data.get("priority", row["priority"])

        conn.execute(
            "UPDATE tasks SET text = ?, done = ?, priority = ? WHERE id = ?",
            (text, done, priority, task_id)
        )
        conn.commit()
        updated = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

    return jsonify(row_to_dict(updated)), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Delete a task by ID."""
    with get_db() as conn:
        row = conn.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
        if not row:
            return jsonify({"error": "Task not found"}), 404

        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

    return jsonify({"message": f"Task {task_id} deleted"}), 200


@app.route("/tasks/clear-done", methods=["DELETE"])
def clear_done():
    """Delete all completed tasks at once."""
    with get_db() as conn:
        conn.execute("DELETE FROM tasks WHERE done = 1")
        conn.commit()
    return jsonify({"message": "Completed tasks cleared"}), 200


# ── RUN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    print("\n  Todo API running at http://localhost:5000")
    print("  Open frontend/index.html in your browser\n")
    app.run(debug=True, port=5000)
