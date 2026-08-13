import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../models/commerce_api_models.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_product_card.dart';
import '../widgets/commerce_state_panel.dart';
import 'categories_screen.dart';

class CartScreen extends ConsumerWidget {
  const CartScreen({super.key});
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppStrings.of(context);
    final state = ref.watch(cartControllerProvider);
    final cart = state.cart;
    if (cart == null) {
      return Scaffold(
        appBar: AppBar(title: Text(l10n.text('cart'))),
        body: CommerceStatePanel(
          status: state.status,
          message: state.message,
          onRetry: () => ref.read(cartControllerProvider.notifier).initialize(),
        ),
      );
    }
    return Scaffold(
      appBar: AppBar(title: Text(l10n.text('cart'))),
      body: RefreshIndicator(
        onRefresh: () => ref.read(cartControllerProvider.notifier).initialize(),
        child: cart.items.isEmpty
            ? ListView(
                children: [
                  SizedBox(height: MediaQuery.of(context).size.height * .25),
                  Icon(
                    Icons.shopping_cart_outlined,
                    size: 56,
                    color: AppTheme.lightText,
                  ),
                  const SizedBox(height: 12),
                  Center(child: Text(l10n.text('empty_cart'))),
                  Center(
                    child: TextButton(
                      onPressed: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => const CategoriesScreen(),
                        ),
                      ),
                      child: Text(l10n.text('browse_categories')),
                    ),
                  ),
                ],
              )
            : ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  if (state.status == LoadStatus.loading)
                    const LinearProgressIndicator(),
                  if (state.status == LoadStatus.offline ||
                      state.status == LoadStatus.error)
                    _Message(
                      text: state.status == LoadStatus.offline
                          ? l10n.text('commerce_offline')
                          : state.message ?? l10n.text('commerce_error'),
                    ),
                  if (cart.deliveryPincode == null)
                    _Message(text: l10n.text('cart_location_required')),
                  for (final issue in cart.issues)
                    _Message(text: issue.message),
                  for (final item in cart.items) _CartItemTile(item: item),
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        children: [
                          _row(
                            l10n.text('subtotal'),
                            formatPaise(cart.subtotalPaise),
                          ),
                          if (cart.deliveryFeePaise != null)
                            _row(
                              l10n.text('delivery_fee'),
                              formatPaise(cart.deliveryFeePaise!),
                            ),
                          if (cart.totalPaise != null)
                            _row(
                              l10n.text('total'),
                              formatPaise(cart.totalPaise!),
                              bold: true,
                            ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
      ),
      bottomNavigationBar: cart.items.isEmpty
          ? null
          : SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: ElevatedButton.icon(
                  onPressed: null,
                  icon: const Icon(Icons.lock_outline),
                  label: Text(
                    cart.validForCheckout
                        ? l10n.text('checkout_next_step')
                        : l10n.text('resolve_cart_issues'),
                  ),
                ),
              ),
            ),
    );
  }
}

class _CartItemTile extends ConsumerWidget {
  const _CartItemTile({required this.item});
  final CommerceCartItem item;
  @override
  Widget build(BuildContext context, WidgetRef ref) => Card(
    child: Padding(
      padding: const EdgeInsets.all(12),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  item.productName,
                  style: const TextStyle(fontWeight: FontWeight.w800),
                ),
                Text(
                  item.skuCode,
                  style: const TextStyle(color: AppTheme.lightText),
                ),
                Text(
                  item.lineTotalPaise == null
                      ? '--'
                      : formatPaise(item.lineTotalPaise!),
                ),
                for (final issue in item.issues)
                  Text(
                    issue.message,
                    style: TextStyle(
                      fontSize: 12,
                      color: issue.severity == 'error'
                          ? Colors.red
                          : AppTheme.warningOrange,
                    ),
                  ),
              ],
            ),
          ),
          IconButton(
            onPressed: () => ref
                .read(cartControllerProvider.notifier)
                .updateItem(item, item.quantity - item.quantityStep),
            icon: const Icon(Icons.remove_circle_outline),
          ),
          Text(compactQuantity(item.quantity)),
          IconButton(
            onPressed: () => ref
                .read(cartControllerProvider.notifier)
                .updateItem(item, item.quantity + item.quantityStep),
            icon: const Icon(Icons.add_circle_outline),
          ),
          IconButton(
            onPressed: () =>
                ref.read(cartControllerProvider.notifier).removeItem(item),
            icon: const Icon(Icons.delete_outline),
          ),
        ],
      ),
    ),
  );
}

class _Message extends StatelessWidget {
  const _Message({required this.text});
  final String text;
  @override
  Widget build(BuildContext context) => Container(
    margin: const EdgeInsets.only(bottom: 10),
    padding: const EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: AppTheme.warningOrange.withValues(alpha: .1),
      borderRadius: BorderRadius.circular(12),
    ),
    child: Text(text),
  );
}

Widget _row(String label, String value, {bool bold = false}) => Padding(
  padding: const EdgeInsets.symmetric(vertical: 4),
  child: Row(
    children: [
      Expanded(child: Text(label)),
      Text(
        value,
        style: TextStyle(fontWeight: bold ? FontWeight.w800 : FontWeight.w500),
      ),
    ],
  ),
);
