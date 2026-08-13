import 'package:flutter/material.dart';

import '../data/commerce_catalog.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_product_card.dart';
import 'product_detail_screen.dart';

class CategoriesScreen extends StatefulWidget {
  const CategoriesScreen({super.key, this.initialCategory});

  final String? initialCategory;

  @override
  State<CategoriesScreen> createState() => _CategoriesScreenState();
}

class _CategoriesScreenState extends State<CategoriesScreen> {
  String? _selectedCategory;

  @override
  void initState() {
    super.initState();
    _selectedCategory = widget.initialCategory;
  }

  @override
  Widget build(BuildContext context) {
    final products = CommerceCatalog.productsForCategory(_selectedCategory);

    return Scaffold(
      appBar: AppBar(title: const Text('Categories')),
      body: Column(
        children: [
          SizedBox(
            height: 58,
            child: ListView(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              scrollDirection: Axis.horizontal,
              children: [
                _CategoryChip(
                  label: 'All',
                  selected: _selectedCategory == null,
                  onSelected: () => setState(() => _selectedCategory = null),
                ),
                for (final category in CommerceCatalog.categories)
                  _CategoryChip(
                    label: category.label,
                    selected: _selectedCategory == category.id,
                    onSelected: () =>
                        setState(() => _selectedCategory = category.id),
                  ),
              ],
            ),
          ),
          Container(
            width: double.infinity,
            margin: const EdgeInsets.fromLTRB(16, 4, 16, 8),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppTheme.primaryBlue.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Text(
              'Preview catalog: prices and availability are indicative. Checkout is not live.',
              style: TextStyle(fontSize: 12, height: 1.35),
            ),
          ),
          Expanded(
            child: LayoutBuilder(
              builder: (context, constraints) {
                final columns = constraints.maxWidth >= 700 ? 4 : 2;
                return GridView.builder(
                  padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: columns,
                    mainAxisSpacing: 12,
                    crossAxisSpacing: 12,
                    childAspectRatio: constraints.maxWidth < 370 ? 0.57 : 0.64,
                  ),
                  itemCount: products.length,
                  itemBuilder: (context, index) {
                    final product = products[index];
                    return CommerceProductCard(
                      product: product,
                      onOpen: () => Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => ProductDetailScreen(product: product),
                        ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}

class _CategoryChip extends StatelessWidget {
  const _CategoryChip({
    required this.label,
    required this.selected,
    required this.onSelected,
  });

  final String label;
  final bool selected;
  final VoidCallback onSelected;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: ChoiceChip(
        label: Text(label),
        selected: selected,
        onSelected: (_) => onSelected(),
      ),
    );
  }
}
