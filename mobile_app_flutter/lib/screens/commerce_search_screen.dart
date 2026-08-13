import 'package:flutter/material.dart';

import '../data/commerce_catalog.dart';
import '../models/commerce_product.dart';
import '../theme/app_theme.dart';
import '../widgets/commerce_product_card.dart';
import 'product_detail_screen.dart';

class CommerceSearchScreen extends StatefulWidget {
  const CommerceSearchScreen({super.key});

  @override
  State<CommerceSearchScreen> createState() => _CommerceSearchScreenState();
}

class _CommerceSearchScreenState extends State<CommerceSearchScreen> {
  final TextEditingController _controller = TextEditingController();
  List<CommerceProduct> _results = CommerceCatalog.products;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _search(String value) {
    setState(() {
      _results = CommerceCatalog.search(value);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Search')),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
            child: TextField(
              controller: _controller,
              autofocus: false,
              textInputAction: TextInputAction.search,
              onChanged: _search,
              decoration: InputDecoration(
                hintText: 'Search vegetables, fruits, grains...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _controller.text.isEmpty
                    ? null
                    : IconButton(
                        tooltip: 'Clear search',
                        onPressed: () {
                          _controller.clear();
                          _search('');
                        },
                        icon: const Icon(Icons.close),
                      ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            child: Row(
              children: [
                Expanded(
                  child: Text(
                    _controller.text.isEmpty
                        ? 'Browse the preview catalog'
                        : '${_results.length} preview result${_results.length == 1 ? '' : 's'}',
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                ),
                const Text(
                  'Not live',
                  style: TextStyle(color: AppTheme.warningOrange),
                ),
              ],
            ),
          ),
          Expanded(
            child: _results.isEmpty
                ? const _NoResults()
                : LayoutBuilder(
                    builder: (context, constraints) {
                      final columns = constraints.maxWidth >= 700 ? 4 : 2;
                      return GridView.builder(
                        padding: const EdgeInsets.fromLTRB(16, 8, 16, 24),
                        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: columns,
                          mainAxisSpacing: 12,
                          crossAxisSpacing: 12,
                          childAspectRatio: constraints.maxWidth < 370
                              ? 0.57
                              : 0.64,
                        ),
                        itemCount: _results.length,
                        itemBuilder: (context, index) {
                          final product = _results[index];
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
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}

class _NoResults extends StatelessWidget {
  const _NoResults();

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Padding(
        padding: EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.search_off, size: 48, color: AppTheme.lightText),
            SizedBox(height: 12),
            Text(
              'No products match this search.',
              style: TextStyle(fontWeight: FontWeight.w700),
            ),
            SizedBox(height: 6),
            Text(
              'Try a product name or category. More products will be added after pilot approval.',
              textAlign: TextAlign.center,
              style: TextStyle(color: AppTheme.lightText, height: 1.4),
            ),
          ],
        ),
      ),
    );
  }
}
