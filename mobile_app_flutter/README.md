# CropPulse Mobile

## Release flow

The GitHub Actions workflow at `.github/workflows/mobile-android.yml` now supports three mobile release channels from the same push to `main`:

- GitHub rolling release asset `mobile-latest` with the APK and `update-metadata.json`
- Firebase App Distribution for tester installs and notifications
- Google Play internal testing with a signed `.aab`

## Required GitHub secrets

Add these repository secrets before expecting Firebase or Play uploads to run:

- `ANDROID_KEYSTORE_BASE64`: base64-encoded upload keystore file
- `ANDROID_KEYSTORE_PASSWORD`: keystore password
- `ANDROID_KEY_ALIAS`: upload key alias
- `ANDROID_KEY_PASSWORD`: upload key password
- `FIREBASE_APP_ID_ANDROID`: Firebase Android app id
- `FIREBASE_SERVICE_ACCOUNT_JSON`: Firebase service account JSON
- `PLAY_SERVICE_ACCOUNT_JSON`: Google Play service account JSON

Optional repository variables:

- `FIREBASE_TESTER_GROUPS`: Firebase tester groups, defaults to `internal-testers`
- `CROPPULSE_PLAY_STORE_URL`: Play listing URL used by the in-app update prompt

## In-app update checker

The app checks for updates on startup by reading the latest `update-metadata.json` asset from the rolling GitHub release. By default it uses:

- `CROPPULSE_UPDATE_METADATA_URL`: `https://github.com/bixamtarala/corpplus/releases/download/mobile-latest/update-metadata.json`
- `CROPPULSE_PLAY_STORE_URL`: `https://play.google.com/store/apps/details?id=com.croppulse.mobile`

You can override those with Flutter dart-defines when needed.

## Local release builds

```bash
flutter pub get
flutter build apk --release
flutter build appbundle --release
```

Release artifacts:

- `build/app/outputs/flutter-apk/app-release.apk`
- `build/app/outputs/bundle/release/app-release.aab`
