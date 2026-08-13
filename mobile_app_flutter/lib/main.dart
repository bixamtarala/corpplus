import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:url_launcher/url_launcher.dart';

import 'localization/app_strings.dart';
import 'models/app_update_info.dart';
import 'screens/cart_screen.dart';
import 'screens/categories_screen.dart';
import 'screens/commerce_account_screen.dart';
import 'screens/commerce_search_screen.dart';
import 'screens/home_screen.dart';
import 'services/app_update_service.dart';
import 'theme/app_theme.dart';

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key, this.updateService});

  final AppUpdateService? updateService;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final locale = ref.watch(appLocaleProvider);

    return MaterialApp(
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
      home: NativeAppGate(updateService: updateService),
    );
  }
}

class NativeAppGate extends ConsumerWidget {
  const NativeAppGate({super.key, this.updateService});

  final AppUpdateService? updateService;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return MainNavigationScreen(updateService: updateService);
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
  const MainNavigationScreen({super.key, this.updateService});

  final AppUpdateService? updateService;

  @override
  State<MainNavigationScreen> createState() => _MainNavigationScreenState();
}

class _MainNavigationScreenState extends State<MainNavigationScreen> {
  late final AppUpdateService _updateService;

  int _selectedIndex = 0;
  bool _updateCheckStarted = false;

  static const List<Widget> _screens = [
    HomeScreen(),
    CategoriesScreen(),
    CommerceSearchScreen(),
    CartScreen(),
    CommerceAccountScreen(),
  ];

  @override
  void initState() {
    super.initState();
    _updateService = widget.updateService ?? AppUpdateService();
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

    final shouldPrompt = await _updateService.shouldPromptForVersion(
      update.versionCode,
    );
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
                update.releaseNotes ??
                    'A newer mobile build is available with the latest app changes.',
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
              child: Text(
                update.playStoreUrl != null ? 'Open store' : 'Download APK',
              ),
            ),
          ],
        );
      },
    );
  }

  Future<void> _openUpdate(AppUpdateInfo update) async {
    final candidateUrls = <String>{
      if (update.playStoreUrl != null && update.playStoreUrl!.isNotEmpty)
        update.playStoreUrl!,
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
      bottomNavigationBar: NavigationBar(
        selectedIndex: _selectedIndex,
        onDestinationSelected: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: const Icon(Icons.home),
            label: l10n.text('nav_home'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.grid_view_outlined),
            selectedIcon: const Icon(Icons.grid_view),
            label: l10n.text('nav_categories'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.search),
            selectedIcon: const Icon(Icons.manage_search),
            label: l10n.text('nav_search'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.shopping_cart_outlined),
            selectedIcon: const Icon(Icons.shopping_cart),
            label: l10n.text('nav_cart'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.person_outline),
            selectedIcon: const Icon(Icons.person),
            label: l10n.text('nav_account'),
          ),
        ],
      ),
    );
  }
}
