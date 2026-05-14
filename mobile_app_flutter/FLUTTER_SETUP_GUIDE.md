# CropPulse Mobile App - Flutter Android

**Status:** MVP Ready for Development  
**Platform:** Android (Primary), iOS Ready (Phase 2)  
**Framework:** Flutter + Dart  
**Target SDK:** Android 21+  
**Build Tools:** Gradle, Android Studio  

---

## 📁 Project Structure

```
mobile_app_flutter/
├── lib/
│   ├── main.dart                    # App entry point & navigation
│   ├── theme/
│   │   └── app_theme.dart           # Design system & colors
│   ├── screens/
│   │   ├── home_screen.dart         # Intelligence Feed
│   │   ├── intelligence_screen.dart  # Market Intelligence
│   │   ├── farmer_hub_screen.dart    # Crop Planning & Best Sell Time
│   │   ├── trader_hub_screen.dart    # Supply & Demand
│   │   ├── marketplace_screen.dart   # Buy/Sell Orders
│   │   └── profile_screen.dart       # User Profile
│   ├── widgets/
│   │   ├── intelligence_card.dart
│   │   └── quick_stats.dart
│   ├── models/
│   │   ├── user_model.dart
│   │   ├── order_model.dart
│   │   ├── price_model.dart
│   │   └── alert_model.dart
│   ├── services/
│   │   ├── api_service.dart         # REST API integration
│   │   ├── auth_service.dart        # OTP authentication
│   │   └── local_storage_service.dart
│   └── providers/
│       ├── auth_provider.dart
│       ├── order_provider.dart
│       └── price_provider.dart
├── android/
│   ├── app/
│   │   ├── build.gradle
│   │   └── src/main/
│   │       └── AndroidManifest.xml
│   └── gradle.properties
├── assets/
│   ├── images/
│   ├── icons/
│   └── fonts/
├── pubspec.yaml                    # Dependencies
└── README.md
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
1. **Flutter SDK** (3.10+)
   ```bash
   flutter --version
   ```

2. **Android Studio** with Android SDK (API 21+)

3. **Git**

### Setup Steps

#### 1️⃣ Clone the repository
```bash
cd c:\Users\LENOVO\Desktop\Agritech
git clone https://github.com/bixamtarala/corpplus.git
cd corpplus/mobile_app_flutter
```

#### 2️⃣ Install dependencies
```bash
flutter pub get
```

#### 3️⃣ Generate build files
```bash
flutter pub run build_runner build
```

#### 4️⃣ Run on emulator
```bash
# Start Android emulator first
emulator -avd Pixel_5_API_30

# Then run the app
flutter run
```

#### 5️⃣ Run on physical device
```bash
# Enable USB debugging on device
flutter run
```

---

## 🎯 Core Features (MVP Phase)

### 1. **Home Screen** (Intelligence Feed)
- ✅ Daily alerts (7 types)
- ✅ Quick stats (price, high, low, volatility)
- ✅ Role selector (Farmer/Trader/Exporter)
- ⏳ API integration for real data

### 2. **Intelligence Tab**
- ✅ Commodity selector
- ✅ Price chart placeholder
- ✅ Supply vs Demand display
- ⏳ Chart library integration (fl_chart)

### 3. **Farmer Hub**
- ✅ Crop Planning card
- ✅ Best Time to Sell card
- ✅ Weather Alerts card
- ✅ Buyer Discovery card
- ⏳ Detailed screens for each module

### 4. **Trader Hub**
- ✅ Supply Visibility card
- ✅ Demand Forecasting card
- ✅ Regional Arbitrage card
- ✅ Inventory Tracking card
- ⏳ Data integration

### 5. **Marketplace**
- ✅ Buy/Sell order tabs
- ✅ Order listing UI
- ✅ Order details screen
- ⏳ Smart matching algorithm integration

### 6. **Profile**
- ✅ User profile display
- ✅ Stats (trades, volume, rating)
- ✅ Menu items (edit, history, settings)
- ⏳ Firebase authentication

---

## 🔧 API Integration

### Backend API Endpoints (Phase 2)
```
Base URL: https://api.croppulse.com/v1

Authentication:
  POST   /auth/otp/request      # Request OTP
  POST   /auth/otp/verify       # Verify OTP & get token

Prices:
  GET    /prices/latest         # Current prices
  GET    /prices/history        # Historical data
  GET    /prices/forecast       # 7-day forecast

Orders:
  GET    /orders                # User's orders
  POST   /orders                # Create order
  GET    /orders/{id}           # Order details
  PUT    /orders/{id}           # Update order

Users:
  GET    /users/profile         # User profile
  PUT    /users/profile         # Update profile
  GET    /users/{id}            # Other user profile
```

### Example API Service
```dart
class ApiService {
  static const String baseUrl = 'https://api.croppulse.com/v1';
  final Dio dio = Dio();

  Future<List<PriceModel>> getPrices() async {
    try {
      final response = await dio.get('$baseUrl/prices/latest');
      return (response.data as List)
          .map((e) => PriceModel.fromJson(e))
          .toList();
    } catch (e) {
      throw Exception('Failed to fetch prices: $e');
    }
  }
}
```

---

## 📦 Build & Deployment

### Debug APK (Testing)
```bash
flutter build apk --debug
# Output: build/app/outputs/flutter-apk/app-debug.apk
```

### Release APK (Production)
```bash
# 1. Create keystore (one-time)
keytool -genkey -v -keystore ~/croppulse-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias croppulse-key

# 2. Build release APK
flutter build apk --release
# Output: build/app/outputs/flutter-apk/app-release.apk
```

### Release App Bundle (Google Play)
```bash
flutter build appbundle --release
# Output: build/app/outputs/bundle/release/app-release.aab
```

### Install on device
```bash
flutter install
# or
adb install -r build/app/outputs/flutter-apk/app-debug.apk
```

---

## 📊 Development Timeline (Phase 2)

### Week 1-2: Core Screens & Navigation
- ✅ Project setup & dependencies
- ✅ Home screen with Intelligence Feed
- ✅ Bottom navigation (6 tabs)
- ✅ Theme & styling

### Week 3-4: Authentication & API
- User OTP login flow
- Firebase authentication setup
- API service layer
- Token management

### Week 5-6: Features
- Farmer Hub full screens
- Trader Hub details
- Marketplace order flow
- Price forecast integration

### Week 7-8: Testing & Optimization
- Unit tests (business logic)
- Widget tests (UI)
- Integration tests (API)
- Performance optimization
- Security hardening

### Week 9-10: Launch Preparation
- Google Play Store setup
- App signing & release APK
- Beta testing (TestFlight/Play Console)
- Analytics integration

---

## 🔐 Security Checklist

- [ ] API calls over HTTPS only
- [ ] Sensitive data encrypted locally
- [ ] OTP tokens with 15-min expiry
- [ ] JWT token refresh mechanism
- [ ] No credentials in code/git
- [ ] Device fingerprinting for fraud detection
- [ ] Rate limiting on auth endpoints
- [ ] SSL pinning for API calls

---

## 📱 Testing Strategy

### Local Testing
```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/widgets/quick_stats_test.dart

# Generate coverage report
flutter test --coverage
```

### Manual Testing Checklist
- [ ] All 6 tabs load without errors
- [ ] Role selector works
- [ ] Back button behavior correct
- [ ] Network error handling
- [ ] Offline mode with cached data
- [ ] Push notification display
- [ ] Location permission prompts

---

## 📈 Performance Targets

| Metric | Target |
|--------|--------|
| App Size | < 30 MB |
| Startup Time | < 2s |
| List Scroll FPS | 60 FPS |
| API Response | < 1s |
| Memory Usage | < 100 MB |

---

## 🤝 Git Workflow

```bash
# Create feature branch
git checkout -b feature/farmer-hub-details

# Make changes and commit
git add .
git commit -m "feat: add crop planning details screen"

# Push to GitHub
git push origin feature/farmer-hub-details

# Create Pull Request on GitHub
# Wait for review & merge
```

---

## 📚 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| flutter_riverpod | 2.4.0 | State management |
| dio | 5.3.0 | HTTP client |
| go_router | 13.0.0 | Navigation |
| hive_flutter | 1.1.0 | Local storage |
| fl_chart | 0.64.0 | Charts & graphs |
| firebase_core | 2.24.0 | Firebase setup |

---

## ❓ Troubleshooting

### "Flutter SDK not found"
```bash
# Check Flutter installation
flutter doctor

# Update Flutter
flutter upgrade

# Set FLUTTER_ROOT environment variable
export FLUTTER_ROOT=/path/to/flutter
```

### "Android SDK not found"
```bash
# Launch Android Studio
android studio

# Go to SDK Manager and install Android SDK 21+
```

### "App won't build"
```bash
# Clean build
flutter clean
flutter pub get
flutter pub run build_runner build
flutter run
```

---

## 📞 Support & Resources

- **Flutter Docs:** https://flutter.dev/docs
- **Dart Docs:** https://dart.dev/guides
- **Firebase Setup:** https://firebase.google.com/docs/flutter/setup
- **Google Play Console:** https://play.google.com/console

---

## 🎉 Next Steps

1. ✅ Create GitHub branch: `mobile/flutter-android`
2. ✅ Push this codebase to GitHub
3. 🔄 Set up CI/CD pipeline for automated testing
4. 🔄 Deploy to Firebase Test Lab
5. 🔄 Conduct beta testing with 100 users
6. 🔄 Submit to Google Play Store

---

**Last Updated:** May 15, 2026  
**Version:** 1.0.0  
**Status:** Ready for Development
