# GitHub Actions CI/CD Pipeline Documentation

## Overview
This directory contains automated CI/CD workflows for the Croppulse application using GitHub Actions.

## Workflows

### 1. CI/CD Pipeline (`ci-cd.yml`)
**Trigger:** Push to `main` branch or Pull Requests

**Jobs:**
1. **Test Job** - Runs on multiple Python versions (3.9, 3.10, 3.11)
   - Installs dependencies from `requirements.txt`
   - Lints code with pylint (errors only)
   - Checks Python syntax
   - Verifies all imports work

2. **Deploy Job** - Runs after tests pass
   - Only triggers on successful push to main
   - Streamlit Cloud automatically redeploys

**Success Indicators:**
- ✓ All Python versions pass syntax check
- ✓ No import errors
- ✓ Code linting passes (critical errors)

**Deployment:**
- Automatic deployment to Streamlit Cloud on main branch
- App URL: https://corpplus.streamlit.app

## Local Testing

Before pushing, test locally:

```bash
# Install dependencies
pip install -r croppulse/requirements.txt
pip install pylint

# Check syntax
python -m py_compile croppulse/croppulse_app.py

# Test imports
cd croppulse
python -c "import streamlit; import pandas; import plotly; print('✓ All imports successful')"

# Run the app locally
streamlit run croppulse_app.py
```

## File Structure

```
.github/
├── workflows/
│   └── ci-cd.yml          # Main CI/CD pipeline
└── README.md              # This file
```

## Requirements

- Python 3.9+
- GitHub repository connected to Streamlit Cloud
- Dependencies listed in `croppulse/requirements.txt`

## Troubleshooting

### Pipeline fails on import
- Check that all packages in `requirements.txt` are installed
- Verify Python version compatibility
- Run `pip install -r croppulse/requirements.txt` locally

### Streamlit Cloud not deploying
- Ensure your Streamlit Cloud account is connected to the GitHub repository
- Check Streamlit Cloud dashboard for error logs
- Verify app configuration in Streamlit Cloud settings

### Linting warnings
- Linting is non-blocking (continue-on-error: true)
- Fix warnings manually or configure pylint in `pyproject.toml`

## Next Steps

To enhance the pipeline:
1. Add unit tests with pytest
2. Add code coverage reporting
3. Add performance benchmarks
4. Add security scanning
5. Add deployment notifications
