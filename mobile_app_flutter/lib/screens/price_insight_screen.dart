import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../data/commodity_catalog.dart';
import '../localization/app_strings.dart';
import '../models/price_insight.dart';
import '../providers/api_providers.dart';
import '../theme/app_theme.dart';
import '../widgets/commodity_selector_field.dart';

class PriceInsightScreen extends ConsumerStatefulWidget {
  const PriceInsightScreen({super.key, this.initialCrop});

  final String? initialCrop;

  @override
  ConsumerState<PriceInsightScreen> createState() => _PriceInsightScreenState();
}

class _PriceInsightScreenState extends ConsumerState<PriceInsightScreen> {
  static final List<String> _crops = CommodityCatalog.all;
  static final List<String> _states = CommodityCatalog.allStates;

  final TextEditingController _quantityController = TextEditingController(text: '500');
  String _selectedCrop = _crops.first;
  String _selectedState = _states.first;
  bool _isLoading = false;
  PriceInsight? _insight;

  @override
  void initState() {
    super.initState();
    final initialCrop = widget.initialCrop;
    if (initialCrop != null && _crops.contains(initialCrop)) {
      _selectedCrop = initialCrop;
    }
  }

  Future<void> _fetchInsight() async {
    final l10n = AppStrings.of(context);
    final quantity = double.tryParse(_quantityController.text.trim());
    if (quantity == null || quantity <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(l10n.text('enter_valid_quantity'))),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    final request = PriceInsightRequestPayload(
      crop: _selectedCrop,
      quantityKg: quantity,
      state: _selectedState,
    );

    final insight = await ref.read(apiServiceProvider).getPriceInsight(request);

    if (!mounted) {
      return;
    }

    setState(() {
      _insight = insight;
      _isLoading = false;
    });
  }

  @override
  void dispose() {
    _quantityController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final currency = NumberFormat.currency(locale: 'en_IN', symbol: 'Rs ', decimalDigits: 0);

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.text('price_advisor_title')),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                gradient: AppTheme.blueGradient,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    l10n.text('live_selling_guidance'),
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    l10n.text('live_selling_guidance_desc'),
                    style: TextStyle(color: Colors.white, height: 1.4),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),
            _buildFormCard(),
            const SizedBox(height: 24),
            if (_isLoading)
              const Center(child: CircularProgressIndicator())
            else if (_insight != null)
              _buildInsightResult(_insight!, currency),
          ],
        ),
      ),
    );
  }

  Widget _buildFormCard() {
    final l10n = AppStrings.of(context);
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.lightGray),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            l10n.text('request_inputs'),
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          CommoditySelectorField(
            value: _selectedCrop,
            labelText: l10n.text('crop'),
            onChanged: (value) {
              setState(() {
                _selectedCrop = value;
              });
            },
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<String>(
            initialValue: _selectedState,
            items: _states
                .map((state) => DropdownMenuItem<String>(value: state, child: Text(state)))
                .toList(),
            decoration: InputDecoration(labelText: l10n.text('state')),
            onChanged: (value) {
              if (value == null) {
                return;
              }

              setState(() {
                _selectedState = value;
              });
            },
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _quantityController,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: const InputDecoration(
              labelText: 'Quantity (kg)',
              hintText: '500',
            ),
          ),
          const SizedBox(height: 16),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _isLoading ? null : _fetchInsight,
              icon: const Icon(Icons.auto_graph),
              label: Text(l10n.text('fetch_recommendation')),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInsightResult(PriceInsight insight, NumberFormat currency) {
    final l10n = AppStrings.of(context);
    final sortedMarkets = insight.nearbyPrices.entries.toList()
      ..sort((left, right) => right.value.compareTo(left.value));

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (insight.source == InsightSource.fallback)
          Container(
            width: double.infinity,
            margin: const EdgeInsets.only(bottom: 16),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppTheme.warningOrange.withValues(alpha: 0.12),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              l10n.text('offline_fallback'),
              style: TextStyle(color: AppTheme.darkText),
            ),
          ),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: AppTheme.lightGray),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                l10n.text('recommendation_suffix', params: {'crop': insight.crop}),
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: _MetricTile(
                      label: l10n.text('recommended_price'),
                      value: '${currency.format(insight.recommendedPrice)}/kg',
                      color: AppTheme.primaryGreen,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _MetricTile(
                      label: l10n.text('market_trend'),
                      value: insight.marketTrend,
                      color: AppTheme.primaryBlue,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Text(
                l10n.text('best_selling_time', params: {'value': insight.bestSellingTime}),
                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 8),
              Text(
                insight.analysis,
                style: const TextStyle(fontSize: 13, color: AppTheme.lightText, height: 1.4),
              ),
              const SizedBox(height: 16),
              Text(
                l10n.text('nearby_markets'),
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              ...sortedMarkets.map((entry) {
                return Container(
                  margin: const EdgeInsets.only(bottom: 10),
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(entry.key, style: const TextStyle(fontWeight: FontWeight.w600)),
                      Text(currency.format(entry.value)),
                    ],
                  ),
                );
              }),
            ],
          ),
        ),
      ],
    );
  }
}

class _MetricTile extends StatelessWidget {
  const _MetricTile({
    required this.label,
    required this.value,
    required this.color,
  });

  final String label;
  final String value;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(label, style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
          const SizedBox(height: 8),
          Text(
            value,
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: color),
          ),
        ],
      ),
    );
  }
}