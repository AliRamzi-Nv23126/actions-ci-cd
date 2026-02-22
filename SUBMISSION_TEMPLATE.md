# Assignment Submission Template

This document guides you through documenting your work for submission.

## How to Create Your Submission

Create a PDF or Markdown file with the following sections and include screenshots as evidence.

---

# GitHub Actions CI/CD Pipeline Assignment - Submission

**Student Name:** [Your Name]  
**Date:** [Today's Date]  
**GitHub Repository:** [Your repo URL]

---

## Part A: CI Workflow

### CI Workflow File

Copy your [.github/workflows/ci.yml](.github/workflows/ci.yml):

```yaml
[PASTE YOUR CI WORKFLOW HERE]
```

### Successful CI Run

**Screenshot:** GitHub Actions showing CI workflow passing (green ✅)

Steps to capture:
1. Go to your GitHub repo → Actions tab
2. Click on a "CI" workflow run
3. Wait for all steps to show green checkmarks
4. Take a screenshot

Instructions:
- Show the full workflow with all steps: Checkout, Setup Python, Install dependencies, Lint, Tests
- All steps must show green ✅ status

**Example log output:**
```
✓ Checkout code
✓ Set up Python
✓ Install dependencies
✓ Lint with flake8
✓ Run tests with pytest
```

### Failed CI Run (Then Fixed)

**Screenshot 1:** CI workflow failing (red ❌)

Steps to create:
1. Edit a file to introduce a linting error or test failure
   - Example lint error: `x=1` (no spaces around =)
   - Example test failure: modify a test assertion to be false
2. Push the branch: `git add . && git commit -m "test: introduce error" && git push`
3. Go to GitHub Actions and wait for CI to run
4. Take screenshot showing red ❌

**Screenshot 2:** CI workflow passing after fix (green ✅)

Steps to fix:
1. Fix the error you introduced
2. Push the fix: `git add . && git commit -m "fix: resolve error" && git push`
3. Wait for CI to run again
4. Take screenshot showing green ✅

---

## Part B: CD Workflow

### CD Workflow File

Copy your [.github/workflows/cd.yml](.github/workflows/cd.yml):

```yaml
[PASTE YOUR CD WORKFLOW HERE]
```

### GitHub Secrets Configuration

**Important:** Do NOT include secret values in your submission

Screenshot requirements:
1. Go to GitHub → Settings → Secrets and variables → Actions
2. Show that you have created secrets (do NOT reveal the values)
3. Screenshot should show secret names only:
   - `DOCKERHUB_USERNAME` ✓
   - `DOCKERHUB_TOKEN` ✓

### CD Successful Run

**Screenshot:** GitHub Actions showing CD workflow passing (green ✅)

Steps:
1. Create a GitHub Release:
   - Go to your repo → Releases → Create a new release
   - Tag: `v0.1.0`
   - Title: "version 0.1.0"
   - Publish
2. Go to Actions tab and wait for "CD" workflow to start
3. Wait until all steps complete with green ✅
4. Take screenshot showing:
   - Workflow job name: "build-push"
   - Steps: Checkout, Setup Buildx, Login to DockerHub, Extract version, Build and push
   - All steps with green ✅

### Docker Image in Registry

**Screenshot:** DockerHub showing your newly pushed image

Steps:
1. Log in to [hub.docker.com](https://hub.docker.com)
2. Click on your repository (e.g., `username/todo-app`)
3. Go to Tags tab
4. Screenshot should show:
   - Tag: `0.1.0` (extracted from release v0.1.0)
   - Tag: `latest` (always points to newest version)
   - Published date (recently)

---

## Part C: End-to-End Flow

### Demonstration Description

Write 3-5 sentences describing the complete flow you executed:

**Example:**

> "I made a code change by adding a new test case to `tests/test_app.py`. I pushed this to the `dev` branch, which triggered the CI workflow automatically. The CI workflow ran linting and tests, and both passed with green checkmarks. I then created a pull request from `dev` to `main`, verified CI passed on the PR, and merged it. Finally, I created a GitHub Release tagged `v0.2.0`, which triggered the CD workflow automatically. The CD workflow built the Docker image, extracted the version from the git tag, and pushed the image to DockerHub with tags `0.2.0` and `latest`. I verified the image appeared in my DockerHub repository within 2 minutes."

### Release Screenshot

**Screenshot:** GitHub Release page showing the version you created

Requirements:
- Show release tag (e.g., v0.2.0)
- Show release title
- Show release notes/description
- Show "Published" status
- Show the created date

Path: **Releases** → Click on your release

### Registry Screenshot

**Screenshot:** DockerHub (or ECR) showing the new image tag from your release

Requirements:
- Repository name visible
- Tag list showing the version you just released (e.g., 0.2.0)
- `latest` tag also present
- Created/pushed date visible

---

## Summary of Learning

Write a short paragraph (3-5 sentences) reflecting on:
- What you learned about GitHub Actions
- Key benefits of CI/CD automation
- One challenge you faced and how you overcame it
- How you would use this in a real project

**Example:**

> "GitHub Actions makes it incredibly easy to automate repetitive tasks like testing and deployment. I learned that CI/CD pipelines catch bugs early by automatically running tests on every push, which gives confidence when merging code. Using secrets for credentials was a key security lesson - I realized how important it is to never commit sensitive data. One challenge I faced was getting the version extraction right in the CD workflow; I debugged it by checking the workflow logs and realized the tag format had to start with 'v'. In a real project, I would require CI checks to pass before allowing merges and would set up notifications to alert the team when deployments succeed or fail."

---

## Submission Checklist

Before submitting, verify you have:

- [ ] Part A: CI workflow file (ci.yml) included
- [ ] Part A: Screenshot of successful CI run
- [ ] Part A: Introduced an error, showed failed CI, then fixed it (2 screenshots)
- [ ] Part B: CD workflow file (cd.yml) included
- [ ] Part B: Screenshot of GitHub Secrets (names only, no values)
- [ ] Part B: Screenshot of successful CD run
- [ ] Part B: Screenshot of Docker image in registry (DockerHub/ECR)
- [ ] Part C: Release description (3-5 sentences about flow)
- [ ] Part C: Screenshot of GitHub Release page
- [ ] Part C: Screenshot of registry showing new tag
- [ ] Summary: Paragraph on what you learned
- [ ] No secret values are visible in any part of the submission
- [ ] All screenshots are clear and show the requested information

---

## Submission Format

### Option 1: Markdown File (Recommended)

Save as `SUBMISSION.md` in your repository:
```
your-repo/
├── SUBMISSION.md (with embedded screenshots)
├── app.py
├── tests/
├── .github/workflows/
├── README.md
└── SETUP_GUIDE.md
```

### Option 2: PDF File

Convert your markdown to PDF and submit (use tools like:
- GitHub → Print to PDF
- Pandoc
- VS Code extension
- Online markdown-to-PDF converter

---

## Screenshots: Technical Tips

### Taking Good Screenshots

1. **Use full width** - Show the complete UI, not just part of it
2. **Include context** - Show URL bar so reviewer knows what page you're on
3. **Highlight key info** - Use developer tools highlighter or rectangles
4. **Dark/Light mode OK** - Either is fine, just be consistent
5. **Readable size** - No smaller than 1024px wide

### Tools to Help

**Windows:** Snagit, Greenshot, or built-in Snipping Tool
**Mac:** Built-in Screenshot tool (Cmd + Shift + 4)
**Linux:** Flameshot, GNOME Screenshot
**Online:** Placeholder.com screenshot tools

### For Workflow Logs

- Actions tab → Click workflow run → Click job → Expand step
- Select text for crisp screenshots
- Include full step name and status

---

## Common Mistakes to Avoid

❌ **Don't submit:**
- Screenshots showing secret values
- Passwords or tokens in any form
- Personal information

❌ **Make sure:**
- Linting passes (`flake8 . --max-line-length=120`)
- Tests pass (`pytest tests/ -v`)
- All CI/CD runs are recent (within last day)
- Release tag format is correct (v0.X.X)

---

## Need Help?

Refer to the guides in your repository:

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Complete setup and troubleshooting
- [README.md](README.md) - Quick reference and API documentation
- [ECR_SETUP.md](ECR_SETUP.md) - If using Amazon ECR instead of DockerHub

---

**Ready to submit? Ensure all checkboxes above are checked, then submit your file(s).**
