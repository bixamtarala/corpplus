# Mobile Release Checklist

Use this checklist before expecting Firebase App Distribution or Google Play internal testing to work from `.github/workflows/mobile-android.yml`.

## 1. GitHub Release Only

No extra secrets are required for the basic APK build and rolling `mobile-latest` GitHub release.

- Confirm pushes to `main` trigger `.github/workflows/mobile-android.yml`
- Confirm the workflow uploads `app-release.apk`
- Confirm the `mobile-latest` prerelease contains `app-release.apk` and `update-metadata.json`

## 2. Firebase App Distribution

These values are required before the Firebase steps in the workflow will run.

| GitHub secret / variable | Required | Where you obtain it | Notes |
| --- | --- | --- | --- |
| `FIREBASE_APP_ID_ANDROID` | Yes | Firebase Console → Project settings → Your apps → Android app | Must match package name `com.croppulse.mobile`. |
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Yes | Google Cloud Console for the Firebase project → IAM & Admin → Service Accounts → create/download JSON key for a service account with Firebase App Distribution access | Store the raw JSON as the GitHub secret value. |
| `FIREBASE_TESTER_GROUPS` | Optional variable | Firebase Console → App Distribution → Testers & Groups | If omitted, the workflow defaults to `internal-testers`. |

Firebase setup checks:

- The Firebase project contains an Android app registered as `com.croppulse.mobile`
- App Distribution is enabled for that Firebase project
- The service account can upload builds to App Distribution
- The tester group named in `FIREBASE_TESTER_GROUPS` already exists

## 3. Google Play Internal Testing

These values are required before the Play upload step will run.

| GitHub secret / variable | Required | Where you obtain it | Notes |
| --- | --- | --- | --- |
| `PLAY_SERVICE_ACCOUNT_JSON` | Yes | Google Cloud Console linked to Play Console → IAM & Admin → Service Accounts → create/download JSON key | The service account must also be granted access in Google Play Console → Users and permissions. |
| `ANDROID_KEYSTORE_BASE64` | Yes | Generated locally from your upload keystore file | Base64-encode the keystore you use for Play uploads. |
| `ANDROID_KEYSTORE_PASSWORD` | Yes | Your local upload keystore creation step | This is the keystore password, not a console value. |
| `ANDROID_KEY_ALIAS` | Yes | Your local upload keystore creation step | This must match the alias inside the keystore. |
| `ANDROID_KEY_PASSWORD` | Yes | Your local upload keystore creation step | This is the key password for the alias above. |
| `CROPPULSE_PLAY_STORE_URL` | Optional variable | Google Play Console → app listing URL | Used for update metadata and in-app update prompt. The workflow has a default fallback. |

Play setup checks:

- A Google Play app already exists for package `com.croppulse.mobile`
- The app has internal testing enabled
- The Play service account is invited in Play Console and has release permissions
- The upload keystore is the same one registered for the app’s upload key flow

## 4. Generate The Android Signing Secrets Locally

If you do not already have an upload keystore, create one locally:

```powershell
Set-Location C:\Users\LENOVO\Desktop\Agritech\mobile_app_flutter
keytool -genkeypair -v -keystore android\keystore\croppulse-upload.jks -keyalg RSA -keysize 2048 -validity 10000 -alias croppulse-upload
```

Base64-encode it for GitHub:

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes('C:\Users\LENOVO\Desktop\Agritech\mobile_app_flutter\android\keystore\croppulse-upload.jks'))
```

Map the results into GitHub secrets:

- `ANDROID_KEYSTORE_BASE64`: the base64 output from the command above
- `ANDROID_KEYSTORE_PASSWORD`: the keystore password you entered into `keytool`
- `ANDROID_KEY_ALIAS`: the alias you created, for example `croppulse-upload`
- `ANDROID_KEY_PASSWORD`: the key password you entered for that alias

## 5. Final Dry Run

Before relying on automation, verify all of the following:

- `flutter test` passes locally in `mobile_app_flutter`
- A local release APK builds successfully
- The GitHub Actions run uploads an APK artifact
- Firebase distribution runs only after both Firebase secrets are set
- Play internal testing runs only after the Play JSON and all four Android signing secrets are set