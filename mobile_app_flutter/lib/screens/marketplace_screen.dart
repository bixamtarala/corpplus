import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../data/commodity_catalog.dart';
import '../models/marketplace.dart';
import '../providers/marketplace_provider.dart';
import '../theme/app_theme.dart';

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
    final marketplaceState = ref.watch(marketplaceControllerProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('🛒 Marketplace'),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Buy Orders'),
            Tab(text: 'Sell Orders'),
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
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
          child: Row(
            children: [
              Expanded(
                child: DropdownButtonFormField<String>(
                  initialValue: _selectedCrop,
                  items: CommodityCatalog.all
                      .map((crop) => DropdownMenuItem<String>(value: crop, child: Text(crop)))
                      .toList(),
                  onChanged: (value) {
                    if (value == null) {
                      return;
                    }
                    setState(() {
                      _selectedCrop = value;
                    });
                  },
                  decoration: const InputDecoration(labelText: 'Crop'),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: TextField(
                  controller: _stateFilterController,
                  decoration: const InputDecoration(labelText: 'State filter'),
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
              label: const Text('Sync Listings'),
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
            child: const Text(
              'No live sell listings yet. Use the add button to publish one to the marketplace backend.',
              style: TextStyle(height: 1.4),
            ),
          ),
        ...marketplaceState.sellOrders.map((listing) => _SellOrderCard(listing: listing)),
      ],
    );
  }

  Future<void> _showCreateListingSheet(BuildContext context) async {
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
                const Text('Create Listing', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                TextField(controller: cropController, decoration: const InputDecoration(labelText: 'Crop ID')),
                const SizedBox(height: 12),
                TextField(controller: quantityController, decoration: const InputDecoration(labelText: 'Quantity (kg)'), keyboardType: const TextInputType.numberWithOptions(decimal: true)),
                const SizedBox(height: 12),
                TextField(controller: qualityController, decoration: const InputDecoration(labelText: 'Quality Grade')),
                const SizedBox(height: 12),
                TextField(controller: priceController, decoration: const InputDecoration(labelText: 'Price per kg'), keyboardType: const TextInputType.numberWithOptions(decimal: true)),
                const SizedBox(height: 12),
                TextField(controller: dateController, decoration: const InputDecoration(labelText: 'Available Date (YYYY-MM-DD)')),
                const SizedBox(height: 12),
                TextField(controller: descriptionController, decoration: const InputDecoration(labelText: 'Description')),
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () {
                      final quantity = double.tryParse(quantityController.text.trim());
                      final price = double.tryParse(priceController.text.trim());
                      if (quantity == null || price == null) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Enter valid numeric values for quantity and price.')),
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
                    child: const Text('Publish Listing'),
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
    final priceController = TextEditingController(text: order.pricePerKg.toStringAsFixed(0));
    final quantityController = TextEditingController(text: order.quantityKg.toStringAsFixed(0));
    final pickupController = TextEditingController(text: '${order.district}, ${order.state}');
    final messageController = TextEditingController(text: 'Ready to purchase quickly.');

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
                Text('Make Offer for ${order.crop}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 12),
                TextField(controller: priceController, decoration: const InputDecoration(labelText: 'Offer price per kg'), keyboardType: const TextInputType.numberWithOptions(decimal: true)),
                const SizedBox(height: 12),
                TextField(controller: quantityController, decoration: const InputDecoration(labelText: 'Quantity (kg)'), keyboardType: const TextInputType.numberWithOptions(decimal: true)),
                const SizedBox(height: 12),
                TextField(controller: pickupController, decoration: const InputDecoration(labelText: 'Pickup location')),
                const SizedBox(height: 12),
                TextField(controller: messageController, decoration: const InputDecoration(labelText: 'Message')),
                const SizedBox(height: 16),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () {
                      final price = double.tryParse(priceController.text.trim());
                      final quantity = double.tryParse(quantityController.text.trim());
                      if (price == null || quantity == null) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Enter valid numeric values for offer and quantity.')),
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
                    child: const Text('Submit Offer'),
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
          Text(order.farmerName, style: const TextStyle(fontWeight: FontWeight.w600)),
          const SizedBox(height: 4),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('${currency.format(order.pricePerKg)}/kg', style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600)),
              Text('${order.district}, ${order.state}', style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
            ],
          ),
          const SizedBox(height: 4),
          Text('Available: ${order.availableDate}', style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
          const SizedBox(height: 12),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: AppTheme.primaryGreen, minimumSize: const Size(double.infinity, 36)),
            onPressed: onMakeOffer,
            child: const Text('Make Offer', style: TextStyle(color: Colors.white)),
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
          Text('Available on ${listing.availableDate} · ${listing.views} views', style: const TextStyle(fontSize: 12, color: AppTheme.lightText)),
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
