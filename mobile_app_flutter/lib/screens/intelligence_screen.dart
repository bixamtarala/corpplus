import 'package:flutter/material.dart';
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
    return Scaffold(
      appBar: AppBar(
        title: const Text('📡 Market Intelligence'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Commodity Selector
            CommoditySelectorField(
              value: _selectedCommodity,
              labelText: 'Select Commodity',
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
              child: const Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.show_chart, size: 48, color: AppTheme.lightText),
                    SizedBox(height: 12),
                    Text('Price Chart (30 Days)', style: TextStyle(color: AppTheme.lightText)),
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
                  const Text(
                    'AI Price Advisor',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Request a crop-specific recommendation from the Phase 2 intelligence API, including nearby mandi prices and best selling time.',
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
                    label: const Text('Open Price Advisor'),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Supply vs Demand
            const Text('🔥 Supply vs Demand', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
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
                        const Text('Supply Level', style: TextStyle(fontSize: 12, color: AppTheme.lightText)),
                        const SizedBox(height: 8),
                        const Text('45%', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppTheme.primaryGreen)),
                        const SizedBox(height: 4),
                        Text('Inventory status', style: TextStyle(fontSize: 12, color: AppTheme.lightText)),
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
                        const Text('Demand Level', style: TextStyle(fontSize: 12, color: AppTheme.lightText)),
                        const SizedBox(height: 8),
                        const Text('92%', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: AppTheme.primaryBlue)),
                        const SizedBox(height: 4),
                        Text('Buyer interest', style: TextStyle(fontSize: 12, color: AppTheme.lightText)),
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
