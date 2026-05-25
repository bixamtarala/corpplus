import 'package:flutter/material.dart';
import '../localization/app_strings.dart';
import '../theme/app_theme.dart';
import 'intelligence_screen.dart';
import 'marketplace_screen.dart';
import 'farmer_profile_screen.dart';
import 'price_insight_screen.dart';

class FarmerHubScreen extends StatelessWidget {
  const FarmerHubScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final modules = <_HubModule>[
      _HubModule(
        icon: Icons.grass,
        title: l10n.text('crop_planning'),
        desc: l10n.text('crop_planning_desc'),
        destinationBuilder: (_) => const FarmerProfileScreen(),
      ),
      _HubModule(
        icon: Icons.schedule,
        title: l10n.text('best_time_sell'),
        desc: l10n.text('best_time_sell_desc'),
        destinationBuilder: (_) => const PriceInsightScreen(),
      ),
      _HubModule(
        icon: Icons.cloud,
        title: l10n.text('weather_alerts'),
        desc: l10n.text('weather_alerts_desc'),
        destinationBuilder: (_) => const IntelligenceScreen(),
      ),
      _HubModule(
        icon: Icons.people,
        title: l10n.text('buyer_discovery'),
        desc: l10n.text('buyer_discovery_desc'),
        destinationBuilder: (_) => const MarketplaceScreen(),
      ),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text('👨‍🌾 ${l10n.text('farmer_hub_title')}'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              l10n.text('farmer_operating_system'),
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            ...modules.map((module) {
              return Container(
                margin: const EdgeInsets.only(bottom: 12),
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppTheme.lightGray),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(module.icon, size: 28, color: AppTheme.primaryGreen),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            module.title,
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                          ),
                        ),
                        _AvailabilityPill(label: l10n.text('available_now')),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      module.desc,
                      style: const TextStyle(fontSize: 13, color: AppTheme.lightText),
                    ),
                    const SizedBox(height: 12),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.primaryGreen,
                        minimumSize: const Size(double.infinity, 40),
                      ),
                      onPressed: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(builder: module.destinationBuilder),
                        );
                      },
                      child: Text(l10n.text('open'), style: const TextStyle(color: Colors.white)),
                    ),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }
}

class _HubModule {
  const _HubModule({
    required this.icon,
    required this.title,
    required this.desc,
    required this.destinationBuilder,
  });

  final IconData icon;
  final String title;
  final String desc;
  final WidgetBuilder destinationBuilder;
}

class _AvailabilityPill extends StatelessWidget {
  const _AvailabilityPill({required this.label, this.color = AppTheme.primaryGreen});

  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 12,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}
