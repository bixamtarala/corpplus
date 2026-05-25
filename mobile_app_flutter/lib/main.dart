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
      localizationsDelegates: const [AppStrings.delegate],
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
    final navItems = [
      _NavItem(
        icon: Icons.home_outlined,
        activeIcon: Icons.home,
        label: l10n.text('nav_home'),
      ),
      _NavItem(
        icon: Icons.trending_up_outlined,
        activeIcon: Icons.trending_up,
        label: l10n.text('nav_intelligence'),
      ),
      _NavItem(
        icon: Icons.grass_outlined,
        activeIcon: Icons.grass,
        label: l10n.text('nav_farmer'),
      ),
      _NavItem(
        icon: Icons.storefront_outlined,
        activeIcon: Icons.storefront,
        label: l10n.text('nav_trader'),
      ),
      _NavItem(
        icon: Icons.shopping_bag_outlined,
        activeIcon: Icons.shopping_bag,
        label: l10n.text('nav_customer'),
      ),
      _NavItem(
        icon: Icons.shopping_cart_outlined,
        activeIcon: Icons.shopping_cart,
        label: l10n.text('nav_market'),
      ),
      _NavItem(
        icon: Icons.person_outline,
        activeIcon: Icons.person,
        label: l10n.text('nav_profile'),
      ),
    ];

    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: _ScrollableNavigationBar(
        items: navItems,
        selectedIndex: _selectedIndex,
        onSelected: (index) {
          setState(() {
            _selectedIndex = index;
          });
        },
      ),
    );
  }
}

class _NavItem {
  const _NavItem({
    required this.icon,
    required this.activeIcon,
    required this.label,
  });

  final IconData icon;
  final IconData activeIcon;
  final String label;
}

class _ScrollableNavigationBar extends StatelessWidget {
  const _ScrollableNavigationBar({
    required this.items,
    required this.selectedIndex,
    required this.onSelected,
  });

  final List<_NavItem> items;
  final int selectedIndex;
  final ValueChanged<int> onSelected;

  @override
  Widget build(BuildContext context) {
    return Material(
      elevation: 12,
      color: Colors.white,
      child: SafeArea(
        top: false,
        child: SingleChildScrollView(
          scrollDirection: Axis.horizontal,
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
          child: Row(
            children: [
              for (var index = 0; index < items.length; index++)
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4),
                  child: _NavigationButton(
                    item: items[index],
                    selected: index == selectedIndex,
                    onTap: () => onSelected(index),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}

class _NavigationButton extends StatelessWidget {
  const _NavigationButton({
    required this.item,
    required this.selected,
    required this.onTap,
  });

  final _NavItem item;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: onTap,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 180),
          constraints: const BoxConstraints(minWidth: 92),
          padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(16),
            color: selected ? AppTheme.primaryGreen.withValues(alpha: 0.12) : Colors.white,
            border: Border.all(
              color: selected ? AppTheme.primaryGreen : AppTheme.lightGray,
            ),
          ),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                selected ? item.activeIcon : item.icon,
                color: selected ? AppTheme.primaryGreen : AppTheme.lightText,
                size: 22,
              ),
              const SizedBox(height: 4),
              Text(
                item.label,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(
                  fontSize: 11,
                  fontWeight: selected ? FontWeight.w700 : FontWeight.w500,
                  color: selected ? AppTheme.primaryGreen : AppTheme.lightText,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
