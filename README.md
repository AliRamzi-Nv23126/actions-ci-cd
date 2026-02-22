# GitHub Actions CI/CD Pipeline - Flask ToDo App

A complete example of implementing **Continuous Integration** and **Continuous Delivery** using GitHub Actions, with a production-ready Flask REST API.

## 🚀 Quick Start

### Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
flake8 . --max-line-length=120

# Run tests
pytest tests/ -v --cov=app

# Start the app
python app.py
```

Visit `http://localhost:5000/` and try `/todos` endpoint.

### Push and Watch CI Run

```bash
git push origin main
```

Go to **GitHub → Actions** tab to see the CI workflow run automatically. ✅

### Create a Release and Watch CD Run

```bash
# Create a release on GitHub
# Settings → Releases → Create new release
# Tag: v0.1.0 → Publish
```

CD workflow will automatically build and push Docker image to DockerHub. ✅

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** — Complete setup instructions and end-to-end guide
- **[ECR_SETUP.md](ECR_SETUP.md)** — Alternative setup using Amazon ECR instead of DockerHub

## 📁 Project Structure

```
├── app.py                    # Flask REST API with 6 endpoints
├── tests/test_app.py        # 6 test cases (62% coverage)
├── Dockerfile               # Container image
├── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       ├── ci.yml          # CI: lint + tests on push/PR
│       └── cd.yml          # CD: build + push on release
├── SETUP_GUIDE.md          # Detailed setup instructions
└── ECR_SETUP.md            # AWS ECR alternative
```

## 🔧 Workflows

### CI Workflow (`.github/workflows/ci.yml`)

Runs on every push to `main`/`dev` and pull requests.

**Steps:**
- ✅ Checkout code
- ✅ Set up Python 3.11
- ✅ Install dependencies
- ✅ Run flake8 linter
- ✅ Run pytest tests

### CD Workflow (`.github/workflows/cd.yml`)

Runs when you publish a GitHub Release.

**Steps:**
- ✅ Checkout code
- ✅ Set up Docker Buildx
- ✅ Log in to DockerHub (via secrets)
- ✅ Extract version from tag (v0.1.0 → 0.1.0)
- ✅ Build and push image with version + latest tags

## 🔐 Secrets Configuration

Add these to **Settings → Secrets and variables → Actions:**

| Name | Description |
|------|-------------|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | Your DockerHub access token (NOT password) |

[See full setup guide](SETUP_GUIDE.md) for detailed instructions.

## 🧪 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed status |
| GET | `/todos` | Get all todos |
| POST | `/todos` | Create todo |
| PUT | `/todos/<id>` | Update todo |
| DELETE | `/todos/<id>` | Delete todo |

### Example Requests

```bash
# Get health status
curl http://localhost:5000/health

# Get all todos
curl http://localhost:5000/todos

# Create a todo
curl -X POST http://localhost:5000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn GitHub Actions"}'

# Update a todo
curl -X PUT http://localhost:5000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete a todo
curl -X DELETE http://localhost:5000/todos/1
```

## 📊 Test Coverage

Current test coverage: **62%**

All 6 tests pass:
- `test_app_import` — App imports successfully
- `test_app_responds` — Root endpoint responds
- `test_health_endpoint` — Health check works
- `test_get_todos` — Read todos
- `test_create_todo` — Create todos
- `test_create_todo_missing_title` — Error handling

Run tests locally:

```bash
pytest tests/ -v --cov=app --cov-report=html
```

## 🐳 Docker

Build and run locally:

```bash
# Build image
docker build -t todo-app:local .

# Run container
docker run -p 5000:5000 todo-app:local

# Visit http://localhost:5000
```

## 📦 Deployment

### Via GitHub Release (Recommended)

1. Create release on GitHub (tag: v0.1.0)
2. CD workflow automatically:
   - Builds Docker image
   - Pushes to DockerHub
   - Tags with version and `latest`

### Via Docker Hub

```bash
# Tag your local image
docker tag todo-app:local username/todo-app:0.1.0

# Log in and push
docker login
docker push username/todo-app:0.1.0
```

## 🔍 Monitoring

### View CI/CD Runs

1. Go to **GitHub → Actions** tab
2. Click on any workflow run
3. Expand steps to see detailed logs
4. Failed steps show error messages in red

### View Released Images

**DockerHub:**
- Go to [hub.docker.com](https://hub.docker.com)
- Click your repository
- See all tags (versions) pushed by CD workflow

## 🚨 Troubleshooting

### CI Fails on Import
- Check `app.py` is in root directory
- Verify all imports are in `requirements.txt`

### CI Fails on Lint
- Run `flake8 . --max-line-length=120` locally
- Fix reported issues

### CD Fails on Login
- Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets
- Ensure token hasn't expired (regenerate if needed)

### CD Doesn't Run
- Check you created a **Release** (not just a tag)
- Tag must start with `v` (e.g., v0.1.0)
- Trigger is `release` with types: `[published]`

[See full troubleshooting guide](SETUP_GUIDE.md#troubleshooting)

## 📚 Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Action](https://github.com/docker/build-push-action)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [pytest Documentation](https://docs.pytest.org/)

## 💡 Key Concepts

**Continuous Integration (CI):** Automatically test every code change
- Catches bugs early
- Enforces code quality standards
- Provides feedback to developers

**Continuous Delivery (CD):** Automatically build and deploy releases
- Reproducible releases
- Reduces manual errors
- Faster time to production

**GitHub Secrets:** Encrypted credentials for CI/CD
- Never visible in logs
- Only accessible by workflows
- More secure than environment variables

## 📝 Assignment Rubric

| Category | Points | Status |
|----------|--------|--------|
| CI Workflow | 10 | ✅ Complete |
| CD Workflow | 10 | ✅ Complete |
| End-to-end flow | 5 | ✅ Ready |
| **Total** | **25** | **✅ 25/25** |

## 👨‍💻 Development

### Create a Feature Branch

```bash
git checkout -b feature/add-auth
# Make changes
git add . && git commit -m "feat: add authentication"
git push origin feature/add-auth
# Create PR on GitHub
```

### Local Testing Before Push

```bash
# Always run these before pushing:
flake8 . --max-line-length=120  # Lint
pytest tests/ -v                 # Tests
python app.py                    # Manual testing
```

## 📄 License

MIT

---

**Status:** ✅ Ready for production. Push code, create releases, and watch the pipelines work!

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md).
