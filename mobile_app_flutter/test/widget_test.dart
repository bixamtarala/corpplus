import 'package:flutter_test/flutter_test.dart';

import 'package:croppulse_mobile/main.dart';

void main() {
  testWidgets('launches directly into the native app shell', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();

    expect(find.text('CropPulse'), findsOneWidget);
    expect(find.text('Home'), findsOneWidget);
    expect(find.text('Market'), findsOneWidget);
    expect(find.text('Choose how to open CropPulse'), findsNothing);
  });
}
