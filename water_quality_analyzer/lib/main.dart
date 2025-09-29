import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'src/providers/water_quality_provider.dart';
import 'src/providers/educational_module_provider.dart';
import 'src/screens/main_screen.dart';
import 'src/screens/animated_splash_screen.dart';
import 'src/screens/auth/login_screen.dart';
import 'src/screens/auth/auth_screen.dart';
import 'src/theme/app_theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<SharedPreferences>(
      future: SharedPreferences.getInstance(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const MaterialApp(
            home: Scaffold(
              body: Center(
                child: CircularProgressIndicator(),
              ),
            ),
          );
        }

        if (snapshot.hasError) {
          return MaterialApp(
            home: Scaffold(
              body: Center(
                child: Text('Error: ${snapshot.error}'),
              ),
            ),
          );
        }

        if (!snapshot.hasData) {
          return const MaterialApp(
            home: Scaffold(
              body: Center(
                child: Text('Failed to initialize preferences'),
              ),
            ),
          );
        }

        return MultiProvider(
          providers: [
            ChangeNotifierProvider(create: (ctx) => WaterQualityProvider()),
            ChangeNotifierProvider(
              create: (ctx) => EducationalModuleProvider(snapshot.data!),
            ),
          ],
          child: MaterialApp(
            title: 'AarogyaJal',
            theme: AppTheme.theme,
            initialRoute: '/',
            routes: {
              '/': (context) => AnimatedSplashScreen(
                    nextScreen: const AuthScreen(),
                  ),
              '/login': (context) => const LoginScreen(),
              '/home': (context) => const MainScreen(),
            },
          ),
        );
      },
    );
  }
}
