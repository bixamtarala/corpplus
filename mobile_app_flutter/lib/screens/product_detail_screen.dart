import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../models/commerce_api_models.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_product_card.dart';

class ProductDetailScreen extends ConsumerWidget {
  const ProductDetailScreen({super.key, required this.product});
  final CommerceProduct product;
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppStrings.of(context);
    final sku = product.skus.firstOrNull;
    final busy = ref.watch(cartControllerProvider).status == LoadStatus.loading;
    return Scaffold(
      appBar: AppBar(title: Text(product.name)),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            height: 210,
            decoration: BoxDecoration(
              color: AppTheme.primaryGreen.withValues(alpha: .08),
              borderRadius: BorderRadius.circular(20),
            ),
            child: Icon(
              commerceCategoryIcon(product.category.slug),
              size: 88,
              color: AppTheme.primaryGreen,
            ),
          ),
          const SizedBox(height: 18),
          Text(
            product.name,
            style: const TextStyle(fontSize: 25, fontWeight: FontWeight.w800),
          ),
          Text(
            product.category.name,
            style: const TextStyle(color: AppTheme.lightText),
          ),
          const SizedBox(height: 12),
          if (sku != null) ...[
            Text(
              sku.packLabel,
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
            Text(
              sku.pricePaise == null
                  ? l10n.text('price_unavailable')
                  : formatPaise(sku.pricePaise!),
              style: const TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
            ),
            Text(
              '${l10n.text('minimum_quantity')}: ${compactQuantity(sku.minimumOrderQuantity)} ${sku.unitOfMeasure}',
            ),
            if (sku.grade != null) Text('${l10n.text('grade')}: ${sku.grade}'),
          ],
          const SizedBox(height: 16),
          Text(
            product.description ?? l10n.text('description_unavailable'),
            style: const TextStyle(height: 1.45),
          ),
        ],
      ),
      bottomNavigationBar: sku == null
          ? null
          : SafeArea(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: ElevatedButton(
                  onPressed: sku.pricePaise == null || busy
                      ? null
                      : () => ref
                            .read(cartControllerProvider.notifier)
                            .addSku(sku),
                  child: Text(l10n.text('add_to_cart')),
                ),
              ),
            ),
    );
  }
}
