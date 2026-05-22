import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import 'farmer_profile_screen.dart';
import 'price_insight_screen.dart';

class FarmerHubScreen extends StatelessWidget {
  const FarmerHubScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final modules = [
      {
        'icon': Icons.grass,
        'title': 'Crop Planning',
        'desc': 'Plan crops with profitability analysis',
      },
      {
        'icon': Icons.schedule,
        'title': 'Best Time to Sell',
        'desc': 'AI predicts optimal harvest date',
      },
      {
        'icon': Icons.cloud,
        'title': 'Weather Alerts',
        'desc': 'Real-time weather & disease alerts',
      },
      {
        'icon': Icons.people,
        'title': 'Buyer Discovery',
        'desc': 'Connect with verified buyers',
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('👨‍🌾 Farmer Hub'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Farmer Operating System',
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
                        if (module['title'] == 'Crop Planning') {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => const FarmerProfileScreen(),
                            ),
                          );
                          return;
                        }

                        if (module['title'] == 'Best Time to Sell') {
                          Navigator.of(context).push(
                            MaterialPageRoute(
                              builder: (_) => const PriceInsightScreen(),
                            ),
                          );
                          return;
                        }
                      },
                      child: const Text('Open', style: TextStyle(color: Colors.white)),
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
