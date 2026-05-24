import 'package:flutter/material.dart';
import '../localization/app_strings.dart';
import '../theme/app_theme.dart';
import 'farmer_profile_screen.dart';
import 'price_insight_screen.dart';

class FarmerHubScreen extends StatelessWidget {
  const FarmerHubScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final modules = [
      {
        'icon': Icons.grass,
        'title': l10n.text('crop_planning'),
        'desc': l10n.text('crop_planning_desc'),
      },
      {
        'icon': Icons.schedule,
        'title': l10n.text('best_time_sell'),
        'desc': l10n.text('best_time_sell_desc'),
      },
      {
        'icon': Icons.cloud,
        'title': l10n.text('weather_alerts'),
        'desc': l10n.text('weather_alerts_desc'),
      },
      {
        'icon': Icons.people,
        'title': l10n.text('buyer_discovery'),
        'desc': l10n.text('buyer_discovery_desc'),
      },
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
                        Icon(module['icon'] as IconData, size: 28, color: AppTheme.primaryGreen),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            module['title'] as String,
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    Text(
                      module['desc'] as String,
                      style: const TextStyle(fontSize: 13, color: AppTheme.lightText),
                    ),
                    const SizedBox(height: 12),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppTheme.primaryGreen,
                        minimumSize: const Size(double.infinity, 40),
                      ),
                      onPressed: () {
                        if (module['title'] == l10n.text('crop_planning')) {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => const FarmerProfileScreen(),
                            ),
                          );
                          return;
                        }

                        if (module['title'] == l10n.text('best_time_sell')) {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => const PriceInsightScreen(),
                            ),
                          );
                          return;
                        }
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
