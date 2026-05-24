import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import 'localization/app_strings.dart';
import 'models/app_update_info.dart';
import 'screens/customer_hub_screen.dart';
import 'screens/farmer_hub_screen.dart';
import 'screens/home_screen.dart';
import 'screens/intelligence_screen.dart';
import 'screens/marketplace_screen.dart';
import 'screens/profile_screen.dart';
import 'screens/trader_hub_screen.dart';
import 'services/app_update_service.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final locale = ref.watch(appLocaleProvider);

    return MaterialApp(
      onGenerateTitle: (context) => AppStrings.of(context).text('app_title'),
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      locale: locale,
      supportedLocales: AppStrings.supportedLocales,
      localizationsDelegates: const [AppStrings.delegate],
      home: const NativeAppGate(),
    );
  }
}

class NativeAppGate extends ConsumerWidget {
  const NativeAppGate({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return const MainNavigationScreen();
  }
}

class SplashScreen extends StatelessWidget {
  const SplashScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: AppTheme.primaryGradient),
        child: const Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('🌾', style: TextStyle(fontSize: 56)),
              SizedBox(height: 12),
              Text(
                'CropPulse',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 30,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class MainNavigationScreen extends StatefulWidget {
  const MainNavigationScreen({super.key});

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  final AppUpdateService _updateService = AppUpdateService();

  int _selectedIndex = 0;
  bool _updateCheckStarted = false;

  static const List<Widget> _screens = [
    HomeScreen(),
    IntelligenceScreen(),
    FarmerHubScreen(),
    TraderHubScreen(),
    CustomerHubScreen(),
    MarketplaceScreen(),
    ProfileScreen(),
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkForAvailableUpdate();
    });
  }

  Future<void> _checkForAvailableUpdate() async {
    if (_updateCheckStarted) {
      return;
    }

    _updateCheckStarted = true;

    final update = await _updateService.getAvailableUpdate();
    if (!mounted || update == null) {
      return;
    }

    final shouldPrompt = await _updateService.shouldPromptForVersion(update.versionCode);
    if (!mounted || !shouldPrompt) {
      return;
    }

    await _showUpdateDialog(update);
  }

  Future<void> _showUpdateDialog(AppUpdateInfo update) async {
    await showDialog<void>(
      context: context,
      barrierDismissible: !update.forceUpdate,
      builder: (dialogContext) {
        return AlertDialog(
          title: const Text('Update available'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'CropPulse ${update.versionName} is ready to install.',
                style: const TextStyle(fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 12),
              Text(
                update.releaseNotes ?? 'A newer mobile build is available with the latest app changes.',
                style: const TextStyle(height: 1.4),
              ),
            ],
          ),
          actions: [
            if (!update.forceUpdate)
              TextButton(
                onPressed: () async {
                  await _updateService.dismissVersion(update.versionCode);
                  if (dialogContext.mounted) {
                    Navigator.of(dialogContext).pop();
                  }
                },
                child: const Text('Later'),
              ),
            ElevatedButton(
              onPressed: () async {
                await _openUpdate(update);
                if (!update.forceUpdate && dialogContext.mounted) {
                  Navigator.of(dialogContext).pop();
                }
              },
              child: Text(update.playStoreUrl != null ? 'Open store' : 'Download APK'),
            ),
          ],
        );
      },
    );
  }

  Future<void> _openUpdate(AppUpdateInfo update) async {
    final candidateUrls = <String>{
      if (update.playStoreUrl != null && update.playStoreUrl!.isNotEmpty) update.playStoreUrl!,
      update.downloadUrl,
    };

    for (final url in candidateUrls) {
      final uri = Uri.tryParse(url);
      if (uri == null) {
        continue;
      }

      if (await canLaunchUrl(uri)) {
        await launchUrl(uri, mode: LaunchMode.externalApplication);
        return;
      }
    }

    if (!mounted) {
      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Could not open the update link.')),
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);

    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        type: BottomNavigationBarType.fixed,
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home_outlined),
            activeIcon: Icon(Icons.home),
            label: l10n.text('nav_home'),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.trending_up_outlined),
            activeIcon: Icon(Icons.trending_up),
            label: l10n.text('nav_intelligence'),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.grass_outlined),
            activeIcon: Icon(Icons.grass),
            label: l10n.text('nav_farmer'),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.storefront_outlined),
            activeIcon: Icon(Icons.storefront),
            label: l10n.text('nav_trader'),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.shopping_bag_outlined),
            activeIcon: Icon(Icons.shopping_bag),
            label: l10n.text('nav_customer'),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.shopping_cart_outlined),
            activeIcon: Icon(Icons.shopping_cart),
            label: l10n.text('nav_market'),
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person_outline),
            activeIcon: Icon(Icons.person),
            label: l10n.text('nav_profile'),
          ),
        ],
      ),
    );
  }
}
