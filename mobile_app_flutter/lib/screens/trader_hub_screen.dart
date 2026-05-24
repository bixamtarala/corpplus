import 'package:flutter/material.dart';
import '../localization/app_strings.dart';
import '../theme/app_theme.dart';

class TraderHubScreen extends StatelessWidget {
  const TraderHubScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text('🧑‍💼 ${l10n.text('trader_hub_title')}'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              l10n.text('procurement_intelligence'),
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            _buildModuleCard(l10n, '📦', l10n.text('supply_visibility'), l10n.text('supply_visibility_desc')),
            _buildModuleCard(l10n, '🔍', l10n.text('demand_forecasting'), l10n.text('demand_forecasting_desc')),
            _buildModuleCard(l10n, '💰', l10n.text('regional_arbitrage'), l10n.text('regional_arbitrage_desc')),
            _buildModuleCard(l10n, '📊', l10n.text('inventory_tracking'), l10n.text('inventory_tracking_desc')),
          ],
        ),
      ),
    );
  }

  Widget _buildModuleCard(AppStrings l10n, String icon, String title, String desc) {
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
              Text(icon, style: const TextStyle(fontSize: 24)),
              const SizedBox(width: 12),
              Expanded(
                child: Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(desc, style: const TextStyle(fontSize: 13, color: AppTheme.lightText)),
          const SizedBox(height: 12),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.primaryBlue,
              minimumSize: const Size(double.infinity, 40),
            ),
            onPressed: () {},
            child: Text(l10n.text('open'), style: const TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}
