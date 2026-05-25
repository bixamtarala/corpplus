import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../theme/app_theme.dart';
import '../widgets/intelligence_card.dart';
import '../widgets/quick_stats.dart';
import 'price_insight_screen.dart';

class HomeScreen extends ConsumerStatefulWidget {
  const HomeScreen({super.key});

  @override
  ConsumerState<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends ConsumerState<HomeScreen> {
  static const List<String> _roles = ['Farmer', 'Trader', 'Customer', 'Exporter'];
  String _selectedRole = 'Farmer';

  Future<void> _showLanguageSelector(AppStrings l10n, Locale currentLocale) async {
    final selectedLocale = await showModalBottomSheet<Locale>(
      context: context,
      showDragHandle: true,
      builder: (sheetContext) {
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  l10n.text('select_language'),
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
                ),
                const SizedBox(height: 12),
                for (final item in AppStrings.supportedLocales)
                  ListTile(
                    contentPadding: EdgeInsets.zero,
                    leading: Icon(
                      item.languageCode == currentLocale.languageCode
                          ? Icons.radio_button_checked
                          : Icons.radio_button_off,
                      color: item.languageCode == currentLocale.languageCode
                          ? AppTheme.primaryGreen
                          : AppTheme.lightText,
                    ),
                    title: Text(l10n.languageLabel(item)),
                    onTap: () {
                      Navigator.of(sheetContext).pop(item);
                    },
                  ),
              ],
            ),
          ),
        );
      },
    );

    if (selectedLocale == null || !mounted) {
      return;
    }

    ref.read(appLocaleProvider.notifier).state = selectedLocale;
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final locale = ref.watch(appLocaleProvider);

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 12,
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('🌾', style: TextStyle(fontSize: 28)),
            const SizedBox(width: 10),
            Flexible(
              child: Text(
                l10n.text('app_title'),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            tooltip: l10n.text('select_language'),
            icon: const Icon(Icons.language, color: AppTheme.primaryBlue),
            onPressed: () => _showLanguageSelector(l10n, locale),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Center(
              child: Column(
                children: [
                  Text(l10n.text('daily_feed_title'),
                      style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Text(l10n.text('daily_feed_subtitle'),
                      style: const TextStyle(fontSize: 14, color: AppTheme.lightText)),
                ],
              ),
            ),
            const SizedBox(height: 20),
            Text(
              l10n.text('select_role'),
              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 10),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final role in _roles)
                  ChoiceChip(
                    label: Text(l10n.roleLabel(role)),
                    selected: role == _selectedRole,
                    onSelected: (_) {
                      setState(() {
                        _selectedRole = role;
                      });
                    },
                    selectedColor: AppTheme.primaryGreen.withValues(alpha: 0.15),
                    labelStyle: TextStyle(
                      color: role == _selectedRole ? AppTheme.primaryGreen : AppTheme.darkText,
                      fontWeight: role == _selectedRole ? FontWeight.w700 : FontWeight.w500,
                    ),
                    side: BorderSide(
                      color: role == _selectedRole ? AppTheme.primaryGreen : AppTheme.lightGray,
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 24),

            // Intelligence Alerts
            const IntelligenceAlerts(),
            const SizedBox(height: 24),

            // Quick Stats
            const QuickStats(),
            const SizedBox(height: 24),

            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                gradient: AppTheme.primaryGradient,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    l10n.text('need_recommendation'),
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    l10n.text('need_recommendation_desc'),
                    style: TextStyle(color: Colors.white, height: 1.4),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: AppTheme.primaryGreen,
                    ),
                    onPressed: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => const PriceInsightScreen(),
                        ),
                      );
                    },
                    child: Text(l10n.text('open_price_advisor')),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class IntelligenceAlerts extends StatelessWidget {
  const IntelligenceAlerts({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final alerts = [
      {
        'emoji': '📈',
        'title': l10n.text('alert_rice_title'),
        'subtitle': l10n.text('alert_rice_subtitle'),
        'action': l10n.text('alert_rice_action'),
        'severity': 'high',
      },
      {
        'emoji': '🔥',
        'title': l10n.text('alert_peak_title'),
        'subtitle': l10n.text('alert_peak_subtitle'),
        'action': l10n.text('alert_peak_action'),
        'severity': 'high',
      },
      {
        'emoji': '⛈️',
        'title': l10n.text('alert_rain_title'),
        'subtitle': l10n.text('alert_rain_subtitle'),
        'action': l10n.text('alert_rain_action'),
        'severity': 'medium',
      },
      {
        'emoji': '⏰',
        'title': l10n.text('alert_sell_title'),
        'subtitle': l10n.text('alert_sell_subtitle'),
        'action': l10n.text('alert_sell_action'),
        'severity': 'high',
      },
    ];

    return Column(
      children: alerts.map((alert) {
        return IntelligenceCard(
          emoji: alert['emoji'] as String,
          title: alert['title'] as String,
          subtitle: alert['subtitle'] as String,
          action: alert['action'] as String,
          severity: alert['severity'] as String,
        );
      }).toList(),
    );
  }
}
