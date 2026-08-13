import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_product_card.dart';
import '../widgets/commerce_state_panel.dart';
import 'categories_screen.dart';
import 'commerce_search_screen.dart';
import 'product_detail_screen.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});
  Future<void> _language(BuildContext context, WidgetRef ref) async {
    final l10n = AppStrings.of(context);
    final selected = await showModalBottomSheet<Locale>(
      context: context,
      builder: (_) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            for (final locale in AppStrings.supportedLocales)
              ListTile(
                title: Text(l10n.languageLabel(locale)),
                onTap: () => Navigator.pop(context, locale),
              ),
          ],
        ),
      ),
    );
    if (selected != null) ref.read(appLocaleProvider.notifier).state = selected;
  }

  Future<void> _location(BuildContext context, WidgetRef ref) async {
    final l10n = AppStrings.of(context);
    final input = TextEditingController(
      text: ref.read(deliveryLocationProvider).pincode,
    );
    await showModalBottomSheet<void>(
      context: context,
      isScrollControlled: true,
      builder: (sheet) => Consumer(
        builder: (_, sheetRef, _) {
          final state = sheetRef.watch(deliveryLocationProvider);
          return Padding(
            padding: EdgeInsets.fromLTRB(
              16,
              20,
              16,
              MediaQuery.of(sheet).viewInsets.bottom + 20,
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  l10n.text('set_delivery_area'),
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                const SizedBox(height: 12),
                TextField(
                  controller: input,
                  maxLength: 6,
                  keyboardType: TextInputType.number,
                  decoration: InputDecoration(
                    labelText: l10n.text('pincode'),
                    errorText: state.message == 'invalid_pincode'
                        ? l10n.text('invalid_pincode')
                        : null,
                  ),
                ),
                if (state.status == LoadStatus.loading)
                  const LinearProgressIndicator(),
                if (state.decision != null)
                  Text(
                    state.decision!.reason,
                    style: TextStyle(
                      color: state.decision!.serviceable
                          ? AppTheme.successGreen
                          : AppTheme.warningOrange,
                    ),
                  ),
                if (state.status == LoadStatus.offline)
                  Text(l10n.text('commerce_offline')),
                const SizedBox(height: 12),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: state.status == LoadStatus.loading
                        ? null
                        : () async {
                            final ok = await sheetRef
                                .read(deliveryLocationProvider.notifier)
                                .setPincode(input.text);
                            if (ok && sheet.mounted) Navigator.pop(sheet);
                          },
                    child: Text(l10n.text('check_delivery')),
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
    input.dispose();
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppStrings.of(context);
    final catalog = ref.watch(catalogControllerProvider);
    final location = ref.watch(deliveryLocationProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'CropPulse',
          style: TextStyle(fontWeight: FontWeight.w800),
        ),
        actions: [
          IconButton(
            onPressed: () => _language(context, ref),
            icon: const Icon(Icons.language),
          ),
        ],
      ),
      body: catalog.status != LoadStatus.ready && catalog.products.isEmpty
          ? CommerceStatePanel(
              status: catalog.status,
              message: catalog.message,
              onRetry: () => ref
                  .read(catalogControllerProvider.notifier)
                  .load(Localizations.localeOf(context).languageCode),
            )
          : RefreshIndicator(
              onRefresh: () => ref
                  .read(catalogControllerProvider.notifier)
                  .load(Localizations.localeOf(context).languageCode),
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  ListTile(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                      side: const BorderSide(color: AppTheme.lightGray),
                    ),
                    leading: const Icon(Icons.location_on_outlined),
                    title: Text(
                      location.pincode == null
                          ? l10n.text('set_delivery_area')
                          : '${l10n.text('delivery_to')} ${location.pincode}',
                    ),
                    subtitle: Text(
                      location.decision == null
                          ? l10n.text('check_serviceability')
                          : l10n.text(location.decision!.status),
                    ),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => _location(context, ref),
                  ),
                  const SizedBox(height: 12),
                  ListTile(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                      side: const BorderSide(color: AppTheme.lightGray),
                    ),
                    leading: const Icon(Icons.search),
                    title: Text(l10n.text('search_products')),
                    onTap: () => Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const CommerceSearchScreen(),
                      ),
                    ),
                  ),
                  const SizedBox(height: 20),
                  Row(
                    children: [
                      Expanded(
                        child: Text(
                          l10n.text('categories'),
                          style: const TextStyle(
                            fontSize: 19,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                      ),
                      TextButton(
                        onPressed: () => Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => const CategoriesScreen(),
                          ),
                        ),
                        child: Text(l10n.text('view_all')),
                      ),
                    ],
                  ),
                  GridView.count(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    crossAxisCount: 3,
                    children: [
                      for (final category in catalog.categories.take(6))
                        InkWell(
                          onTap: () => Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => CategoriesScreen(
                                initialCategory: category.slug,
                              ),
                            ),
                          ),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                commerceCategoryIcon(category.slug),
                                color: AppTheme.primaryGreen,
                              ),
                              const SizedBox(height: 6),
                              Text(
                                category.name,
                                textAlign: TextAlign.center,
                                maxLines: 2,
                              ),
                            ],
                          ),
                        ),
                    ],
                  ),
                  const SizedBox(height: 18),
                  Text(
                    l10n.text('available_products'),
                    style: const TextStyle(
                      fontSize: 19,
                      fontWeight: FontWeight.w800,
                    ),
                  ),
                  const SizedBox(height: 10),
                  SizedBox(
                    height: 300,
                    child: ListView.separated(
                      scrollDirection: Axis.horizontal,
                      itemCount: catalog.products.take(8).length,
                      separatorBuilder: (_, _) => const SizedBox(width: 12),
                      itemBuilder: (_, i) {
                        final product = catalog.products[i];
                        return SizedBox(
                          width: 170,
                          child: CommerceProductCard(
                            product: product,
                            onOpen: () => Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) =>
                                    ProductDetailScreen(product: product),
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
