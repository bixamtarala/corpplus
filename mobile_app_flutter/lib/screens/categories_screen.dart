import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../providers/commerce_provider.dart';
import '../widgets/commerce_product_card.dart';
import '../widgets/commerce_state_panel.dart';
import 'product_detail_screen.dart';

class CategoriesScreen extends ConsumerStatefulWidget {
  const CategoriesScreen({super.key, this.initialCategory});
  final String? initialCategory;
  @override
  ConsumerState<CategoriesScreen> createState() => _CategoriesScreenState();
}

class _CategoriesScreenState extends ConsumerState<CategoriesScreen> {
  String? selected;
  @override
  void initState() {
    super.initState();
    selected = widget.initialCategory;
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final catalog = ref.watch(catalogControllerProvider);
    if (catalog.status != LoadStatus.ready && catalog.products.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text(l10n.text('categories'))),
        body: CommerceStatePanel(
          status: catalog.status,
          message: catalog.message,
          onRetry: () => ref
              .read(catalogControllerProvider.notifier)
              .load(Localizations.localeOf(context).languageCode),
        ),
      );
    }
    final products = ref
        .read(catalogControllerProvider.notifier)
        .productsFor(selected);
    return Scaffold(
      appBar: AppBar(title: Text(l10n.text('categories'))),
      body: Column(
        children: [
          SizedBox(
            height: 58,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              children: [
                Padding(
                  padding: const EdgeInsets.only(right: 8),
                  child: ChoiceChip(
                    label: Text(l10n.text('all')),
                    selected: selected == null,
                    onSelected: (_) => setState(() => selected = null),
                  ),
                ),
                for (final category in catalog.categories)
                  Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ChoiceChip(
                      label: Text(category.name),
                      selected: selected == category.slug,
                      onSelected: (_) =>
                          setState(() => selected = category.slug),
                    ),
                  ),
              ],
            ),
          ),
          Expanded(
            child: products.isEmpty
                ? Center(child: Text(l10n.text('no_products')))
                : LayoutBuilder(
                    builder: (context, constraints) {
                      final columns = constraints.maxWidth >= 700 ? 4 : 2;
                      return RefreshIndicator(
                        onRefresh: () => ref
                            .read(catalogControllerProvider.notifier)
                            .load(Localizations.localeOf(context).languageCode),
                        child: GridView.builder(
                          padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
                          gridDelegate:
                              SliverGridDelegateWithFixedCrossAxisCount(
                                crossAxisCount: columns,
                                mainAxisSpacing: 12,
                                crossAxisSpacing: 12,
                                childAspectRatio: constraints.maxWidth < 370
                                    ? .57
                                    : .64,
                              ),
                          itemCount: products.length,
                          itemBuilder: (_, index) {
                            final product = products[index];
                            return CommerceProductCard(
                              product: product,
                              onOpen: () => Navigator.of(context).push(
                                MaterialPageRoute(
                                  builder: (_) =>
                                      ProductDetailScreen(product: product),
                                ),
                              ),
                            );
                          },
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
