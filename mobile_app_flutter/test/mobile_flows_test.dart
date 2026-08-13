import 'package:croppulse_mobile/localization/app_strings.dart';
import 'package:croppulse_mobile/main.dart';
import 'package:croppulse_mobile/models/app_update_info.dart';
import 'package:croppulse_mobile/models/auth_session.dart';
import 'package:croppulse_mobile/models/commerce_api_models.dart';
import 'package:croppulse_mobile/models/marketplace.dart';
import 'package:croppulse_mobile/models/price_insight.dart';
import 'package:croppulse_mobile/providers/api_providers.dart';
import 'package:croppulse_mobile/providers/marketplace_provider.dart';
import 'package:croppulse_mobile/screens/farmer_profile_screen.dart';
import 'package:croppulse_mobile/screens/home_screen.dart';
import 'package:croppulse_mobile/screens/intelligence_screen.dart';
import 'package:croppulse_mobile/screens/login_screen.dart';
import 'package:croppulse_mobile/screens/marketplace_screen.dart';
import 'package:croppulse_mobile/screens/price_insight_screen.dart';
import 'package:croppulse_mobile/screens/trader_hub_screen.dart';
import 'package:croppulse_mobile/services/api_service.dart';
import 'package:croppulse_mobile/services/app_update_service.dart';
import 'package:croppulse_mobile/services/secure_storage_service.dart';
import 'package:croppulse_mobile/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late MemorySecureStorage secureStorage;

  setUp(() async {
    SharedPreferences.setMockInitialValues({});
    secureStorage = MemorySecureStorage();
  });

  testWidgets(
    'login screen requests and verifies OTP with provider overrides',
    (tester) async {
      final fakeApi = FakeApiService(
        otpResult: const OtpRequestResult(
          phone: '+919876543210',
          message: 'OTP sent',
          expiresInSeconds: 600,
        ),
        session: const AuthSession(
          accessToken: 'test-token',
          tokenType: 'bearer',
          userId: 'user-123',
          phone: '+919876543210',
        ),
      );

      await tester.pumpWidget(
        _buildTestApp(
          const LoginScreen(),
          overrides: [
            apiServiceProvider.overrideWithValue(fakeApi),
            secureStorageProvider.overrideWithValue(secureStorage),
          ],
        ),
      );
      await tester.pumpAndSettle();

      await tester.enterText(find.byType(TextField).first, '9876543210');
      await tester.tap(find.text('Request OTP'));
      await tester.pumpAndSettle();

      expect(fakeApi.requestedPhones, ['9876543210']);
      expect(find.text('Verify OTP'), findsOneWidget);
      expect(find.textContaining('OTP sent'), findsOneWidget);

      await tester.enterText(find.byType(TextField).at(1), '123456');
      await tester.tap(find.text('Verify OTP'));
      await tester.pumpAndSettle();

      expect(fakeApi.verifiedOtps, ['123456']);
      expect(find.text('Signed in successfully.'), findsOneWidget);

      expect(secureStorage.values['commerce_access_token'], 'test-token');
    },
  );

  test(
    'marketplace controller keeps guest listings and offers as local drafts',
    () async {
      final container = ProviderContainer(
        overrides: [secureStorageProvider.overrideWithValue(secureStorage)],
      );
      addTearDown(container.dispose);

      final controller = container.read(marketplaceControllerProvider.notifier);

      await controller.createListing(
        const MarketplaceListingRequest(
          cropId: 'rice_crop_1',
          quantityKg: 1000,
          qualityGrade: 'A',
          pricePerKg: 2400,
          availableDate: '2026-09-20',
          description: 'Guest draft listing',
        ),
      );

      var marketplaceState = container.read(marketplaceControllerProvider);
      expect(marketplaceState.sellOrders, hasLength(1));
      expect(marketplaceState.sellOrders.first.status, 'draft');
      expect(
        marketplaceState.statusMessage,
        'Preview mode: listing saved locally as a draft.',
      );

      await controller.makeOffer(
        const MarketplaceOfferRequest(
          listingId: 'listing-123',
          offeredPricePerKg: 2350,
          quantityKg: 500,
          pickupLocation: 'Erode, Tamil Nadu',
          message: 'Need pickup tomorrow',
        ),
      );

      marketplaceState = container.read(marketplaceControllerProvider);
      expect(marketplaceState.latestOffer, isNotNull);
      expect(marketplaceState.latestOffer!.status, 'draft');
      expect(
        marketplaceState.statusMessage,
        'Preview mode: offer saved locally for later sync.',
      );
    },
  );

  testWidgets(
    'main navigation shows an update prompt when a newer build is available',
    (tester) async {
      final fakeUpdateService = FakeAppUpdateService(
        update: const AppUpdateInfo(
          versionName: '1.0.3',
          versionCode: 5,
          downloadUrl: 'https://example.com/app-release.apk',
          playStoreUrl:
              'https://play.google.com/store/apps/details?id=com.croppulse.mobile',
          releaseNotes: 'Fresh marketplace fixes and release wiring.',
        ),
      );

      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            apiServiceProvider.overrideWithValue(FakeApiService()),
            secureStorageProvider.overrideWithValue(secureStorage),
          ],
          child: MyApp(updateService: fakeUpdateService),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Update available'), findsOneWidget);
      expect(find.text('CropPulse 1.0.3 is ready to install.'), findsOneWidget);
      expect(
        find.text('Fresh marketplace fixes and release wiring.'),
        findsOneWidget,
      );
      expect(find.text('Later'), findsOneWidget);
      expect(find.text('Open store'), findsOneWidget);
    },
  );

  testWidgets(
    'home screen language picker updates across repeated selections',
    (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            apiServiceProvider.overrideWithValue(FakeApiService()),
            secureStorageProvider.overrideWithValue(secureStorage),
          ],
          child: MyApp(updateService: FakeAppUpdateService(update: null)),
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Categories'), findsWidgets);

      await tester.tap(find.byIcon(Icons.language));
      await tester.pumpAndSettle();
      await tester.tap(find.text('Hindi'));
      await tester.pumpAndSettle();

      expect(find.text('श्रेणियाँ'), findsWidgets);

      await tester.tap(find.byIcon(Icons.language));
      await tester.pumpAndSettle();
      await tester.tap(find.text('तेलुगु'));
      await tester.pumpAndSettle();

      expect(find.text('వర్గాలు'), findsWidgets);

      await tester.tap(find.byIcon(Icons.language));
      await tester.pumpAndSettle();
      await tester.tap(find.text('ఇంగ్లీష్'));
      await tester.pumpAndSettle();

      expect(find.text('Categories'), findsWidgets);
    },
  );

  testWidgets(
    'commerce home fits categories and preview catalog on narrow screens',
    (tester) async {
      tester.view.physicalSize = const Size(360, 800);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);

      await tester.pumpWidget(
        _buildTestApp(
          const HomeScreen(),
          overrides: [apiServiceProvider.overrideWithValue(FakeApiService())],
        ),
      );
      await tester.pumpAndSettle();

      expect(find.text('Categories'), findsOneWidget);
      await tester.scrollUntilVisible(
        find.text('Available products'),
        300,
        scrollable: find.byType(Scrollable).first,
      );
      expect(find.text('Available products'), findsOneWidget);
      expect(find.text('Vegetables'), findsOneWidget);
      expect(tester.takeException(), isNull);
    },
  );

  testWidgets('trader hub fits localized cards on narrow screens', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(
      _buildTestApp(const TraderHubScreen(), locale: const Locale('te')),
    );
    await tester.pumpAndSettle();

    expect(find.text('ప్రోక్యూర్‌మెంట్ ఇంటెలిజెన్స్'), findsOneWidget);
    expect(find.text('సరఫరా విజిబిలిటీ'), findsOneWidget);
    expect(find.text('ఇప్పుడు అందుబాటులో ఉంది'), findsWidgets);
    expect(tester.takeException(), isNull);
  });

  testWidgets('marketplace fits filters and tabs on narrow localized screens', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    final fakeApi = FakeApiService(searchResults: const []);

    await tester.pumpWidget(
      _buildTestApp(
        const MarketplaceScreen(),
        locale: const Locale('te'),
        overrides: [apiServiceProvider.overrideWithValue(fakeApi)],
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('కొనుగోలు ఆర్డర్లు'), findsOneWidget);
    expect(find.text('అమ్మకపు ఆర్డర్లు'), findsOneWidget);
    expect(find.text('పంట'), findsOneWidget);
    expect(find.text('రాష్ట్ర ఫిల్టర్'), findsOneWidget);
    expect(find.text('లిస్టింగ్స్ సింక్ చేయండి'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets(
    'intelligence screen fits localized advisor and supply cards on narrow screens',
    (tester) async {
      tester.view.physicalSize = const Size(360, 800);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);

      await tester.pumpWidget(
        _buildTestApp(const IntelligenceScreen(), locale: const Locale('te')),
      );
      await tester.pumpAndSettle();

      expect(find.text('ఏఐ ప్రైస్ అడ్వైజర్'), findsOneWidget);
      expect(find.text('ప్రైస్ అడ్వైజర్ తెరవండి'), findsOneWidget);
      expect(find.textContaining('సరఫరా వర్సెస్ డిమాండ్'), findsOneWidget);
      expect(find.text('కొనుగోలుదారుల ఆసక్తి'), findsOneWidget);
      expect(tester.takeException(), isNull);
    },
  );

  testWidgets('farmer profile actions fit localized labels on narrow screens', (
    tester,
  ) async {
    tester.view.physicalSize = const Size(360, 800);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(
      _buildTestApp(const FarmerProfileScreen(), locale: const Locale('te')),
    );
    await tester.pumpAndSettle();

    expect(find.text('ప్రొఫైల్ సింక్ చేయండి'), findsOneWidget);
    expect(find.text('ప్రొఫైల్ సేవ్ చేయండి'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });

  testWidgets(
    'price insight fits localized hero and result tiles on narrow screens',
    (tester) async {
      tester.view.physicalSize = const Size(360, 800);
      tester.view.devicePixelRatio = 1.0;
      addTearDown(tester.view.resetPhysicalSize);
      addTearDown(tester.view.resetDevicePixelRatio);

      final fakeApi = FakeApiService(
        priceInsight: const PriceInsight(
          crop: 'Rice',
          recommendedPrice: 2650,
          marketTrend: 'పెరుగుతోంది',
          nearbyPrices: {'Warangal Mandi': 2620, 'Khammam Mandi': 2675},
          bestSellingTime: 'తదుపరి 48 గంటలు',
          analysis:
              'డిమాండ్ బలంగా ఉంది, కాబట్టి ధరల కదలికను గమనిస్తూ త్వరగా అమ్మడం మంచిది.',
          source: InsightSource.fallback,
        ),
      );

      await tester.pumpWidget(
        _buildTestApp(
          const PriceInsightScreen(initialCrop: 'Rice'),
          locale: const Locale('te'),
          overrides: [apiServiceProvider.overrideWithValue(fakeApi)],
        ),
      );
      await tester.pumpAndSettle();

      await tester.tap(find.text('సిఫార్సు తెమ్మండి'));
      await tester.pumpAndSettle();

      expect(find.text('లైవ్ అమ్మకాల మార్గదర్శకం'), findsOneWidget);
      expect(find.text('సమీప మార్కెట్లు'), findsOneWidget);
      expect(find.textContaining('అమ్మడానికి ఉత్తమ సమయం'), findsOneWidget);
      expect(find.text('మార్కెట్ ధోరణి'), findsOneWidget);
      expect(tester.takeException(), isNull);
    },
  );
}

Widget _buildTestApp(
  Widget child, {
  List<Override> overrides = const [],
  Locale? locale,
}) {
  return ProviderScope(
    overrides: [
      secureStorageProvider.overrideWithValue(MemorySecureStorage()),
      ...overrides,
    ],
    child: MaterialApp(
      onGenerateTitle: (context) => AppStrings.of(context).text('app_title'),
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      locale: locale,
      supportedLocales: AppStrings.supportedLocales,
      localizationsDelegates: const [
        AppStrings.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
      ],
      home: child,
    ),
  );
}

class FakeApiService extends ApiService {
  FakeApiService({
    this.otpResult,
    this.session,
    this.searchResults,
    this.priceInsight,
  }) : super();

  final OtpRequestResult? otpResult;
  final AuthSession? session;
  final List<MarketplaceSearchResult>? searchResults;
  final PriceInsight? priceInsight;
  final List<String> requestedPhones = <String>[];
  final List<String> verifiedOtps = <String>[];
  static const category = CommerceCategory(
    id: 'category-1',
    slug: 'vegetables',
    name: 'Vegetables',
  );
  static const sku = CommerceSku(
    id: 'sku-1',
    code: 'TOMATO-1KG',
    packQuantity: 1,
    unitOfMeasure: 'kg',
    minimumOrderQuantity: 1,
    quantityStep: 1,
    pricePaise: 4200,
  );
  static const product = CommerceProduct(
    id: 'product-1',
    slug: 'tomato',
    name: 'Tomato',
    category: category,
    skus: [sku],
  );
  static const emptyCart = CommerceCart(
    id: 'cart-1',
    ownerType: 'guest',
    guestToken: 'guest-token-which-is-long-enough-for-tests',
    version: 1,
    currency: 'INR',
    subtotalPaise: 0,
    itemCount: 0,
    validForCheckout: false,
    validationStatus: 'empty',
    issues: [],
    items: [],
  );

  @override
  Future<OtpRequestResult> requestOtp(String phoneNumber) async {
    requestedPhones.add(phoneNumber);
    return otpResult ??
        const OtpRequestResult(
          phone: '+910000000000',
          message: 'OTP sent',
          expiresInSeconds: 600,
        );
  }

  @override
  Future<AuthSession> verifyOtp({
    required String phoneNumber,
    required String otp,
  }) async {
    verifiedOtps.add(otp);
    return session ??
        AuthSession(
          accessToken: 'fallback-token',
          tokenType: 'bearer',
          userId: 'fallback-user',
          phone: phoneNumber,
        );
  }

  @override
  Future<CurrentCommerceUser> getCurrentCommerceUser(
    String accessToken,
  ) async => const CurrentCommerceUser(
    id: 'user-123',
    phone: '+919876543210',
    preferredLocale: 'en',
  );

  @override
  Future<List<CommerceCategory>> getCommerceCategories({
    required String locale,
  }) async => [
    CommerceCategory(
      id: category.id,
      slug: category.slug,
      name: locale == 'hi'
          ? 'सब्ज़ियाँ'
          : locale == 'te'
          ? 'కూరగాయలు'
          : category.name,
    ),
  ];

  @override
  Future<List<CommerceProduct>> getCommerceProducts({
    required String locale,
    String? category,
    String? query,
  }) async => [
    CommerceProduct(
      id: product.id,
      slug: product.slug,
      name: locale == 'hi'
          ? 'टमाटर'
          : locale == 'te'
          ? 'టమాటా'
          : product.name,
      category: CommerceCategory(
        id: FakeApiService.category.id,
        slug: FakeApiService.category.slug,
        name: locale == 'hi'
            ? 'सब्ज़ियाँ'
            : locale == 'te'
            ? 'కూరగాయలు'
            : FakeApiService.category.name,
      ),
      skus: product.skus,
    ),
  ];

  @override
  Future<CommerceCart> createGuestCart({String? pincode}) async => emptyCart;

  @override
  Future<CommerceCart> restoreCart({
    String? accessToken,
    String? guestToken,
  }) async => emptyCart;

  @override
  Future<List<MarketplaceSearchResult>> searchListings({
    required String crop,
    String? state,
    String? quality,
    double? maxPrice,
  }) async {
    return searchResults ?? const <MarketplaceSearchResult>[];
  }

  @override
  Future<PriceInsight> getPriceInsight(
    PriceInsightRequestPayload request,
  ) async {
    return priceInsight ??
        const PriceInsight(
          crop: 'Rice',
          recommendedPrice: 2500,
          marketTrend: 'stable',
          nearbyPrices: <String, double>{},
          bestSellingTime: 'Next 3-5 days',
          analysis: 'Fallback insight',
          source: InsightSource.fallback,
        );
  }
}

class FakeAppUpdateService extends AppUpdateService {
  FakeAppUpdateService({this.update, this.prompt = true})
    : super(
        metadataUrl: 'https://example.com/update.json',
        fallbackPlayStoreUrl:
            'https://play.google.com/store/apps/details?id=com.croppulse.mobile',
      );

  final AppUpdateInfo? update;
  final bool prompt;

  @override
  Future<AppUpdateInfo?> getAvailableUpdate() async => update;

  @override
  Future<bool> shouldPromptForVersion(int versionCode) async => prompt;

  @override
  Future<void> dismissVersion(int versionCode) async {}
}
