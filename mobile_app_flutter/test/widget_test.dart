import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:croppulse_mobile/main.dart';
import 'package:croppulse_mobile/models/commerce_api_models.dart';
import 'package:croppulse_mobile/providers/api_providers.dart';
import 'package:croppulse_mobile/services/api_service.dart';
import 'package:croppulse_mobile/services/secure_storage_service.dart';

void main() {
  testWidgets('launches directly into the native app shell', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          apiServiceProvider.overrideWithValue(_ShellApi()),
          secureStorageProvider.overrideWithValue(MemorySecureStorage()),
        ],
        child: const MyApp(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('CropPulse'), findsOneWidget);
    expect(find.text('Home'), findsOneWidget);
    expect(find.text('Categories'), findsWidgets);
    expect(find.text('Search'), findsOneWidget);
    expect(find.text('Cart'), findsOneWidget);
    expect(find.text('Account'), findsOneWidget);
    expect(find.text('Choose how to open CropPulse'), findsNothing);
  });
}

class _ShellApi extends ApiService {
  @override
  Future<List<CommerceCategory>> getCommerceCategories({
    required String locale,
  }) async => const [
    CommerceCategory(id: '1', slug: 'vegetables', name: 'Vegetables'),
  ];
  @override
  Future<List<CommerceProduct>> getCommerceProducts({
    required String locale,
    String? category,
    String? query,
  }) async => const [];
  @override
  Future<CommerceCart> createGuestCart({String? pincode}) async =>
      const CommerceCart(
        id: 'cart',
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
}
