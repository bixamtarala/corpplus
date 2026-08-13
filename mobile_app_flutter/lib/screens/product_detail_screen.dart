import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/commerce_catalog.dart';
import '../models/commerce_product.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_product_card.dart';

class ProductDetailScreen extends ConsumerWidget {
  const ProductDetailScreen({super.key, required this.product});

  final CommerceProduct product;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final quantity = ref.watch(
      cartControllerProvider.select((state) => state.quantityFor(product.id)),
    );
    final languageCode = Localizations.localeOf(context).languageCode;
    final category = CommerceCatalog.categoryById(product.category);

    return Scaffold(
      appBar: AppBar(title: Text(product.displayName(languageCode))),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            height: 220,
            decoration: BoxDecoration(
              color: AppTheme.primaryGreen.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Icon(
              commerceCategoryIcon(product.category),
              color: AppTheme.primaryGreen,
              size: 88,
            ),
          ),
          const SizedBox(height: 18),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _InfoChip(label: category.label, icon: Icons.category_outlined),
              _InfoChip(label: product.grade, icon: Icons.verified_outlined),
              if (product.isFresh)
                const _InfoChip(
                  label: 'Fresh-product preview',
                  icon: Icons.eco_outlined,
                ),
            ],
          ),
          const SizedBox(height: 16),
          Text(
            product.displayName(languageCode),
            style: Theme.of(
              context,
            ).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 6),
          Text(
            product.packLabel,
            style: const TextStyle(color: AppTheme.lightText),
          ),
          const SizedBox(height: 10),
          Text(
            '${product.formattedPreviewPrice} indicative pilot price',
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 16),
          _Notice(
            icon: Icons.info_outline,
            text:
                'Preview catalog only. Live ordering, delivery, final price, stock, source, and quality are not active yet.',
          ),
          const SizedBox(height: 20),
          _DetailRow(title: 'Source and origin', value: product.origin),
          _DetailRow(title: 'Pack information', value: product.packLabel),
          _DetailRow(title: 'Product information', value: product.description),
          const _DetailRow(
            title: 'Replacement policy',
            value: 'To be approved before pilot checkout is enabled.',
          ),
          const SizedBox(height: 96),
        ],
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(16, 8, 16, 12),
          child: quantity == 0
              ? ElevatedButton.icon(
                  onPressed: () =>
                      ref.read(cartControllerProvider.notifier).add(product.id),
                  icon: const Icon(Icons.add_shopping_cart),
                  label: const Text('Add to preview cart'),
                )
              : Row(
                  children: [
                    IconButton.outlined(
                      tooltip: 'Remove one',
                      onPressed: () => ref
                          .read(cartControllerProvider.notifier)
                          .removeOne(product.id),
                      icon: const Icon(Icons.remove),
                    ),
                    Expanded(
                      child: Center(
                        child: Text(
                          '$quantity in preview cart',
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        ),
                      ),
                    ),
                    IconButton.filled(
                      tooltip: 'Add one',
                      onPressed: () => ref
                          .read(cartControllerProvider.notifier)
                          .add(product.id),
                      icon: const Icon(Icons.add),
                    ),
                  ],
                ),
        ),
      ),
    );
  }
}

class _InfoChip extends StatelessWidget {
  const _InfoChip({required this.label, required this.icon});

  final String label;
  final IconData icon;

  @override
  Widget build(BuildContext context) {
    return Chip(
      avatar: Icon(icon, size: 17, color: AppTheme.primaryGreen),
      label: Text(label),
      side: const BorderSide(color: AppTheme.lightGray),
      backgroundColor: Colors.white,
    );
  }
}

class _Notice extends StatelessWidget {
  const _Notice({required this.icon, required this.text});

  final IconData icon;
  final String text;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: AppTheme.warningOrange.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: AppTheme.warningOrange),
          const SizedBox(width: 10),
          Expanded(child: Text(text, style: const TextStyle(height: 1.35))),
        ],
      ),
    );
  }
}

class _DetailRow extends StatelessWidget {
  const _DetailRow({required this.title, required this.value});

  final String title;
  final String value;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 18),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontWeight: FontWeight.w700)),
          const SizedBox(height: 5),
          Text(
            value,
            style: const TextStyle(color: AppTheme.lightText, height: 1.4),
          ),
        ],
      ),
    );
  }
}
