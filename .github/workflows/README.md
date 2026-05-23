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

### 2. Mobile Android Delivery (`mobile-android.yml`)
**Trigger:** Every push to `main` and manual workflow dispatch

**Jobs:**
1. **Android Build**
   - Sets up Java 17 and Flutter 3.41.9
   - Runs `flutter pub get` inside `mobile_app_flutter`
   - Builds `app-release.apk`

2. **Artifact Publishing**
   - Uploads the APK as a GitHub Actions artifact for each run
   - Updates a rolling prerelease tagged `mobile-latest`
   - Attaches the latest `app-release.apk` to that prerelease

3. **Firebase App Distribution**
   - Optional
   - Runs only when the required repository secrets are configured
   - Distributes the same APK to your tester group(s)

**Required repository secrets for Firebase distribution:**
- `FIREBASE_APP_ID`
- `FIREBASE_SERVICE_ACCOUNT`
  Store the Firebase service account JSON as the full secret value.
- `FIREBASE_TESTER_GROUPS`
  Example: `internal-testers`

**Notes for Android signing:**
- The current Android Gradle config falls back to debug signing when no release keystore is present.
- That is fine for internal testing, GitHub artifacts, and Firebase App Distribution.
- For production-grade signed builds, add your Android keystore and key properties separately.

**Where to get the APK after each push:**
- GitHub Actions run artifact: `croppulse-android-apk-<run number>`
- GitHub prerelease tag: `mobile-latest`

## Local Testing

Before pushing, test locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pylint

# Check syntax
python -m py_compile streamlit_app_phase2.py

# Test imports
python -c "import streamlit; import pandas; import plotly; import db_config; print('✓ All imports successful')"

# Run the app locally
streamlit run streamlit_app_phase2.py
```

## File Structure

```
.github/
├── workflows/
│   ├── ci-cd.yml          # Main Streamlit CI/CD pipeline
│   ├── mobile-android.yml # Android APK build/release/distribution workflow
│   └── deploy-status.yml  # Streamlit deployment status reporter
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

### Mobile APK not reaching Firebase testers
- Confirm `FIREBASE_APP_ID`, `FIREBASE_SERVICE_ACCOUNT`, and `FIREBASE_TESTER_GROUPS` exist in repository secrets
- Confirm the Firebase app is an Android app that matches `com.croppulse.mobile`
- Check the Mobile Android Delivery workflow logs in GitHub Actions

### Mobile APK release missing on GitHub
- Check the `mobile-android.yml` workflow run logs
- Confirm the runner built `mobile_app_flutter/build/app/outputs/flutter-apk/app-release.apk`
- Verify the workflow has permission to write repository contents for release updates

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
