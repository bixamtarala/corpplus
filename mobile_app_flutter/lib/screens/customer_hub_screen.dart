import 'package:flutter/material.dart';

import '../localization/app_strings.dart';
import '../theme/app_theme.dart';
import 'intelligence_screen.dart';
import 'marketplace_screen.dart';
import 'price_insight_screen.dart';

class CustomerHubScreen extends StatelessWidget {
  const CustomerHubScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text('🛍️ ${l10n.text('customer_hub_title')}'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              l10n.text('customer_buying_desk'),
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              l10n.text('customer_buying_desc'),
              style: const TextStyle(height: 1.4, color: AppTheme.lightText),
            ),
            const SizedBox(height: 20),
            _CustomerCard(
              icon: Icons.shopping_basket,
              title: l10n.text('customer_card_market_title'),
              description: l10n.text('customer_card_market_desc'),
            ),
            _CustomerCard(
              icon: Icons.verified_user,
              title: l10n.text('customer_card_buyers_title'),
              description: l10n.text('customer_card_buyers_desc'),
            ),
            _CustomerCard(
              icon: Icons.insights,
              title: l10n.text('customer_card_guidance_title'),
              description: l10n.text('customer_card_guidance_desc'),
            ),
            const SizedBox(height: 20),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(builder: (_) => const MarketplaceScreen()),
                  );
                },
                icon: const Icon(Icons.shopping_cart),
                label: Text(l10n.text('customer_marketplace_cta')),
              ),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(builder: (_) => const IntelligenceScreen()),
                  );
                },
                icon: const Icon(Icons.trending_up),
                label: Text(l10n.text('customer_intelligence_cta')),
              ),
            ),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton.icon(
                onPressed: () {
                  Navigator.of(context).push(
                    MaterialPageRoute(builder: (_) => const PriceInsightScreen()),
                  );
                },
                icon: const Icon(Icons.auto_graph),
                label: Text(l10n.text('customer_price_cta')),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _CustomerCard extends StatelessWidget {
  const _CustomerCard({
    required this.icon,
    required this.title,
    required this.description,
  });

  final IconData icon;
  final String title;
  final String description;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: AppTheme.lightGray),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: AppTheme.primaryGreen),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
                const SizedBox(height: 6),
                Text(description, style: const TextStyle(fontSize: 13, height: 1.35, color: AppTheme.lightText)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}