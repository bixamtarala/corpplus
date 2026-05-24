import 'package:flutter/material.dart';
import '../localization/app_strings.dart';
import '../theme/app_theme.dart';
import '../widgets/commodity_selector_field.dart';
import 'price_insight_screen.dart';

class IntelligenceScreen extends StatefulWidget {
  const IntelligenceScreen({super.key});

  @override
  State<IntelligenceScreen> createState() => _IntelligenceScreenState();
}

class _IntelligenceScreenState extends State<IntelligenceScreen> {
  String _selectedCommodity = 'Rice';

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text('📡 ${l10n.text('intelligence_title')}'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Commodity Selector
            CommoditySelectorField(
              value: _selectedCommodity,
              labelText: l10n.text('select_commodity'),
              onChanged: (value) {
                setState(() {
                  _selectedCommodity = value;
                });
              },
            ),
            const SizedBox(height: 24),

            // Price Chart Placeholder
            Container(
              height: 300,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.lightGray),
              ),
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.show_chart, size: 48, color: AppTheme.lightText),
                    const SizedBox(height: 12),
                    Text(l10n.text('price_chart_30_days'), style: const TextStyle(color: AppTheme.lightText)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.lightGray),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    l10n.text('ai_price_advisor'),
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    l10n.text('ai_price_advisor_desc'),
                    style: TextStyle(fontSize: 13, color: AppTheme.lightText, height: 1.4),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton.icon(
                    onPressed: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => PriceInsightScreen(initialCrop: _selectedCommodity),
                        ),
                      );
                    },
                    icon: const Icon(Icons.insights),
                    label: Text(l10n.text('open_price_advisor')),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Supply vs Demand
            Text('🔥 ${l10n.text('supply_vs_demand')}', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppTheme.lightGray),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(l10n.text('supply_level'), style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
                        const SizedBox(height: 8),
                        const Text('45%', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppTheme.primaryGreen)),
                        const SizedBox(height: 4),
                        Text(l10n.text('inventory_status'), style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
                      ],
                    ),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: AppTheme.lightGray),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(l10n.text('demand_level'), style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
                        const SizedBox(height: 8),
                        const Text('92%', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppTheme.primaryBlue)),
                        const SizedBox(height: 4),
                        Text(l10n.text('buyer_interest'), style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
