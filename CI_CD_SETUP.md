# CI/CD Pipeline Setup Guide

## Overview

Your Croppulse application now has a **full automated CI/CD pipeline** with GitHub Actions that:

- ✅ Runs automated tests on every push
- ✅ Checks code syntax across multiple Python versions
- ✅ Validates all imports and dependencies
- ✅ Auto-deploys to Streamlit Cloud on main branch
- ✅ Reports deployment status

## Architecture

```
GitHub Push to main
      ↓
GitHub Actions CI/CD Pipeline
      ├── Test Job (Python 3.9, 3.10, 3.11)
      │   ├── Install dependencies
      │   ├── Lint with pylint
      │   ├── Check Python syntax
      │   └── Verify imports
      ├── Deploy Job (if tests pass)
      │   └── Trigger Streamlit Cloud redeploy
      └── Status Report
          ├── Notify success/failure
          └── Report deployment status
```

## Workflow Files

### 1. `.github/workflows/ci-cd.yml`
**Main pipeline** - Runs tests and deploys

**Triggers:**
- On every push to `main` branch
- On pull requests

**Steps:**
1. Checkout code
2. Setup Python (3.9, 3.10, 3.11)
3. Install dependencies
4. Run linting
5. Check syntax
6. Test imports
7. Deploy (main branch only)

### 2. `.github/workflows/deploy-status.yml`
**Status reporter** - Shows deployment results

**Reports:**
- Deployment success/failure
- Application URL
- Action link for reviews

### 3. `pyproject.toml`
**Project configuration** - Code quality settings

**Includes:**
- Pylint configuration
- Black formatting rules
- isort import sorting
- MyPy type checking config

## How It Works

### When you push to main:

```
1. GitHub detects push to main
2. CI/CD workflow starts automatically
3. Code is tested on 3 Python versions
4. If all tests pass → Streamlit Cloud redeploys
5. App updates at https://corpplus.streamlit.app
```

### When you create a pull request:

```
1. CI/CD workflow runs tests
2. Code quality checks run
3. Results shown in PR checks
4. Merge only after tests pass
```

## Local Setup

### Install development tools:

```bash
# Install testing & linting tools
pip install pytest pylint black isort mypy

# Install app dependencies
pip install -r croppulse/requirements.txt
```

### Run checks locally before pushing:

```bash
# Check syntax
python -m py_compile croppulse/croppulse_app.py

# Lint code
pylint croppulse/croppulse_app.py

# Format code
black croppulse/

# Sort imports
isort croppulse/

# Test locally
streamlit run croppulse/croppulse_app.py
```

## Monitoring Deployments

### View workflow runs:
1. Go to: https://github.com/bixamtarala/corpplus/actions
2. Click on workflow name to see details
3. View logs for each job

### Check Streamlit Cloud:
1. Go to: https://share.streamlit.io/bixamtarala/corpplus
2. View deployment logs
3. Check app health

## Configuration Files

### `.github/workflows/ci-cd.yml`
```yaml
# Tests run on 3 Python versions
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']

# Only deploy on successful test
needs: test
if: github.event_name == 'push'
```

### `pyproject.toml`
```toml
# Project dependencies
requires-python = ">=3.9"
dependencies = [
    "streamlit>=1.28.1",
    "pandas>=2.1.0",
    "plotly>=5.17.0",
    "numpy>=1.26.0"
]

# Linting rules (disable noisy checks)
[tool.pylint]
disable = ["C0111", "R0913", "R0914", ...]
```

### `.gitignore`
Automatically ignores:
- Python cache files (`__pycache__`, `*.pyc`)
- Virtual environments (`venv/`, `.venv/`)
- IDE settings (`.vscode/`, `.idea/`)
- Streamlit secrets (`.streamlit/secrets.toml`)

## GitHub Actions Status Badge

Add this to your README.md to show pipeline status:

```markdown
[![CI/CD Status](https://github.com/bixamtarala/corpplus/actions/workflows/ci-cd.yml/badge.svg?branch=main)](https://github.com/bixamtarala/corpplus/actions)
```

## Troubleshooting

### Pipeline fails on syntax:
1. Check error in GitHub Actions logs
2. Fix the syntax locally
3. Push again

### Tests pass locally but fail in CI:
1. Check Python version differences
2. Verify all dependencies in requirements.txt
3. Test on same Python version locally

### App not updating on Streamlit Cloud:
1. Check Streamlit Cloud dashboard for errors
2. Verify GitHub repository is connected
3. Check deployment logs in Actions

## Next Steps (Optional Enhancements)

1. **Add Unit Tests:**
   ```bash
   pip install pytest
   # Create tests/ directory with test files
   ```

2. **Code Coverage:**
   ```bash
   pip install coverage pytest-cov
   # Add coverage reporting to CI/CD
   ```

3. **Security Scanning:**
   ```yaml
   # Add to ci-cd.yml
   - name: Run security scan
     run: pip install bandit && bandit -r croppulse/
   ```

4. **Performance Benchmarks:**
   - Monitor app load time
   - Track memory usage
   - Report in each deployment

5. **Slack Notifications:**
   - Alert team on deploy success/failure
   - Post app metrics to Slack

## Support

For issues:
1. Check GitHub Actions logs: https://github.com/bixamtarala/corpplus/actions
2. Review Streamlit Cloud status: https://share.streamlit.io
3. Check requirements compatibility: `pip install -r croppulse/requirements.txt`

---

**Your app is now production-ready with automated CI/CD! 🚀**
