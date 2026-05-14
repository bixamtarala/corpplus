# CropPulse Mobile - Flutter Setup & Run Guide

**Status:** Flutter downloading (567MB)  
**Platform:** Windows 10/11 + Android  
**Estimated Setup Time:** 20-30 minutes  

---

## 📥 Step 1: Flutter SDK Installation (IN PROGRESS)

### Automatic Installation (Current)
```powershell
# Running:
cd C:\flutter_sdk
# Downloading Flutter v3.19.6 (567MB)
# Extracting files...
```

### Manual Installation (Alternative)
If automatic fails, download manually:
1. Go to https://flutter.dev/docs/get-started/install/windows
2. Download: `flutter_windows_3.19.6-stable.zip`
3. Extract to: `C:\flutter_sdk\flutter`
4. Add to PATH: `C:\flutter_sdk\flutter\bin`

---

## 🔧 Step 2: Environment Setup (After Download)

### Add Flutter to PATH (Windows)
```powershell
# 1. Open System Properties
# 2. Go to Environment Variables
# 3. Add to PATH: C:\flutter_sdk\flutter\bin
# 4. Restart PowerShell

# Verify:
flutter --version
# Should show: Flutter 3.19.6 • channel stable
```

### Run Flutter Doctor
```powershell
flutter doctor
```

**Expected Output:**
```
[✓] Flutter (Channel stable, 3.19.6)
[✓] Windows Version (Windows 10/11 22H2)
[!] Visual Studio - develop for windows (incomplete - install if needed)
[ ] Android Studio (not yet installed)
[ ] Chrome - develop for web (not installed)
[!] Android SDK (needs setup)
```

---

## 🤖 Step 3: Android Setup (REQUIRED)

### Option A: Android Studio (Recommended)
```powershell
# 1. Download Android Studio from:
# https://developer.android.com/studio

# 2. Install it
# 3. Launch Android Studio
# 4. Install SDKs:
#    - Go to SDK Manager
#    - Install "Android SDK Build-Tools 34"
#    - Install "Android SDK Platform 34"
#    - Install "Android Emulator"
#    - Set Android SDK location

# 5. Accept licenses:
flutter doctor --android-licenses
# Type 'y' for all prompts
```

### Option B: Command-Line Android SDK (Advanced)
```powershell
# Install Android SDK Command-line tools
# Add to PATH: C:\Android\cmdline-tools\bin
# Add to PATH: C:\Android\platform-tools
```

### Accept Android Licenses
```powershell
flutter doctor --android-licenses
# Answer 'y' to all prompts
```

---

## 📱 Step 4: Android Emulator Setup

### Create Virtual Device
```powershell
# 1. Open Android Studio
# 2. Click: AVD Manager (Tools → Device Manager)
# 3. Create new device:
#    - Device: Pixel 5
#    - OS: Android 13 (API 33) or higher
#    - RAM: 2GB minimum (4GB recommended)

# 4. Start emulator:
#    Option A: From Android Studio UI
#    Option B: Command-line:
emulator -avd Pixel_5_API_33
```

### Or Use Physical Device
```powershell
# 1. Connect Android phone via USB
# 2. Enable USB Debugging:
#    Settings → Developer Options → USB Debugging
# 3. Run:
flutter devices
# Should show your device
```

---

## ✅ Step 5: Verify Setup

```powershell
flutter doctor
```

**Required for green checkmarks:**
```
[✓] Flutter (Channel stable, 3.19.6)
[✓] Windows Version (Windows 10/11 22H2)
[✓] Android toolchain - develop for Android devices
[✓] Android Studio (latest)
[✓] Devices (Emulator or physical device detected)
```

---

## 🚀 Step 6: Run the App

### Navigate to Project
```powershell
cd c:\Users\LENOVO\Desktop\Agritech\mobile_app_flutter
```

### Get Dependencies
```powershell
flutter pub get
# Downloads all 20+ packages
# Takes 1-2 minutes
```

### Start Emulator (if not running)
```powershell
emulator -avd Pixel_5_API_33 &
# Wait 10-15 seconds for emulator to fully boot
flutter devices
# Should show your emulator listed
```

### Run the App
```powershell
flutter run
```

### Expected Output
```
Launching lib/main.dart on Pixel 5 in debug mode...
(Takes 10-30 seconds on first run)

Waiting for Pixel 5 to report its views...
All views reported.
════════════════════════════════════════════════════════════════════
App started successfully! 🎉
════════════════════════════════════════════════════════════════════
```

---

## 🎯 What You'll See

### On Emulator Screen
```
┌─────────────────────────────┐
│  🌾 CropPulse               │
│     Agricultural OS         │
│                             │
│  📈 Daily Intelligence Feed │
│                             │
│  [Alert Card 1]             │
│  [Alert Card 2]             │
│  [Alert Card 3]             │
│  [Alert Card 4]             │
│                             │
│  ⚡ Quick Stats             │
│  [Price] [High] [Low] [Vol] │
│                             │
└─────────────────────────────┘
  🏠 📡 👨‍🌾 🧑‍💼 🛒 👤
```

---

## 📋 Complete Checklist

### Pre-Run
- [ ] Flutter SDK downloaded & extracted (C:\flutter_sdk\flutter)
- [ ] Flutter added to PATH
- [ ] Android Studio installed
- [ ] Android SDK 21+ installed
- [ ] Android emulator created (or device connected)
- [ ] `flutter doctor` shows all green checkmarks

### Run Steps
- [ ] Emulator started: `emulator -avd Pixel_5_API_33`
- [ ] Navigate: `cd mobile_app_flutter`
- [ ] Get deps: `flutter pub get`
- [ ] Run app: `flutter run`
- [ ] See home screen with Intelligence Feed
- [ ] Click through all 6 tabs
- [ ] Verify no errors

### Verify Features
- [ ] Home tab: Intelligence Feed with 7 alerts
- [ ] Intelligence tab: Commodity selector, price chart, supply/demand
- [ ] Farmer Hub: 4 module cards (Crop Planning, Best Sell, Weather, Buyer)
- [ ] Trader Hub: 4 module cards (Supply, Demand, Arbitrage, Inventory)
- [ ] Marketplace: Buy/Sell tabs with order listing
- [ ] Profile: User stats and menu items

---

## 🆘 Troubleshooting

### Flutter not found after installation
```powershell
# Restart PowerShell/Terminal completely
# Or manually add to PATH:
$env:Path += ";C:\flutter_sdk\flutter\bin"

# Verify:
flutter --version
```

### Android SDK not found
```powershell
# Set ANDROID_SDK_ROOT
$env:ANDROID_SDK_ROOT = "C:\Android"  # or your path
flutter doctor
```

### Emulator won't start
```powershell
# 1. Check emulator exists:
emulator -list-avds

# 2. Start with verbose output:
emulator -avd Pixel_5_API_33 -verbose

# 3. Or use Android Studio GUI:
# Tools → Device Manager → Play button
```

### "Could not start emulator"
```powershell
# 1. Check Virtualization enabled (BIOS)
# 2. Check GPU support:
#    Android Studio → Settings → System Settings → GPU
#    Set to: Automatic or Software GLES 2.0

# 3. Clear emulator cache:
emulator -avd Pixel_5_API_33 -wipe-data
```

### App crashes on launch
```powershell
# Check logs:
flutter logs

# If dependencies issue:
flutter clean
flutter pub get
flutter run
```

### Gradle errors
```powershell
flutter clean
rm -r build android/.gradle
flutter pub get
flutter run
```

---

## 🎓 Learn Flutter Commands

```powershell
flutter --version              # Check version
flutter doctor                 # Diagnose setup
flutter doctor --android-licenses  # Accept licenses
flutter pub get                # Install dependencies
flutter build apk              # Build APK for testing
flutter build apk --release    # Build production APK
flutter run                    # Run app on device/emulator
flutter run --release          # Run in release mode
flutter clean                  # Clean build files
flutter logs                   # View app logs
```

---

## 📊 Performance Tips

### Speed up first run
```powershell
# Use release mode instead (faster, but not debuggable):
flutter run --release
```

### Improve emulator speed
1. Increase RAM in AVD config (2-4GB)
2. Enable GPU acceleration in Android Studio
3. Use Pixel device (not custom)
4. Close other apps

### Reduce APK size
```powershell
# Already optimized in pubspec.yaml
# Further optimization:
flutter build apk --split-per-abi
```

---

## 📁 Important Paths

```
C:\flutter_sdk\flutter\           # Flutter SDK root
C:\flutter_sdk\flutter\bin\       # Flutter executables
C:\Android\                        # Android SDK (optional location)
C:\Users\LENOVO\.gradle\          # Gradle cache
C:\Users\LENOVO\AppData\Local\Pub # Pub package cache
```

---

## ⏱️ Typical Timeline

| Step | Time |
|------|------|
| Flutter SDK download | 5-10 min |
| Android Studio + SDKs | 15-20 min |
| Create emulator | 5 min |
| Start emulator | 10-15 sec |
| `flutter pub get` | 1-2 min |
| First `flutter run` | 30-60 sec |
| **Total** | **30-50 min** |

---

## ✨ After App Runs Successfully

### Test All Features
```
1. Home tab → See 7 daily alerts
2. Intelligence tab → See market data
3. Farmer Hub → See 4 crop modules
4. Trader Hub → See 4 supply modules
5. Marketplace → See buy/sell orders
6. Profile → See user information
```

### Try Hot Reload
```powershell
# While app is running, press 'r' in terminal to hot reload
# Changes appear instantly (without restarting app)
```

### Next: Backend Integration
- Connect to API: https://api.croppulse.com/v1
- Replace mock data with real prices
- Implement OTP authentication
- Add push notifications

---

## 📞 Resources

**Official Documentation:**
- Flutter: https://flutter.dev/docs
- Dart: https://dart.dev/guides
- Android: https://developer.android.com/docs

**Troubleshooting:**
- Flutter Issues: https://github.com/flutter/flutter/issues
- Stack Overflow: Tag `flutter`

**Community:**
- Discord: https://discord.gg/flutter
- Twitter: @flutterdev

---

## 🎉 Success Indicator

When you see the **6 navigation tabs** at the bottom:
```
🏠 📡 👨‍🌾 🧑‍💼 🛒 👤
```

**You're ready for Phase 2 backend integration!** 🚀

---

**Last Updated:** May 15, 2026  
**Setup Time:** 30-50 minutes (first time)  
**Difficulty:** Medium (automated steps included)
