import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:croppulse_mobile/main.dart';

void main() {
  testWidgets('shows startup mode selector by default', (
    WidgetTester tester,
  ) async {
    SharedPreferences.setMockInitialValues(<String, Object>{});

    await tester.pumpWidget(const MyApp());
    await tester.pumpAndSettle();

    expect(find.text('Choose how to open CropPulse'), findsOneWidget);
    expect(find.text('Open Native App'), findsOneWidget);
    expect(find.text('Open Web App'), findsOneWidget);
    expect(find.text('Last used: Native App'), findsOneWidget);
  });
}
