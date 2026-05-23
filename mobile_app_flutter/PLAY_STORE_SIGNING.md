# Play Store Signing Setup

This project can build release artifacts immediately, but a Play Store upload requires a real release keystore.

## Files To Create

1. Create a keystore file, for example:

```powershell
keytool -genkeypair -v -keystore android\keystore\croppulse-upload.jks -keyalg RSA -keysize 2048 -validity 10000 -alias croppulse-upload
```

2. Copy `android/key.properties.example` to `android/key.properties`.

3. Replace the placeholder values in `android/key.properties` with the real store path, alias, and passwords.

## Build Commands

Release APK:

```powershell
Set-Location C:\Users\LENOVO\Desktop\Agritech\mobile_app_flutter
C:\Users\LENOVO\Downloads\flutter_windows_3.41.9-stable\flutter\bin\flutter.bat build apk --release --dart-define=CROPPULSE_API_BASE_URL=https://your-active-api-host
```

Play Store App Bundle:

```powershell
Set-Location C:\Users\LENOVO\Desktop\Agritech\mobile_app_flutter
C:\Users\LENOVO\Downloads\flutter_windows_3.41.9-stable\flutter\bin\flutter.bat build appbundle --release --dart-define=CROPPULSE_API_BASE_URL=https://your-active-api-host
```

## Output Paths

- APK: `build/app/outputs/flutter-apk/app-release.apk`
- AAB: `build/app/outputs/bundle/release/app-release.aab`

## Important Notes

- Replace `https://your-active-api-host` with the backend URL you actually use, or omit the define if the build should not talk to a live API.
- Do not commit `android/key.properties`.
- Do not commit `.jks` or `.keystore` files.
- Without a real keystore, Flutter falls back to debug signing for local release tests, which is not Play Store-ready.