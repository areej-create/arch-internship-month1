# Todo App — Flask + SQLite + HTML/CSS/JS

A full-stack todo list application built with a Flask REST API backend
(SQLite storage) and a plain HTML/CSS/JavaScript frontend.

---

## Project Structure

```
todo-app/
├── backend/
│   ├── app.py            ← Flask REST API (all routes)
│   ├── todo.db           ← SQLite database (auto-created on first run)
│   └── requirements.txt  ← Python dependencies
│
└── frontend/
    └── index.html        ← Complete frontend (HTML + CSS + JS)
```

---

## How to Run

### Step 1 — Install Python dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Start the Flask server

```bash
python app.py
```

You should see:
```
Todo API running at http://localhost:5000
Open frontend/index.html in your browser
```

### Step 3 — Open the frontend

Just open `frontend/index.html` in your browser.
The green "Flask API connected" badge confirms the connection.

---

## API Endpoints

| Method | Route               | Description              |
|--------|---------------------|--------------------------|
| GET    | /tasks              | Get all tasks            |
| POST   | /tasks              | Add a new task           |
| PUT    | /tasks/<id>         | Edit a task              |
| DELETE | /tasks/<id>         | Delete a task            |
| DELETE | /tasks/clear-done   | Delete all done tasks    |

### Example POST body
```json
{ "text": "Buy groceries", "priority": "high" }
```

### Example PUT body
```json
{ "text": "Updated text", "done": true, "priority": "low" }
```

---

## Tech Stack

| Layer    | Technology                  |
|----------|-----------------------------|
| Backend  | Python, Flask, flask-cors   |
| Database | SQLite (built into Python)  |
| Frontend | HTML, CSS, JavaScript       |
| API style| REST (JSON)                 |

---

## Features

- Add tasks with priority (High / Medium / Low)
- Edit tasks inline
- Mark tasks as complete/incomplete
- Delete individual tasks
- Clear all completed tasks at once
- Filter by status or priority
- Live stats (total / pending / done)
- API connection status badge
- Toast notifications for all actions
