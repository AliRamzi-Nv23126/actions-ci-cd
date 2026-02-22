"""Flask ToDo Application."""
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory todo list for demo purposes
todos = [
    {"id": 1, "title": "Learn GitHub Actions", "completed": False},
    {"id": 2, "title": "Build CI/CD pipeline", "completed": False},
]


@app.route("/", methods=["GET"])
def index():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "ToDo API is running"})


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route("/todos", methods=["GET"])
def get_todos():
    """Get all todos."""
    return jsonify(todos), 200


@app.route("/todos", methods=["POST"])
def create_todo():
    """Create a new todo."""
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_todo = {
        "id": max([t["id"] for t in todos], default=0) + 1,
        "title": data["title"],
        "completed": data.get("completed", False),
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201


@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Update a todo."""
    data = request.get_json()
    todo = next((t for t in todos if t["id"] == todo_id), None)

    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    if "title" in data:
        todo["title"] = data["title"]
    if "completed" in data:
        todo["completed"] = data["completed"]

    return jsonify(todo), 200


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo."""
    global todos
    todo = next((t for t in todos if t["id"] == todo_id), None)

    if not todo:
        return jsonify({"error": "Todo not found"}), 404

    todos = [t for t in todos if t["id"] != todo_id]
    return "", 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
