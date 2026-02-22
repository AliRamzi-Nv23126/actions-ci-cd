"""Test suite for ToDo app."""


def test_app_import():
    """Test that the app can be imported."""
    from app import app

    assert app is not None


def test_app_responds():
    """Smoke test: app responds to a request."""
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        rv = client.get("/")
    assert rv.status_code == 200


def test_health_endpoint():
    """Test health check endpoint."""
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        rv = client.get("/health")
    assert rv.status_code == 200
    assert rv.get_json()["status"] == "healthy"


def test_get_todos():
    """Test getting todos."""
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        rv = client.get("/todos")
    assert rv.status_code == 200
    assert isinstance(rv.get_json(), list)


def test_create_todo():
    """Test creating a todo."""
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        rv = client.post("/todos", json={"title": "Test todo"})
    assert rv.status_code == 201
    todo = rv.get_json()
    assert todo["title"] == "Test todo"
    assert todo["completed"] is False


def test_create_todo_missing_title():
    """Test creating a todo without title."""
    from app import app

    app.config["TESTING"] = True
    with app.test_client() as client:
        rv = client.post("/todos", json={})
    assert rv.status_code == 400
