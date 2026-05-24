import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../localization/app_strings.dart';
import '../models/marketplace.dart';
import '../providers/marketplace_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/commodity_selector_field.dart';

class MarketplaceScreen extends ConsumerStatefulWidget {
  const MarketplaceScreen({super.key});

  @override
  ConsumerState<MarketplaceScreen> createState() => _MarketplaceScreenState();
}

class _MarketplaceScreenState extends ConsumerState<MarketplaceScreen>
    with SingleTickerProviderStateMixin {
  final TextEditingController _stateFilterController = TextEditingController(text: 'Tamil Nadu');
  late TabController _tabController;
  String _selectedCrop = 'Rice';

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    Future.microtask(() {
      ref.read(marketplaceControllerProvider.notifier).loadBuyOrders(crop: _selectedCrop, stateFilter: _stateFilterController.text.trim());
    });
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final marketplaceState = ref.watch(marketplaceControllerProvider);

    return Scaffold(
      appBar: AppBar(
        title: Text('🛒 ${l10n.text('marketplace_title')}'),
        bottom: TabBar(
          controller: _tabController,
          tabs: [
            Tab(text: l10n.text('buy_orders')),
            Tab(text: l10n.text('sell_orders')),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildBuyOrdersTab(marketplaceState),
          _buildSellOrdersTab(marketplaceState),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _showCreateListingSheet(context),
        backgroundColor: AppTheme.primaryGreen,
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildBuyOrdersTab(MarketplaceState marketplaceState) {
    final l10n = AppStrings.of(context);
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 0),
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppTheme.primaryGreen.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              l10n.text('customer_buy_banner'),
              style: const TextStyle(height: 1.35, color: AppTheme.darkText),
            ),
          ),
        ),
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
          child: Row(
            children: [
              Expanded(
                child: CommoditySelectorField(
                  value: _selectedCrop,
                  labelText: l10n.text('crop'),
                  onChanged: (value) {
                    setState(() {
                      _selectedCrop = value;
                    });
                  },
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: TextField(
                  controller: _stateFilterController,
                  decoration: InputDecoration(labelText: l10n.text('state_filter')),
                ),
              ),
            ],
          ),
        ),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: marketplaceState.isLoadingBuyOrders
                  ? null
                  : () {
                      ref.read(marketplaceControllerProvider.notifier).loadBuyOrders(
                            crop: _selectedCrop,
                            stateFilter: _stateFilterController.text.trim(),
                          );
                    },
              icon: const Icon(Icons.sync),
              label: Text(l10n.text('sync_listings')),
            ),
          ),
        ),
        if (marketplaceState.errorMessage != null)
          _StatusBanner(message: marketplaceState.errorMessage!, color: AppTheme.errorRed),
        if (marketplaceState.statusMessage != null)
          _StatusBanner(message: marketplaceState.statusMessage!, color: AppTheme.successGreen),
        Expanded(
          child: marketplaceState.isLoadingBuyOrders
              ? const Center(child: CircularProgressIndicator())
              : ListView(
                  padding: const EdgeInsets.all(16),
                  children: marketplaceState.buyOrders
                      .map((order) => _BuyOrderCard(
                            order: order,
                            onMakeOffer: () => _showMakeOfferSheet(context, order),
                          ))
                      .toList(),
                ),
        ),
      ],
    );
  }

  Widget _buildSellOrdersTab(MarketplaceState marketplaceState) {
    final l10n = AppStrings.of(context);
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        if (marketplaceState.sellOrders.isEmpty)
          Container(
            padding: const EdgeInsets.all(18),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: AppTheme.lightGray),
            ),
            child: Text(
              l10n.text('no_live_sell_listings'),
              style: TextStyle(height: 1.4),
            ),
          ),
        ...marketplaceState.sellOrders.map((listing) => _SellOrderCard(listing: listing)),
      ],
    );
  }

  Future<void> _showCreateListingSheet(BuildContext context) async {
    final l10n = AppStrings.of(context);
    final cropController = TextEditingController(text: 'rice_crop_1');
    final quantityController = TextEditingController(text: '1000');
    final qualityController = TextEditingController(text: 'A');
    final priceController = TextEditingController(text: '2400');
    final dateController = TextEditingController(text: '2026-09-20');
    final descriptionController = TextEditingController();

    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (context) {
        return Padding(
          padding: EdgeInsets.fromLTRB(16, 16, 16, 16 + MediaQuery.of(context).viewInsets.bottom),
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(l10n.text('create_listing'), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                TextField(controller: cropController, decoration: InputDecoration(labelText: l10n.text('crop_id'))),
                const SizedBox(height: 12),
                TextField(controller: quantityController, decoration: InputDecoration(labelText: l10n.text('quantity_kg')), keyboardType: const TextInputType.numberWithOptions(decimal: true)),
                const SizedBox(height: 12),
                TextField(controller: qualityController, decoration: InputDecoration(labelText: l10n.text('quality_grade'))),
                const SizedBox(height: 12),
                TextField(controller: priceController, decoration: InputDecoration(labelText: l10n.text('price_per_kg')), keyboardType: const TextInputType.numberWithOptions(decimal: true)),
                const SizedBox(height: 12),
                TextField(controller: dateController, decoration: InputDecoration(labelText: l10n.text('available_date'))),
                const SizedBox(height: 12),
                TextField(controller: descriptionController, decoration: InputDecoration(labelText: l10n.text('description'))),
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () {
                      final quantity = double.tryParse(quantityController.text.trim());
                      final price = double.tryParse(priceController.text.trim());
                      if (quantity == null || price == null) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text(l10n.text('enter_valid_quantity_price'))),
                        );
                        return;
                      }

                      ref.read(marketplaceControllerProvider.notifier).createListing(
                            MarketplaceListingRequest(
                              cropId: cropController.text.trim(),
                              quantityKg: quantity,
                              qualityGrade: qualityController.text.trim(),
                              pricePerKg: price,
                              availableDate: dateController.text.trim(),
                              description: descriptionController.text.trim().isEmpty ? null : descriptionController.text.trim(),
                            ),
                          );
                      Navigator.of(context).pop();
                    },
                    child: Text(l10n.text('publish_listing')),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Future<void> _showMakeOfferSheet(BuildContext context, MarketplaceSearchResult order) async {
    final l10n = AppStrings.of(context);
    final priceController = TextEditingController(text: order.pricePerKg.toStringAsFixed(0));
    final quantityController = TextEditingController(text: order.quantityKg.toStringAsFixed(0));
    final pickupController = TextEditingController(text: '${order.district}, ${order.state}');
    final messageController = TextEditingController(text: l10n.text('ready_to_purchase'));

    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (context) {
        return Padding(
          padding: EdgeInsets.fromLTRB(16, 16, 16, 16 + MediaQuery.of(context).viewInsets.bottom),
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(l10n.text('make_offer_for', params: {'crop': order.crop}), style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                TextField(controller: priceController, decoration: InputDecoration(labelText: l10n.text('offer_price_per_kg')), keyboardType: const TextInputType.numberWithOptions(decimal: true)),
                const SizedBox(height: 12),
                TextField(controller: quantityController, decoration: InputDecoration(labelText: l10n.text('quantity_kg')), keyboardType: const TextInputType.numberWithOptions(decimal: true)),
                const SizedBox(height: 12),
                TextField(controller: pickupController, decoration: InputDecoration(labelText: l10n.text('pickup_location'))),
                const SizedBox(height: 12),
                TextField(controller: messageController, decoration: InputDecoration(labelText: l10n.text('message'))),
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () {
                      final price = double.tryParse(priceController.text.trim());
                      final quantity = double.tryParse(quantityController.text.trim());
                      if (price == null || quantity == null) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text(l10n.text('enter_valid_offer_quantity'))),
                        );
                        return;
                      }

                      ref.read(marketplaceControllerProvider.notifier).makeOffer(
                            MarketplaceOfferRequest(
                              listingId: order.listingId,
                              offeredPricePerKg: price,
                              quantityKg: quantity,
                              pickupLocation: pickupController.text.trim(),
                              message: messageController.text.trim().isEmpty ? null : messageController.text.trim(),
                            ),
                          );
                      Navigator.of(context).pop();
                    },
                    child: Text(l10n.text('submit_offer')),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  @override
  void dispose() {
    _stateFilterController.dispose();
    _tabController.dispose();
    super.dispose();
  }
}

class _BuyOrderCard extends StatelessWidget {
  const _BuyOrderCard({required this.order, required this.onMakeOffer});

  final MarketplaceSearchResult order;
  final VoidCallback onMakeOffer;

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final currency = NumberFormat.currency(locale: 'en_IN', symbol: '₹', decimalDigits: 0);
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
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(
                  '${order.crop} - ${order.quantityKg.toStringAsFixed(0)} kg',
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: AppTheme.primaryGreen.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Text(
                  order.qualityGrade,
                  style: const TextStyle(fontSize: 12, color: AppTheme.primaryGreen, fontWeight: FontWeight.w600),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(l10n.text('seller', params: {'name': order.farmerName}), style: const TextStyle(fontWeight: FontWeight.w600)),
          const SizedBox(height: 4),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('${currency.format(order.pricePerKg)}/kg', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
              Text('${order.district}, ${order.state}', style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
            ],
          ),
          const SizedBox(height: 4),
          Text(l10n.text('available', params: {'value': order.availableDate}), style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
          const SizedBox(height: 12),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, minimumSize: const Size(double.infinity, 36)),
            onPressed: onMakeOffer,
            child: Text(l10n.text('make_offer'), style: const TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }
}

class _SellOrderCard extends StatelessWidget {
  const _SellOrderCard({required this.listing});

  final MarketplaceListing listing;

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final currency = NumberFormat.currency(locale: 'en_IN', symbol: '₹', decimalDigits: 0);
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
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(listing.cropId, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
              Text(listing.status, style: const TextStyle(fontSize: 12, color: AppTheme.primaryGreen, fontWeight: FontWeight.w600)),
            ],
          ),
          const SizedBox(height: 8),
          Text('${listing.quantityKg.toStringAsFixed(0)} kg · ${listing.qualityGrade} quality'),
          const SizedBox(height: 4),
          Text('${currency.format(listing.pricePerKg)}/kg'),
          const SizedBox(height: 4),
          Text(l10n.text('available_on_views', params: {'date': listing.availableDate, 'views': listing.views.toString()}), style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
          if (listing.description != null && listing.description!.isNotEmpty) ...[
            const SizedBox(height: 8),
            Text(listing.description!, style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
          ],
        ],
      ),
    );
  }
}

class _StatusBanner extends StatelessWidget {
  const _StatusBanner({required this.message, required this.color});

  final String message;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.1),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Text(message, style: TextStyle(color: color, fontWeight: FontWeight.w600)),
      ),
    );
  }
}
