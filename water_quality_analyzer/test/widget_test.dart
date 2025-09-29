// This is a basic Flutter widget test.
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../lib/src/providers/water_quality_provider.dart';
import '../lib/src/providers/educational_module_provider.dart';
import '../lib/src/screens/auth/auth_screen.dart';

void main() {
  testWidgets('App starts with auth screen', (WidgetTester tester) async {
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();

    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider(create: (ctx) => WaterQualityProvider()),
          ChangeNotifierProvider(
            create: (ctx) => EducationalModuleProvider(prefs),
          ),
        ],
        child: const MaterialApp(
          home: AuthScreen(),
        ),
      ),
    );

    // Verify that the auth screen shows up
    expect(find.text('AarogyaJal'), findsOneWidget);
    expect(find.text('Your Smart Water Quality Companion'), findsOneWidget);
    expect(find.text('Log In'), findsOneWidget);
    expect(find.text('Sign Up'), findsOneWidget);
  });
}
