# Android Test Readiness Checklist

Last verified: May 22, 2026

## Environment

- Flutter SDK available locally: `C:\Users\LENOVO\Downloads\flutter_windows_3.41.9-stable\flutter`
- Android SDK available locally: `C:\Users\LENOVO\AppData\Local\Android\sdk`
- Test AVD: `CropPulse_Pixel_7_API_35`
- Backend base URL for emulator: `http://10.0.2.2:8000`
- API prefix in use: `/api/v2`

## Pre-Run Checks

- Start the Phase 2 backend on port `8000`
- Confirm the emulator is visible in `adb devices`
- Run the app with `--dart-define=CROPPULSE_API_BASE_URL=http://10.0.2.2:8000`
- Verify the installed app package is `com.croppulse.mobile`

## Verified Flows

- OTP request succeeds against `POST /api/v2/auth/request-otp`
- OTP verify succeeds against `POST /api/v2/auth/verify-otp`
- Farmer profile sync succeeds against `GET /api/v2/farmer/profile`
- Marketplace search succeeds against `GET /api/v2/marketplace/search`
- Marketplace listing creation succeeds against `POST /api/v2/marketplace/listings`
- Marketplace offer submission succeeds against `POST /api/v2/marketplace/offers`
- Logout clears the saved session and relaunch returns to the login screen
- Session restore works after a confirmed login and relaunch returns to the authenticated home shell

## Test Credentials

- Phone number: `9876543210`
- Mock OTP: `123456`

## Launch Commands

```powershell
cd C:\Users\LENOVO\Desktop\Agritech
.\.venv\Scripts\python.exe -m uvicorn phase2_backend.main_phase2:app --host 0.0.0.0 --port 8000
```

```powershell
cd C:\Users\LENOVO\Desktop\Agritech\mobile_app_flutter
C:\Users\LENOVO\Downloads\flutter_windows_3.41.9-stable\flutter\bin\flutter.bat run -d emulator-5554 --dart-define=CROPPULSE_API_BASE_URL=http://10.0.2.2:8000
```

## Ready If

- The backend starts without startup errors
- The emulator boots and remains connected through the test pass
- Login reaches the authenticated home shell
- Profile data loads without a client-side error banner
- Market search returns at least one listing
- Listing creation and offer submission both return success banners
- Relaunch after logout shows the login gate
- Relaunch after login restores the authenticated shell

## Known Good Notes

- For emulator automation in this environment, `adb.exe` is most reliable when invoked through `Start-Process -FilePath ... -ArgumentList ...`
- If the emulator becomes unstable with hardware rendering, relaunch with software graphics such as `-gpu swiftshader_indirect`