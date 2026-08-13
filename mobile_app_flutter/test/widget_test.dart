import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:croppulse_mobile/main.dart';

void main() {
  testWidgets('launches directly into the native app shell', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const ProviderScope(child: MyApp()));
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
