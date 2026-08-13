import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../models/commerce_api_models.dart';
import '../providers/api_providers.dart';
import '../services/api_service.dart';
import '../widgets/commerce_product_card.dart';
import 'product_detail_screen.dart';

class CommerceSearchScreen extends ConsumerStatefulWidget {
  const CommerceSearchScreen({super.key});
  @override
  ConsumerState<CommerceSearchScreen> createState() => _State();
}

class _State extends ConsumerState<CommerceSearchScreen> {
  final controller = TextEditingController();
  List<CommerceProduct> results = const [];
  bool loading = false;
  String? error;
  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  Future<void> search() async {
    setState(() {
      loading = true;
      error = null;
    });
    try {
      final items = await ref
          .read(apiServiceProvider)
          .getCommerceProducts(
            locale: Localizations.localeOf(context).languageCode,
            query: controller.text,
          );
      if (mounted) setState(() => results = items);
    } catch (e) {
      if (mounted) setState(() => error = commerceErrorMessage(e));
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(l10n.text('search'))),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: controller,
              textInputAction: TextInputAction.search,
              onSubmitted: (_) => search(),
              decoration: InputDecoration(
                hintText: l10n.text('search_products'),
                prefixIcon: const Icon(Icons.search),
                suffixIcon: IconButton(
                  onPressed: search,
                  icon: const Icon(Icons.arrow_forward),
                ),
              ),
            ),
          ),
          if (loading) const LinearProgressIndicator(),
          if (error != null)
            Padding(
              padding: const EdgeInsets.all(12),
              child: Text(
                error == 'offline' ? l10n.text('commerce_offline') : error!,
                style: const TextStyle(color: Colors.red),
              ),
            ),
          Expanded(
            child: results.isEmpty
                ? Center(child: Text(l10n.text('search_prompt')))
                : GridView.builder(
                    padding: const EdgeInsets.all(16),
                    gridDelegate:
                        const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 2,
                          mainAxisSpacing: 12,
                          crossAxisSpacing: 12,
                          childAspectRatio: .64,
                        ),
                    itemCount: results.length,
                    itemBuilder: (_, i) => CommerceProductCard(
                      product: results[i],
                      onOpen: () => Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) =>
                              ProductDetailScreen(product: results[i]),
                        ),
                      ),
                    ),
                  ),
          ),
        ],
      ),
    );
  }
}
