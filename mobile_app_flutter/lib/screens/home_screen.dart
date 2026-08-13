import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/commerce_catalog.dart';
import '../localization/app_strings.dart';
import '../models/commerce_product.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_product_card.dart';
import 'categories_screen.dart';
import 'commerce_search_screen.dart';
import 'product_detail_screen.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  Future<void> _showLanguageSelector(
    BuildContext context,
    WidgetRef ref,
    AppStrings l10n,
    Locale currentLocale,
  ) async {
    final selectedLocale = await showModalBottomSheet<Locale>(
      context: context,
      showDragHandle: true,
      builder: (sheetContext) {
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  l10n.text('select_language'),
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 12),
                for (final item in AppStrings.supportedLocales)
                  ListTile(
                    contentPadding: EdgeInsets.zero,
                    leading: Icon(
                      item.languageCode == currentLocale.languageCode
                          ? Icons.radio_button_checked
                          : Icons.radio_button_off,
                      color: item.languageCode == currentLocale.languageCode
                          ? AppTheme.primaryGreen
                          : AppTheme.lightText,
                    ),
                    title: Text(l10n.languageLabel(item)),
                    onTap: () => Navigator.of(sheetContext).pop(item),
                  ),
              ],
            ),
          ),
        );
      },
    );

    if (selectedLocale != null) {
      ref.read(appLocaleProvider.notifier).state = selectedLocale;
    }
  }

  Future<void> _showLocationSheet(BuildContext context, WidgetRef ref) async {
    final controller = TextEditingController(
      text: ref.read(deliveryLocationProvider).pincode ?? '',
    );

    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      showDragHandle: true,
      builder: (sheetContext) {
        return Consumer(
          builder: (context, sheetRef, _) {
            final state = sheetRef.watch(deliveryLocationProvider);
            return Padding(
              padding: EdgeInsets.fromLTRB(
                16,
                4,
                16,
                20 + MediaQuery.of(context).viewInsets.bottom,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Set delivery area',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.w700),
                  ),
                  const SizedBox(height: 6),
                  const Text(
                    'Enter a pincode to prepare the serviceability flow. No pincode is live for checkout yet.',
                    style: TextStyle(color: AppTheme.lightText, height: 1.4),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: controller,
                    keyboardType: TextInputType.number,
                    maxLength: 6,
                    decoration: InputDecoration(
                      labelText: 'Pincode',
                      errorText:
                          state.validationMessage != null && !state.hasPincode
                          ? state.validationMessage
                          : null,
                    ),
                  ),
                  if (state.hasPincode && state.validationMessage != null)
                    Padding(
                      padding: const EdgeInsets.only(bottom: 12),
                      child: Text(
                        state.validationMessage!,
                        style: const TextStyle(
                          color: AppTheme.warningOrange,
                          height: 1.35,
                        ),
                      ),
                    ),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {
                        final accepted = sheetRef
                            .read(deliveryLocationProvider.notifier)
                            .setPincode(controller.text);
                        if (accepted) {
                          Navigator.of(sheetContext).pop();
                        }
                      },
                      child: const Text('Save for preview'),
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
    controller.dispose();
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppStrings.of(context);
    final locale = ref.watch(appLocaleProvider);
    final location = ref.watch(deliveryLocationProvider);
    final featuredProducts = CommerceCatalog.products.take(6).toList();

    return Scaffold(
      appBar: AppBar(
        titleSpacing: 12,
        title: const Text(
          'CropPulse',
          style: TextStyle(fontWeight: FontWeight.w800),
        ),
        actions: [
          IconButton(
            tooltip: l10n.text('select_language'),
            onPressed: () => _showLanguageSelector(context, ref, l10n, locale),
            icon: const Icon(Icons.language, color: AppTheme.primaryBlue),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.fromLTRB(16, 10, 16, 28),
        children: [
          InkWell(
            onTap: () => _showLocationSheet(context, ref),
            borderRadius: BorderRadius.circular(12),
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.lightGray),
              ),
              child: Row(
                children: [
                  const Icon(
                    Icons.location_on_outlined,
                    color: AppTheme.primaryGreen,
                  ),
                  const SizedBox(width: 10),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          location.hasPincode
                              ? 'Preview area: ${location.pincode}'
                              : 'Set delivery area',
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        ),
                        const Text(
                          'Pilot delivery is not live',
                          style: TextStyle(
                            fontSize: 12,
                            color: AppTheme.warningOrange,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Icon(Icons.chevron_right),
                ],
              ),
            ),
          ),
          const SizedBox(height: 12),
          Semantics(
            button: true,
            label: 'Search preview products',
            child: InkWell(
              borderRadius: BorderRadius.circular(14),
              onTap: () => Navigator.of(context).push(
                MaterialPageRoute(builder: (_) => const CommerceSearchScreen()),
              ),
              child: Container(
                height: 52,
                padding: const EdgeInsets.symmetric(horizontal: 14),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: AppTheme.lightGray),
                ),
                child: const Row(
                  children: [
                    Icon(Icons.search, color: AppTheme.lightText),
                    SizedBox(width: 10),
                    Expanded(
                      child: Text(
                        'Search vegetables, fruits, grains...',
                        style: TextStyle(color: AppTheme.lightText),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              gradient: AppTheme.primaryGradient,
              borderRadius: BorderRadius.circular(18),
            ),
            child: const Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Farm commerce, built for trust',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 21,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                SizedBox(height: 6),
                Text(
                  'Explore the proposed Phase 1 catalog. Live stock, suppliers, delivery, and checkout will activate only after pilot approval.',
                  style: TextStyle(color: Colors.white, height: 1.4),
                ),
              ],
            ),
          ),
          const SizedBox(height: 12),
          Text(
            l10n.text('daily_feed_title'),
            style: const TextStyle(fontSize: 13, color: AppTheme.lightText),
          ),
          const SizedBox(height: 22),
          _SectionHeader(
            title: 'Categories',
            actionLabel: 'View all',
            onAction: () => Navigator.of(
              context,
            ).push(MaterialPageRoute(builder: (_) => const CategoriesScreen())),
          ),
          const SizedBox(height: 10),
          GridView.count(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisCount: 3,
            mainAxisSpacing: 10,
            crossAxisSpacing: 10,
            childAspectRatio: 1.02,
            children: [
              for (final category in CommerceCatalog.categories)
                _CategoryTile(
                  category: category,
                  onTap: () => Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (_) =>
                          CategoriesScreen(initialCategory: category.id),
                    ),
                  ),
                ),
            ],
          ),
          const SizedBox(height: 24),
          const _SectionHeader(title: 'Pilot catalog preview'),
          const SizedBox(height: 10),
          SizedBox(
            height: 300,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: featuredProducts.length,
              separatorBuilder: (_, _) => const SizedBox(width: 12),
              itemBuilder: (context, index) {
                final product = featuredProducts[index];
                return SizedBox(
                  width: 170,
                  child: CommerceProductCard(
                    product: product,
                    onOpen: () => Navigator.of(context).push(
                      MaterialPageRoute(
                        builder: (_) => ProductDetailScreen(product: product),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _SectionHeader extends StatelessWidget {
  const _SectionHeader({required this.title, this.actionLabel, this.onAction});

  final String title;
  final String? actionLabel;
  final VoidCallback? onAction;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Text(
            title,
            style: const TextStyle(fontSize: 19, fontWeight: FontWeight.w800),
          ),
        ),
        if (actionLabel != null)
          TextButton(onPressed: onAction, child: Text(actionLabel!)),
      ],
    );
  }
}

class _CategoryTile extends StatelessWidget {
  const _CategoryTile({required this.category, required this.onTap});

  final CommerceCategory category;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: const BorderSide(color: AppTheme.lightGray),
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(14),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(8),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                commerceCategoryIcon(category.id),
                color: AppTheme.primaryGreen,
                size: 30,
              ),
              const SizedBox(height: 7),
              Text(
                category.label,
                maxLines: 2,
                textAlign: TextAlign.center,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
