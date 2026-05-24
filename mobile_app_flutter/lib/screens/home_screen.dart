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
          Padding(
            padding: const EdgeInsets.only(right: 8),
            child: PopupMenuButton<Locale>(
              tooltip: l10n.text('select_language'),
              onSelected: (value) {
                ref.read(appLocaleProvider.notifier).state = value;
              },
              itemBuilder: (context) => [
                for (final item in AppStrings.supportedLocales)
                  PopupMenuItem<Locale>(
                    value: item,
                    child: Row(
                      children: [
                        Expanded(child: Text(l10n.languageLabel(item))),
                        if (item.languageCode == locale.languageCode)
                          const Icon(Icons.check, size: 18, color: AppTheme.primaryGreen),
                      ],
                    ),
                  ),
              ],
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                decoration: BoxDecoration(
                  border: Border.all(color: AppTheme.primaryBlue),
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.white,
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.language, size: 16, color: AppTheme.primaryBlue),
                    const SizedBox(width: 6),
                    Text(
                      l10n.languageLabel(locale),
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: AppTheme.primaryBlue,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(right: 12),
            child: PopupMenuButton<String>(
              padding: EdgeInsets.zero,
              tooltip: l10n.text('select_role'),
              initialValue: _selectedRole,
              itemBuilder: (context) => [
                for (final role in _roles)
                  PopupMenuItem<String>(
                    value: role,
                    child: Row(
                      children: [
                        Expanded(child: Text(l10n.roleLabel(role))),
                        if (role == _selectedRole)
                          const Icon(
                            Icons.check,
                            size: 18,
                            color: AppTheme.primaryGreen,
                          ),
                      ],
                    ),
                  ),
              ],
              onSelected: (role) {
                setState(() {
                  _selectedRole = role;
                });
              },
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                decoration: BoxDecoration(
                  border: Border.all(color: AppTheme.primaryGreen),
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.white,
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.person, size: 16, color: AppTheme.primaryGreen),
                    const SizedBox(width: 6),
                    Text(
                      l10n.roleLabel(_selectedRole),
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: AppTheme.primaryGreen,
                      ),
                    ),
                    const SizedBox(width: 4),
                    const Icon(Icons.keyboard_arrow_down, size: 16, color: AppTheme.primaryGreen),
                  ],
                ),
              ),
            ),
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
