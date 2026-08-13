import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../data/commerce_catalog.dart';
import '../models/commerce_product.dart';

class CartState {
  const CartState({this.quantities = const {}});

  final Map<String, int> quantities;

  int quantityFor(String productId) => quantities[productId] ?? 0;

  int get itemCount =>
      quantities.values.fold(0, (total, quantity) => total + quantity);

  int get previewSubtotalPaise => quantities.entries.fold(0, (total, entry) {
    final product = CommerceCatalog.products.firstWhere(
      (item) => item.id == entry.key,
    );
    return total + product.previewPricePaise * entry.value;
  });

  List<CartLine> get lines => quantities.entries.map((entry) {
    final product = CommerceCatalog.products.firstWhere(
      (item) => item.id == entry.key,
    );
    return CartLine(product: product, quantity: entry.value);
  }).toList();
}

class CartLine {
  const CartLine({required this.product, required this.quantity});

  final CommerceProduct product;
  final int quantity;

  int get previewTotalPaise => product.previewPricePaise * quantity;
}

class CartController extends StateNotifier<CartState> {
  CartController() : super(const CartState());

  void add(String productId) =>
      setQuantity(productId, state.quantityFor(productId) + 1);

  void removeOne(String productId) =>
      setQuantity(productId, state.quantityFor(productId) - 1);

  void remove(String productId) => setQuantity(productId, 0);

  void setQuantity(String productId, int quantity) {
    final next = Map<String, int>.from(state.quantities);
    if (quantity <= 0) {
      next.remove(productId);
    } else {
      next[productId] = quantity.clamp(1, 99);
    }
    state = CartState(quantities: Map.unmodifiable(next));
  }

  void clear() => state = const CartState();
}

final cartControllerProvider = StateNotifierProvider<CartController, CartState>(
  (ref) {
    return CartController();
  },
);

class DeliveryLocationState {
  const DeliveryLocationState({this.pincode, this.validationMessage});

  final String? pincode;
  final String? validationMessage;

  bool get hasPincode => pincode != null;
}

class DeliveryLocationController extends StateNotifier<DeliveryLocationState> {
  DeliveryLocationController() : super(const DeliveryLocationState());

  bool setPincode(String value) {
    final normalized = value.trim();
    if (!RegExp(r'^\d{6}$').hasMatch(normalized)) {
      state = const DeliveryLocationState(
        validationMessage: 'Enter a valid 6-digit Indian pincode.',
      );
      return false;
    }

    state = DeliveryLocationState(
      pincode: normalized,
      validationMessage:
          'Pilot availability is not confirmed yet. Browsing and preview cart remain available.',
    );
    return true;
  }
}

final deliveryLocationProvider =
    StateNotifierProvider<DeliveryLocationController, DeliveryLocationState>((
      ref,
    ) {
      return DeliveryLocationController();
    });
