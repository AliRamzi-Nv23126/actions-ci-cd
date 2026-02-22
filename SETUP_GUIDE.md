# GitHub Actions CI/CD Pipeline Setup Guide

This repository includes a complete Flask ToDo app with automated CI/CD pipelines using GitHub Actions.

## What's Been Set Up

### Project Structure
```
.
├── app.py                      # Flask application with 6 REST API endpoints
├── requirements.txt            # Python dependencies (Flask, pytest, flake8)
├── Dockerfile                  # Container image configuration
├── tests/
│   ├── __init__.py            # Tests package
│   └── test_app.py            # 6 test cases (100% endpoint coverage)
├── .github/
│   └── workflows/
│       ├── ci.yml             # Continuous Integration workflow
│       └── cd.yml             # Continuous Delivery workflow
└── README.md
```

### Flask API Endpoints

The app includes a fully functional REST API for managing todos:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health status |
| GET | `/todos` | Get all todos |
| POST | `/todos` | Create a new todo |
| PUT | `/todos/<id>` | Update a todo |
| DELETE | `/todos/<id>` | Delete a todo |

### CI Workflow (`.github/workflows/ci.yml`)

**Triggers:** Every push to `main` or `dev` branches, and all pull requests

**Steps:**
1. ✅ Checkout code (actions/checkout@v4)
2. ✅ Set up Python 3.11 (actions/setup-python@v5)
3. ✅ Install dependencies (pip install -r requirements.txt)
4. ✅ Run lint checks (flake8 with max-line-length=120)
5. ✅ Run tests (pytest with coverage reporting)

**Status Indicators:**
- Green check mark ✅ = All tests and lint passed
- Red "X" ❌ = Build failed (lint error or test failure)

### CD Workflow (`.github/workflows/cd.yml`)

**Triggers:** When a GitHub Release is published with type `[published]`

**Steps:**
1. ✅ Checkout code
2. ✅ Set up Docker Buildx
3. ✅ Log in to DockerHub (using secrets)
4. ✅ Extract version from git tag (v0.1.0 → 0.1.0)
5. ✅ Build and push Docker image with version tags

**Example Release Workflow:**
- Create release `v0.2.0` → CD workflow automatically:
  - Builds image: `yourname/todo-app:0.2.0`
  - Also tags: `yourname/todo-app:latest`

---

## Setup Instructions

### Step 1: Create DockerHub Account (if needed)

1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up for a free account
3. Create access token:
   - Account Settings → Security → New Access Token
   - Name it something like `github-actions-token`
   - Copy the token (you won't be able to see it again)

### Step 2: Add GitHub Secrets

Go to your repository settings on GitHub:

1. **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. Add the following secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `DOCKERHUB_USERNAME` | Your DockerHub username | Required for pushing images |
| `DOCKERHUB_TOKEN` | Your DockerHub access token | Access token (NOT your password) |

⚠️ **IMPORTANT:** These secrets are:
- Encrypted by GitHub
- NOT visible in logs or other parts of the UI
- Only accessible by the workflows
- Never commit tokens to your repository

### Step 3: Test the CI Workflow

The CI workflow runs automatically when you push code. To verify it works:

#### Test 1: Successful CI Run
```bash
git push origin main
```
Then check:
1. Go to GitHub repo → **Actions** tab
2. You should see a workflow run named "CI"
3. It should show a green ✅ check mark
4. Click it to see the detailed logs (checkout → setup Python → lint → tests)

#### Test 2: Failed CI Run (then fix it)
1. Introduce a linting error in `app.py`:
   ```python
   x=1  # No spaces around = will trigger flake8
   ```
2. Push the change: `git add . && git commit -m "test: lint error" && git push origin main`
3. Watch the workflow fail (red ❌)
4. Fix the error: `x = 1`
5. Push fix: `git add . && git commit -m "fix: lint error" && git push origin main`
6. Verify it passes again (green ✅)

---

## Step 4: Test the CD Workflow

### Create a GitHub Release

1. Go to your GitHub repo → **Releases** (right panel)
2. Click **"Create a new release"**
3. Fill in:
   - **Tag version:** `v0.1.0` (must start with `v`)
   - **Release title:** `version 0.1.0`
   - **Description:** "Initial release of ToDo API"
4. Click **"Publish release"**

### Verify CD Workflow

1. Go to **Actions** tab
2. You should see "CD" workflow running
3. Wait for it to complete (green ✅)
4. Check DockerHub to confirm image was pushed:
   - Go to [hub.docker.com](https://hub.docker.com)
   - Click your repository (`todo-app`)
   - You should see:
     - Tag: `0.1.0` (extracted from v0.1.0)
     - Tag: `latest` (always points to newest)

---

## Complete End-to-End Flow

Follow these steps to demonstrate the full CI/CD pipeline:

### 1. Make a Code Change
```bash
# On dev branch, make a small improvement
git checkout dev
echo "# Enhanced ToDo API" >> app.py
git add . && git commit -m "docs: update app description" && git push origin dev
```

### 2. Verify CI Passes on Dev
- Go to **Actions** tab
- Confirm CI workflow ran and passed ✅

### 3. Create Pull Request
- Go to GitHub repo → **Pull requests** → **New pull request**
- Select `dev` → `main`
- Add title and description
- Click **Create pull request**
- Verify CI runs on the PR (required before merge)

### 4. Merge Pull Request
- Click **"Merge pull request"**
- CI runs again on main (should pass ✅)

### 5. Create Release
- Go to **Releases** → **Create a new release**
- Tag: `v0.2.0`
- Title: `version 0.2.0`
- Description: "Feature complete version"
- Publish release

### 6. Verify CD Pipeline
- Go to **Actions** tab
- Watch "CD" workflow run
- Image is built and pushed to DockerHub
- Check [hub.docker.com](https://hub.docker.com) for new tag `0.2.0`

---

## Troubleshooting

### CI Workflow Issues

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError: No module named 'app'" | Ensure `app.py` is in root directory; check PYTHONPATH |
| Flake8 errors in logs | Run `flake8 . --max-line-length=120` locally to see issues first |
| Tests failing | Run `pytest tests/ -v` locally to debug |
| Import errors | Check that all dependencies are in `requirements.txt` |

### CD Workflow Issues

| Problem | Solution |
|---------|----------|
| "Credentials invalid" | Check secrets in Settings → Secrets; verify DockerHub token isn't expired |
| Wrong image tag | Ensure release tag is `v0.1.0` format; workflow extracts `0.1.0` from it |
| Workflow doesn't run | Use GitHub UI to create Release (not just a git tag); must use Release with type `[published]` |
| Image not in DockerHub | Check workflow logs; verify `DOCKERHUB_USERNAME` matches your account |

### View Workflow Logs

1. Go to **Actions** tab
2. Click on the workflow run
3. Click on the job (e.g., "test" or "build-push")
4. Expand each step to see detailed output
5. Look for error messages in red

---

## Key Learnings: GitHub Actions & Automation

### Why CI/CD Matters
- **Consistency**: Same steps every time, reducing human error
- **Speed**: Automated testing catches bugs early
- **Safety**: CD requires CI to pass before deploying
- **Confidence**: Automated releases are reproducible

### GitHub Actions Concepts

**Workflows**: YAML files in `.github/workflows/` that define automation
- Triggered by events (push, pull_request, release, etc.)
- Run on GitHub's servers (or self-hosted)

**Jobs**: Units of work in a workflow
- Each job runs on a fresh virtual machine
- Jobs can run in parallel or sequential

**Steps**: Individual command/action in a job
- Can run shell commands or reusable actions
- Actions are pre-built tools (e.g., checkout@v4, setup-python@v5)

**Secrets**: Encrypted credentials not visible in logs
- Used for DockerHub tokens, AWS keys, etc.
- Accessed via `${{ secrets.NAME }}`

**Contexts**: Information available during workflow
- `github.ref` = Git ref (e.g., `refs/tags/v0.1.0`)
- `github.event` = Event that triggered workflow

### Best Practices

1. ✅ **Always use Secrets for credentials** — never hardcode tokens/passwords
2. ✅ **Require CI to pass before merge** — GitHub Setting: Require status checks
3. ✅ **Version your releases with semantic versioning** — v0.1.0 format
4. ✅ **Tag Docker images** — include version and `latest`
5. ✅ **Test locally before pushing** — use same commands as CI
6. ✅ **Use clear commit messages** — explains what changed and why

---

## Next Steps

### Optional Enhancements

1. **Require status checks before merge:**
   - Settings → Branches → Add rule → Require CI to pass

2. **Add more tests:**
   - Increase coverage above 62% (currently at app.py)
   - Add integration tests

3. **Add ECR support instead of DockerHub:**
   - Replace DockerHub steps with ECR login
   - Use AWS credentials instead

4. **Slack/Email notifications:**
   - Add step to notify on workflow completion
   - Use community actions like `slackapi/slack-github-action`

5. **Auto-tag releases:**
   - Use `softprops/action-gh-release` for automated tagging

---

## Commands Reference

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run linting
flake8 . --max-line-length=120

# Run tests
pytest tests/ -v --cov=app

# Run the app locally
python app.py        # Runs on http://localhost:5000

# Test API endpoints
curl http://localhost:5000/health
curl http://localhost:5000/todos
```

### Docker
```bash
# Build image locally
docker build -t todo-app:local .

# Run container
docker run -p 5000:5000 todo-app:local

# Push to DockerHub (if logged in)
docker tag todo-app:local username/todo-app:0.1.0
docker push username/todo-app:0.1.0
```

### Git + GitHub
```bash
# Create and checkout dev branch
git checkout -b dev

# Create feature branch
git checkout -b feature/add-auth

# Push branch
git push origin feature/add-auth

# Create release (via GitHub UI - more reliable)
# Settings → Releases → Create new release
```

---

## File Descriptions

### [app.py](app.py)
Main Flask application with 6 REST API endpoints for CRUD operations on todos.
- Lines 1-7: Imports and app setup
- Lines 10-13: In-memory todo store
- Lines 16-71: Route handlers for todo operations

### [tests/test_app.py](tests/test_app.py)
Comprehensive test suite with 6 test cases:
- `test_app_import`: Verifies app can be imported
- `test_app_responds`: Smoke test for basic endpoint
- `test_health_endpoint`: Tests health check
- `test_get_todos`: Tests retrieval of todos
- `test_create_todo`: Tests creating a todo
- `test_create_todo_missing_title`: Tests error handling

Achieves 62% code coverage.

### [.github/workflows/ci.yml](.github/workflows/ci.yml)
Continuous Integration workflow:
- Triggers on push to main/dev and all pull requests
- Runs lint checks (flake8) and tests (pytest)
- Fails fast if errors are found

### [.github/workflows/cd.yml](.github/workflows/cd.yml)
Continuous Delivery workflow:
- Triggers when a GitHub Release is published
- Builds Docker image and pushes to DockerHub
- Tags image with version from git tag

---

**Status:** ✅ Ready to use. Push code to main, create a release, and watch the pipelines run!
