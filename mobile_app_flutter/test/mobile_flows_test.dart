import 'package:croppulse_mobile/localization/app_strings.dart';
import 'package:croppulse_mobile/main.dart';
import 'package:croppulse_mobile/models/app_update_info.dart';
import 'package:croppulse_mobile/models/auth_session.dart';
import 'package:croppulse_mobile/models/marketplace.dart';
import 'package:croppulse_mobile/providers/api_providers.dart';
import 'package:croppulse_mobile/providers/marketplace_provider.dart';
import 'package:croppulse_mobile/screens/login_screen.dart';
import 'package:croppulse_mobile/services/api_service.dart';
import 'package:croppulse_mobile/services/app_update_service.dart';
import 'package:croppulse_mobile/theme/app_theme.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() async {
    SharedPreferences.setMockInitialValues({});
  });

  testWidgets('login screen requests and verifies OTP with provider overrides', (tester) async {
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
        overrides: [apiServiceProvider.overrideWithValue(fakeApi)],
      ),
    );
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField).first, '9876543210');
    await tester.tap(find.text('Request OTP'));
    await tester.pumpAndSettle();

    expect(fakeApi.requestedPhones, ['9876543210']);
    expect(find.text('Verify OTP'), findsOneWidget);
    expect(find.textContaining('Use the mock code 123456 for now.'), findsOneWidget);

    await tester.enterText(find.byType(TextField).at(1), '123456');
    await tester.tap(find.text('Verify OTP'));
    await tester.pumpAndSettle();

    expect(fakeApi.verifiedOtps, ['123456']);
    expect(find.text('Signed in successfully.'), findsOneWidget);

    final preferences = await SharedPreferences.getInstance();
    expect(preferences.getString('auth_access_token'), 'test-token');
    expect(preferences.getString('auth_phone'), '+919876543210');
  });

  test('marketplace controller keeps guest listings and offers as local drafts', () async {
    final container = ProviderContainer();
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
    expect(marketplaceState.statusMessage, 'Preview mode: listing saved locally as a draft.');

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
    expect(marketplaceState.statusMessage, 'Preview mode: offer saved locally for later sync.');
  });

  testWidgets('main navigation shows an update prompt when a newer build is available', (tester) async {
    final fakeUpdateService = FakeAppUpdateService(
      update: const AppUpdateInfo(
        versionName: '1.0.3',
        versionCode: 5,
        downloadUrl: 'https://example.com/app-release.apk',
        playStoreUrl: 'https://play.google.com/store/apps/details?id=com.croppulse.mobile',
        releaseNotes: 'Fresh marketplace fixes and release wiring.',
      ),
    );

    await tester.pumpWidget(
      ProviderScope(
        child: MyApp(updateService: fakeUpdateService),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Update available'), findsOneWidget);
    expect(find.text('CropPulse 1.0.3 is ready to install.'), findsOneWidget);
    expect(find.text('Fresh marketplace fixes and release wiring.'), findsOneWidget);
    expect(find.text('Later'), findsOneWidget);
    expect(find.text('Open store'), findsOneWidget);
  });
}

Widget _buildTestApp(Widget child, {List<Override> overrides = const []}) {
  return ProviderScope(
    overrides: overrides,
    child: MaterialApp(
      onGenerateTitle: (context) => AppStrings.of(context).text('app_title'),
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      supportedLocales: AppStrings.supportedLocales,
      localizationsDelegates: const [AppStrings.delegate],
      home: child,
    ),
  );
}

class FakeApiService extends ApiService {
  FakeApiService({this.otpResult, this.session}) : super();

  final OtpRequestResult? otpResult;
  final AuthSession? session;
  final List<String> requestedPhones = <String>[];
  final List<String> verifiedOtps = <String>[];

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
  Future<AuthSession> verifyOtp({required String phoneNumber, required String otp}) async {
    verifiedOtps.add(otp);
    return session ??
        AuthSession(
          accessToken: 'fallback-token',
          tokenType: 'bearer',
          userId: 'fallback-user',
          phone: phoneNumber,
        );
  }
}

class FakeAppUpdateService extends AppUpdateService {
  FakeAppUpdateService({this.update, this.prompt = true})
      : super(
          metadataUrl: 'https://example.com/update.json',
          fallbackPlayStoreUrl: 'https://play.google.com/store/apps/details?id=com.croppulse.mobile',
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