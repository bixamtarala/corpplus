import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/commerce_product.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';

IconData commerceCategoryIcon(String categoryId) {
  return switch (categoryId) {
    'vegetables' => Icons.eco_outlined,
    'fruits' => Icons.apple_outlined,
    'greens' => Icons.grass_outlined,
    'grains' => Icons.grain_outlined,
    'pulses' => Icons.breakfast_dining_outlined,
    'spices' => Icons.local_fire_department_outlined,
    _ => Icons.shopping_basket_outlined,
  };
}

class CommerceProductCard extends ConsumerWidget {
  const CommerceProductCard({
    super.key,
    required this.product,
    required this.onOpen,
  });

  final CommerceProduct product;
  final VoidCallback onOpen;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final quantity = ref.watch(
      cartControllerProvider.select((state) => state.quantityFor(product.id)),
    );
    final languageCode = Localizations.localeOf(context).languageCode;

    return Card(
      clipBehavior: Clip.antiAlias,
      margin: EdgeInsets.zero,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: AppTheme.lightGray),
      ),
      child: InkWell(
        onTap: onOpen,
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                height: 92,
                width: double.infinity,
                decoration: BoxDecoration(
                  color: AppTheme.primaryGreen.withValues(alpha: 0.08),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(
                  commerceCategoryIcon(product.category),
                  size: 44,
                  color: AppTheme.primaryGreen,
                ),
              ),
              const SizedBox(height: 10),
              Text(
                product.displayName(languageCode),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 3),
              Text(
                product.packLabel,
                style: const TextStyle(fontSize: 12, color: AppTheme.lightText),
              ),
              const Spacer(),
              Text(
                '${product.formattedPreviewPrice} preview',
                style: const TextStyle(fontWeight: FontWeight.w700),
              ),
              const SizedBox(height: 8),
              if (quantity == 0)
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton(
                    onPressed: () => ref
                        .read(cartControllerProvider.notifier)
                        .add(product.id),
                    child: const Text('Add'),
                  ),
                )
              else
                _QuantityControl(productId: product.id, quantity: quantity),
            ],
          ),
        ),
      ),
    );
  }
}

class _QuantityControl extends ConsumerWidget {
  const _QuantityControl({required this.productId, required this.quantity});

  final String productId;
  final int quantity;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final controller = ref.read(cartControllerProvider.notifier);
    return Container(
      height: 40,
      decoration: BoxDecoration(
        border: Border.all(color: AppTheme.primaryGreen),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Row(
        children: [
          Expanded(
            child: IconButton(
              tooltip: 'Remove one',
              padding: EdgeInsets.zero,
              onPressed: () => controller.removeOne(productId),
              icon: const Icon(Icons.remove, size: 18),
            ),
          ),
          Text(
            '$quantity',
            style: const TextStyle(fontWeight: FontWeight.w700),
          ),
          Expanded(
            child: IconButton(
              tooltip: 'Add one',
              padding: EdgeInsets.zero,
              onPressed: () => controller.add(productId),
              icon: const Icon(Icons.add, size: 18),
            ),
          ),
        ],
      ),
    );
  }
}
