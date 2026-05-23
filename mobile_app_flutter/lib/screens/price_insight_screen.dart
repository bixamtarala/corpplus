import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../data/commodity_catalog.dart';
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
  static const List<String> _states = ['Tamil Nadu', 'Punjab', 'Karnataka'];

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
    final quantity = double.tryParse(_quantityController.text.trim());
    if (quantity == null || quantity <= 0) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Enter a valid quantity in kilograms.')),
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
    final currency = NumberFormat.currency(locale: 'en_IN', symbol: 'Rs ', decimalDigits: 0);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Price Advisor'),
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
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Live selling guidance',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 22,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  SizedBox(height: 8),
                  Text(
                    'Query the CropPulse Phase 2 intelligence API for recommended price, nearby mandi comparisons, and best selling window.',
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
          const Text(
            'Request inputs',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 16),
          CommoditySelectorField(
            value: _selectedCrop,
            labelText: 'Crop',
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
            decoration: const InputDecoration(labelText: 'State'),
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
              label: const Text('Fetch recommendation'),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInsightResult(PriceInsight insight, NumberFormat currency) {
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
            child: const Text(
              'Showing offline fallback data because the mobile app could not reach the API.',
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
                '${insight.crop} Recommendation',
                style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              Row(
                children: [
                  Expanded(
                    child: _MetricTile(
                      label: 'Recommended price',
                      value: '${currency.format(insight.recommendedPrice)}/kg',
                      color: AppTheme.primaryGreen,
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: _MetricTile(
                      label: 'Market trend',
                      value: insight.marketTrend,
                      color: AppTheme.primaryBlue,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Text(
                'Best selling time: ${insight.bestSellingTime}',
                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
              const SizedBox(height: 8),
              Text(
                insight.analysis,
                style: const TextStyle(fontSize: 13, color: AppTheme.lightText, height: 1.4),
              ),
              const SizedBox(height: 16),
              const Text(
                'Nearby markets',
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