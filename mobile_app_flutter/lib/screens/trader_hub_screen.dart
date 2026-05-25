import 'package:flutter/material.dart';
import '../localization/app_strings.dart';
import '../theme/app_theme.dart';
import 'intelligence_screen.dart';
import 'marketplace_screen.dart';
import 'price_insight_screen.dart';

class TraderHubScreen extends StatelessWidget {
  const TraderHubScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final modules = <_TraderModule>[
      _TraderModule(
        icon: '📦',
        title: l10n.text('supply_visibility'),
        desc: l10n.text('supply_visibility_desc'),
        destinationBuilder: (_) => const MarketplaceScreen(),
      ),
      _TraderModule(
        icon: '🔍',
        title: l10n.text('demand_forecasting'),
        desc: l10n.text('demand_forecasting_desc'),
        destinationBuilder: (_) => const IntelligenceScreen(),
      ),
      _TraderModule(
        icon: '💰',
        title: l10n.text('regional_arbitrage'),
        desc: l10n.text('regional_arbitrage_desc'),
        destinationBuilder: (_) => const PriceInsightScreen(),
      ),
      _TraderModule(
        icon: '📊',
        title: l10n.text('inventory_tracking'),
        desc: l10n.text('inventory_tracking_desc'),
      ),
    ];

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
            ...modules.map((module) => _buildModuleCard(context, l10n, module)),
          ],
        ),
      ),
    );
  }

  Widget _buildModuleCard(BuildContext context, AppStrings l10n, _TraderModule module) {
    final isEnabled = module.destinationBuilder != null;

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
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(module.icon, style: const TextStyle(fontSize: 24)),
              const SizedBox(width: 12),
              Expanded(
                child: Text(module.title, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
              ),
            ],
          ),
          const SizedBox(height: 10),
          _AvailabilityPill(
            label: l10n.text(isEnabled ? 'available_now' : 'coming_soon'),
            color: isEnabled ? AppTheme.primaryBlue : AppTheme.warningOrange,
          ),
          const SizedBox(height: 8),
          Text(module.desc, style: const TextStyle(fontSize: 13, color: AppTheme.lightText)),
          const SizedBox(height: 12),
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: isEnabled ? AppTheme.primaryBlue : AppTheme.lightGray,
              minimumSize: const Size(double.infinity, 40),
            ),
            onPressed: !isEnabled
                ? null
                : () {
                    Navigator.of(context).push(
                      MaterialPageRoute(builder: module.destinationBuilder!),
                    );
                  },
            child: Text(
              l10n.text(isEnabled ? 'open' : 'coming_soon'),
              style: const TextStyle(color: Colors.white),
            ),
          ),
        ],
      ),
    );
  }
}

class _TraderModule {
  const _TraderModule({
    required this.icon,
    required this.title,
    required this.desc,
    this.destinationBuilder,
  });

  final String icon;
  final String title;
  final String desc;
  final WidgetBuilder? destinationBuilder;
}

class _AvailabilityPill extends StatelessWidget {
  const _AvailabilityPill({required this.label, required this.color});

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
