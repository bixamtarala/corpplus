import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_product_card.dart';
import 'categories_screen.dart';
import 'product_detail_screen.dart';

class CartScreen extends ConsumerWidget {
  const CartScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cart = ref.watch(cartControllerProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('Preview cart')),
      body: cart.lines.isEmpty
          ? _EmptyCart(
              onBrowse: () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const CategoriesScreen()),
              ),
            )
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: AppTheme.warningOrange.withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: const Row(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Icon(Icons.info_outline, color: AppTheme.warningOrange),
                      SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          'This cart validates the shopping experience only. Prices are indicative and checkout is disabled until live catalog, inventory, serviceability, and payment are configured.',
                          style: TextStyle(height: 1.35),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 14),
                for (final line in cart.lines)
                  _CartLineTile(
                    line: line,
                    onOpen: () => Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) =>
                            ProductDetailScreen(product: line.product),
                      ),
                    ),
                  ),
                const SizedBox(height: 10),
                _PreviewSummary(cart: cart),
              ],
            ),
      bottomNavigationBar: cart.lines.isEmpty
          ? null
          : SafeArea(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
                child: ElevatedButton.icon(
                  onPressed: null,
                  icon: const Icon(Icons.lock_outline),
                  label: const Text('Checkout not live yet'),
                ),
              ),
            ),
    );
  }
}

class _EmptyCart extends StatelessWidget {
  const _EmptyCart({required this.onBrowse});

  final VoidCallback onBrowse;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(
              Icons.shopping_cart_outlined,
              size: 56,
              color: AppTheme.lightText,
            ),
            const SizedBox(height: 14),
            const Text(
              'Your preview cart is empty',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.w700),
            ),
            const SizedBox(height: 6),
            const Text(
              'Browse the pilot catalog and add products to test the planned shopping flow.',
              textAlign: TextAlign.center,
              style: TextStyle(color: AppTheme.lightText, height: 1.4),
            ),
            const SizedBox(height: 18),
            ElevatedButton(
              onPressed: onBrowse,
              child: const Text('Browse categories'),
            ),
          ],
        ),
      ),
    );
  }
}

class _CartLineTile extends ConsumerWidget {
  const _CartLineTile({required this.line, required this.onOpen});

  final CartLine line;
  final VoidCallback onOpen;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final languageCode = Localizations.localeOf(context).languageCode;
    final controller = ref.read(cartControllerProvider.notifier);

    return Card(
      elevation: 0,
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: const BorderSide(color: AppTheme.lightGray),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            InkWell(
              onTap: onOpen,
              borderRadius: BorderRadius.circular(10),
              child: Container(
                width: 64,
                height: 64,
                decoration: BoxDecoration(
                  color: AppTheme.primaryGreen.withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(
                  commerceCategoryIcon(line.product.category),
                  color: AppTheme.primaryGreen,
                ),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    line.product.displayName(languageCode),
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                  Text(
                    '${line.product.packLabel} • preview',
                    style: const TextStyle(
                      fontSize: 12,
                      color: AppTheme.lightText,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    _formatPaise(line.previewTotalPaise),
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                ],
              ),
            ),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                IconButton(
                  tooltip: 'Remove one',
                  onPressed: () => controller.removeOne(line.product.id),
                  icon: const Icon(Icons.remove_circle_outline),
                ),
                Text(
                  '${line.quantity}',
                  style: const TextStyle(fontWeight: FontWeight.w700),
                ),
                IconButton(
                  tooltip: 'Add one',
                  onPressed: () => controller.add(line.product.id),
                  icon: const Icon(Icons.add_circle_outline),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _PreviewSummary extends StatelessWidget {
  const _PreviewSummary({required this.cart});

  final CartState cart;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: AppTheme.lightGray),
      ),
      child: Row(
        children: [
          const Expanded(
            child: Text(
              'Indicative subtotal',
              style: TextStyle(fontWeight: FontWeight.w700),
            ),
          ),
          Text(
            _formatPaise(cart.previewSubtotalPaise),
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
          ),
        ],
      ),
    );
  }
}

String _formatPaise(int paise) {
  final rupees = paise ~/ 100;
  final remainder = paise % 100;
  return remainder == 0
      ? 'Rs $rupees'
      : 'Rs $rupees.${remainder.toString().padLeft(2, '0')}';
}
