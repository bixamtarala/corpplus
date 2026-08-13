import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../models/commerce_api_models.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';

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
    final l10n = AppStrings.of(context);
    final sku = product.skus.firstOrNull;
    final cart = ref.watch(cartControllerProvider);
    final quantity = sku == null ? 0.0 : cart.quantityForSku(sku.id);
    return Card(
      clipBehavior: Clip.antiAlias,
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: const BorderSide(color: AppTheme.lightGray),
      ),
      child: InkWell(
        onTap: onOpen,
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Center(
                  child: Icon(
                    commerceCategoryIcon(product.category.slug),
                    size: 58,
                    color: AppTheme.primaryGreen,
                  ),
                ),
              ),
              Text(
                product.name,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 4),
              Text(
                sku?.packLabel ?? l10n.text('not_available'),
                style: const TextStyle(fontSize: 12, color: AppTheme.lightText),
              ),
              const SizedBox(height: 6),
              Text(
                sku?.pricePaise == null
                    ? l10n.text('price_unavailable')
                    : formatPaise(sku!.pricePaise!),
                style: const TextStyle(fontWeight: FontWeight.w800),
              ),
              const SizedBox(height: 8),
              SizedBox(
                width: double.infinity,
                child: quantity > 0
                    ? OutlinedButton(
                        onPressed: null,
                        child: Text(
                          l10n.text(
                            'in_cart',
                            params: {'quantity': compactQuantity(quantity)},
                          ),
                        ),
                      )
                    : ElevatedButton(
                        onPressed:
                            sku?.pricePaise == null ||
                                cart.status == LoadStatus.loading
                            ? null
                            : () => ref
                                  .read(cartControllerProvider.notifier)
                                  .addSku(sku!),
                        child: Text(l10n.text('add_to_cart')),
                      ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

IconData commerceCategoryIcon(String category) => switch (category) {
  'vegetables' => Icons.eco_outlined,
  'fruits' => Icons.apple_outlined,
  'greens' => Icons.grass_outlined,
  'grains' => Icons.rice_bowl_outlined,
  'pulses' => Icons.scatter_plot_outlined,
  'spices' => Icons.local_fire_department_outlined,
  _ => Icons.inventory_2_outlined,
};
String formatPaise(int paise) =>
    '₹${(paise / 100).toStringAsFixed(paise % 100 == 0 ? 0 : 2)}';
String compactQuantity(double value) => value == value.roundToDouble()
    ? value.toInt().toString()
    : value.toString();
