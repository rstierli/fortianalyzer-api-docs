# GitHub Mirror Setup for Read the Docs

This repository automatically mirrors from GitLab to GitHub for publishing on Read the Docs.

## Architecture

```
GitLab (Source of Truth)     →     GitHub (Public Mirror)     →     Read the Docs
Internal Development                Public Documentation              Live Docs Site
```

## Setup Instructions

### 1. GitHub Personal Access Token

Create a GitHub Personal Access Token (PAT) for the mirroring:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name: `GitLab CI - FortiAnalyzer Docs Mirror`
4. Expiration: `No expiration` (or set as per your security policy)
5. Scopes: Select **`repo`** (full control of private repositories)
6. Click **"Generate token"**
7. **Copy the token** (you won't see it again!)

### 2. Configure GitLab CI/CD Variables

Add the following variables to your GitLab project:

**GitLab Settings → CI/CD → Variables**

| Variable Name | Value | Protected | Masked | Description |
|--------------|-------|-----------|--------|-------------|
| `GITHUB_USERNAME` | `rstierli` | ✅ Yes | ❌ No | Your GitHub username |
| `GITHUB_TOKEN` | `ghp_xxxx...` | ✅ Yes | ✅ Yes | GitHub Personal Access Token |

**How to add:**
1. Go to: https://gitlab.frval.fortinet-emea.com/support/cse-intl-cmm/FAZ_howto_API/-/settings/ci_cd
2. Expand **"Variables"**
3. Click **"Add variable"**
4. Add each variable from the table above
5. Check **"Protect variable"** and **"Mask variable"** (for token)

### 3. Initial Push to GitHub

From your local repository:

```bash
cd /Users/rstierli/03_Privat/myGIT@private/fortianalyzer-api-docs

# Verify remotes are configured
git remote -v

# Push to GitHub for the first time
git push origin main
```

### 4. Configure Read the Docs

1. Go to: https://readthedocs.org/
2. **Sign in with GitHub** (or create account)
3. Click **"Import a Project"**
4. Select **`fortianalyzer-api-docs`**
5. Click **"Next"**
6. Configuration will be auto-detected from `.readthedocs.yaml`
7. Click **"Build version"**

### 5. Verify the Setup

After committing to GitLab `main` branch:

1. GitLab CI/CD will run automatically
2. Check pipeline: https://gitlab.frval.fortinet-emea.com/support/cse-intl-cmm/FAZ_howto_API/-/pipelines
3. Verify GitHub received the push: https://github.com/rstierli/fortianalyzer-api-docs/commits/main
4. Read the Docs will auto-build: https://readthedocs.org/projects/fortianalyzer-api-docs/builds/

## Workflow

### Making Documentation Changes

1. **Edit files** in GitLab repository (or local clone)
2. **Commit and push** to GitLab `main` branch
3. **GitLab CI/CD** automatically mirrors to GitHub
4. **Read the Docs** detects GitHub webhook and rebuilds
5. **Live docs** updated at: `https://fortianalyzer-api-docs.readthedocs.io/`

### Manual Mirror Trigger

If automatic mirroring fails or you need to force sync:

```bash
# From your local repo
cd /Users/rstierli/03_Privat/myGIT@private/fortianalyzer-api-docs

# Pull latest from GitLab
git pull gitlab main

# Push to GitHub
git push origin main
```

## Files Added for Read the Docs

- `.readthedocs.yaml` - Read the Docs build configuration
- `requirements.txt` - Python dependencies for Sphinx build
- `.gitlab-ci.yml` - Updated with GitHub mirror stage

## Troubleshooting

### Mirror job fails with "Authentication failed"

Check that:
- `GITHUB_TOKEN` is valid and not expired
- `GITHUB_USERNAME` matches your GitHub username
- Token has `repo` scope permissions

### Read the Docs build fails

1. Check build logs at: https://readthedocs.org/projects/fortianalyzer-api-docs/builds/
2. Verify `requirements.txt` includes all dependencies
3. Check `.readthedocs.yaml` configuration
4. Ensure Sphinx conf.py is compatible

### Changes not appearing on Read the Docs

1. Verify GitLab pipeline succeeded
2. Check GitHub repo has latest commit
3. Manually trigger Read the Docs build if needed

## Documentation URLs

- **GitLab Pages** (Internal): https://support.gitlab.frval.fortinet-emea.com/cse-intl-cmm/faz_howto_api
- **Read the Docs** (Public): https://fortianalyzer-api-docs.readthedocs.io/
- **GitHub Mirror**: https://github.com/rstierli/fortianalyzer-api-docs

## Maintenance

### Updating Dependencies

Edit `requirements.txt` and commit:

```bash
# requirements.txt
sphinx>=7.0.0
myst-parser>=2.0.0
# ... other packages
```

### Changing Read the Docs Settings

Edit `.readthedocs.yaml` to:
- Change Python version
- Add/remove output formats (PDF, ePub)
- Modify build configuration

## Security Notes

- ✅ GitHub token is masked in GitLab CI/CD logs
- ✅ Token stored as protected variable
- ✅ Only runs on `main` branch (protected)
- ⚠️ Rotate token regularly (every 90 days recommended)
- ⚠️ Never commit tokens to git repository

## Support

For issues with:
- **GitLab CI/CD**: Check pipeline logs
- **GitHub Mirror**: Verify token and permissions
- **Read the Docs**: Check build logs on readthedocs.org
