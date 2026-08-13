# GitHub Secrets and Docker Hub Setup Guide

This guide explains how to configure the GitHub Actions workflow to automatically build and push Docker images to Docker Hub.

## Prerequisites

- GitHub repository with the Hospital Application
- Docker Hub account
- GitHub repository write access

## Step 1: Create Docker Hub Personal Access Token

### 1.1 Log in to Docker Hub
- Visit https://hub.docker.com/
- Sign in with your Docker Hub credentials (create account if needed)

### 1.2 Generate Personal Access Token (PAT)
1. Click on your **Profile icon** (top right)
2. Select **Account Settings**
3. Navigate to **Security** tab
4. Click **New Access Token**
5. Give it a descriptive name (e.g., "GitHub Actions Hospital App")
6. Select access permissions: **Read, Write, Delete** (for pushing images)
7. Click **Generate**
8. **IMPORTANT**: Copy the token immediately and save it somewhere safe - you won't be able to see it again!

## Step 2: Configure GitHub Secrets

### 2.1 Add DOCKER_USERNAME Secret
1. Go to your GitHub repository
2. Click **Settings** (top menu bar)
3. Click **Secrets and variables** → **Actions** (left sidebar)
4. Click **New repository secret**
5. **Name**: `DOCKER_USERNAME`
6. **Secret**: Your Docker Hub username
7. Click **Add secret**

### 2.2 Add DOCKER_PASSWORD Secret
1. Click **New repository secret** again
2. **Name**: `DOCKER_PASSWORD`
3. **Secret**: Your Docker Hub Personal Access Token (from Step 1.2)
4. Click **Add secret**

## Step 3: Verify Workflow Configuration

The workflow file (`.github/workflows/ci-cd.yml`) is already configured to:

1. ✅ Run linting checks
2. ✅ Run tests with 85%+ coverage requirement
3. ✅ Run security checks with Bandit
4. ✅ Build Docker image (only if all checks pass)
5. ✅ Authenticate with Docker Hub using GitHub Secrets
6. ✅ Push image to Docker Hub with tags:
   - `<username>/<repo>:latest` (main branch)
   - `<username>/<repo>:<commit-sha>` (commit-specific tag)

### Trigger Conditions
- Workflow runs automatically when you push to `main` or `develop` branches
- Docker build/push only runs on `main` branch after all CI checks pass
- Pull requests trigger CI checks but NOT the Docker push step

## Step 4: Push to GitHub and Trigger Workflow

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Add Docker Hub CI/CD configuration"
   git push origin main
   ```

2. Go to your GitHub repository **Actions** tab
3. Watch the workflow execute:
   - **Gate 1 - Linting**: Code quality checks
   - **Gate 2 - Test Coverage**: Tests with 85%+ coverage
   - **Gate 3 - Security Check**: Bandit security scan
   - **Build and Push Docker Image**: Builds and pushes to Docker Hub

## Step 5: Verify Docker Image on Docker Hub

1. Once the workflow completes successfully, go to https://hub.docker.com/r/<your-username>
2. Find your repository (name matches your GitHub repo)
3. Verify the image tags:
   - `latest` - most recent image
   - `<commit-sha>` - specific commit versions

## Security Best Practices

✅ **DO:**
- Use GitHub Secrets for credentials (never hardcode them)
- Rotate your Docker Hub PAT periodically
- Use descriptive token names for organization
- Review workflow logs for sensitive data (GitHub hides secrets)

❌ **DON'T:**
- Commit credentials to the repository
- Share Docker Hub tokens outside GitHub Secrets
- Commit Docker Hub passwords in any file
- Store credentials in environment files (.env, config.py, etc.)

## Troubleshooting

### Docker Login Fails
- Verify GitHub Secrets are correctly configured
- Ensure DOCKER_PASSWORD contains a Personal Access Token, not your actual password
- Check that secrets match your exact Docker Hub username

### Workflow Doesn't Push to Docker Hub
- Verify you pushed to the `main` branch
- Ensure all CI checks (lint, test, security) passed first
- Check workflow logs in GitHub Actions tab
- Verify Docker Hub authentication in the workflow logs (look for "Log in to Docker Hub" step)

### Image Not Appearing on Docker Hub
- Check that the workflow completed successfully (no red X marks)
- Verify the DOCKER_USERNAME secret is correct
- Wait a few moments - Docker Hub may take time to update
- Refresh your Docker Hub page

### Coverage Check Fails
- Tests must achieve ≥85% code coverage
- Review test failures in the workflow logs
- Add more tests to increase coverage
- Run locally: `pytest --cov=app --cov-report=term-missing`

## Workflow Structure

```
Push to Main Branch
       ↓
GitHub Actions Triggered
       ↓
┌──────────────────────────────────────┐
│ Run in Parallel (jobs)               │
├──────────────────────────────────────┤
│ • Linting (flake8)                   │
│ • Security (Bandit)                  │
│ • Tests (Pytest, 85%+ coverage)      │
└──────────────────────────────────────┘
       ↓ (All must pass)
Build Docker Image
       ↓
Authenticate with Docker Hub
       ↓
Push to Docker Hub
       ↓
Docker Image Available for Deployment
```

## Docker Hub Repository URL Format

Once configured, your Docker Hub image will be available at:

```
https://hub.docker.com/r/<docker-username>/<repository-name>
```

Example:
```
https://hub.docker.com/r/johndoe/hospital-appointment-api
```

This is the URL you'll submit as proof of the CI/CD integration.

## Next Steps

1. ✅ Configure GitHub Secrets (DOCKER_USERNAME, DOCKER_PASSWORD)
2. ✅ Push code to main branch
3. ✅ Wait for workflow to complete
4. ✅ Verify image appears on Docker Hub
5. ✅ Submit Docker Hub URL for grading

For questions or issues, check the GitHub Actions logs in your repository's Actions tab.
