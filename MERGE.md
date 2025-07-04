# Merge Instructions

This document provides instructions for merging the current feature branch changes back to the main branch using two different approaches.

## Current Changes Summary

The following changes have been made to improve the PDF RAG chat system:

1. **Backend Dependencies**: Added missing dependencies to `pyproject.toml` and `api/requirements.txt`
2. **Frontend Proxy Configuration**: Added proxy configuration in `frontend/vite.config.js` to forward API requests to the backend
3. **Environment Setup**: Improved dependency management and server configuration

## Prerequisites

Before merging, ensure you have:
- [ ] All changes are committed to the current feature branch
- [ ] Tests pass (if applicable)
- [ ] Code review completed (if working with a team)
- [ ] GitHub CLI installed (for CLI approach)

## Method 1: GitHub Pull Request (Recommended for Teams)

### Step 1: Push Your Feature Branch
```bash
# Ensure you're on your feature branch
git branch

# Push the feature branch to GitHub
git push origin your-feature-branch-name
```

### Step 2: Create Pull Request
1. Go to your GitHub repository in a web browser
2. Click on "Pull requests" tab
3. Click "New pull request"
4. Select:
   - **Base branch**: `main`
   - **Compare branch**: `your-feature-branch-name`
5. Click "Create pull request"
6. Add a descriptive title and description:

```
Title: Add PDF RAG System Dependencies and Frontend Proxy Configuration

Description:
- Added missing dependencies for PDF processing and AI functionality
- Configured frontend proxy to properly communicate with backend API
- Updated pyproject.toml and requirements.txt with necessary packages
- Fixed Vite configuration for API request forwarding

Changes:
- api/requirements.txt: Added PyPDF2, numpy, python-dotenv, and aimakerspace dependencies
- pyproject.toml: Updated project dependencies
- frontend/vite.config.js: Added proxy configuration for /api requests
```

### Step 3: Review and Merge
1. Review the changes in the PR
2. Request code review from team members (if applicable)
3. Once approved, click "Merge pull request"
4. Choose merge strategy (usually "Create a merge commit")
5. Click "Confirm merge"

### Step 4: Clean Up
```bash
# Switch to main branch
git checkout main

# Pull the latest changes
git pull origin main

# Delete the feature branch locally
git branch -d your-feature-branch-name

# Delete the feature branch on GitHub (optional)
git push origin --delete your-feature-branch-name
```

## Method 2: GitHub CLI (Quick Merge)

### Step 1: Authenticate with GitHub CLI
```bash
# Login to GitHub CLI
gh auth login

# Follow the prompts to authenticate
```

### Step 2: Create Pull Request via CLI
```bash
# Create a pull request from your current branch to main
gh pr create \
  --title "Add PDF RAG System Dependencies and Frontend Proxy Configuration" \
  --body "This PR adds missing dependencies for PDF processing and AI functionality, and configures the frontend proxy to properly communicate with the backend API.

Changes:
- api/requirements.txt: Added PyPDF2, numpy, python-dotenv, and aimakerspace dependencies
- pyproject.toml: Updated project dependencies  
- frontend/vite.config.js: Added proxy configuration for /api requests

This resolves issues with PDF upload functionality and frontend-backend communication." \
  --base main
```

### Step 3: Merge via CLI
```bash
# Merge the pull request
gh pr merge --merge

# Or if you want to squash commits
gh pr merge --squash
```

### Step 4: Clean Up
```bash
# Switch to main branch
git checkout main

# Pull the latest changes
git pull origin main

# Delete the feature branch locally
git branch -d your-feature-branch-name

# Delete the feature branch on GitHub
gh pr delete-branch
```

## Verification After Merge

After merging, verify that:

1. **Backend starts correctly**:
   ```bash
   cd api
   python -m uvicorn app:app --reload
   ```

2. **Frontend connects to backend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **PDF upload functionality works** with a valid OpenAI API key

## Troubleshooting

### If merge conflicts occur:
1. Resolve conflicts in the affected files
2. Add resolved files: `git add .`
3. Complete the merge: `git commit`
4. Push changes: `git push`

### If the feature branch doesn't exist on GitHub:
```bash
# Push the branch first
git push -u origin your-feature-branch-name
```

### If you need to update the PR:
```bash
# Make your changes
git add .
git commit -m "Update PR with additional changes"
git push origin your-feature-branch-name
```

## Notes

- Always use descriptive commit messages and PR titles
- Consider using conventional commits format for better project history
- Keep feature branches focused on a single feature or fix
- Delete feature branches after successful merge to keep the repository clean 