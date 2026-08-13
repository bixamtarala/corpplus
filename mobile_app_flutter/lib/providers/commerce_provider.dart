import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../models/commerce_api_models.dart';
import '../services/api_service.dart';
import 'api_providers.dart';
import 'auth_provider.dart';

enum LoadStatus { initial, loading, ready, offline, error }

class CatalogState {
  const CatalogState({
    this.status = LoadStatus.initial,
    this.categories = const [],
    this.products = const [],
    this.message,
  });
  final LoadStatus status;
  final List<CommerceCategory> categories;
  final List<CommerceProduct> products;
  final String? message;
}

class CatalogController extends StateNotifier<CatalogState> {
  CatalogController(this._ref) : super(const CatalogState()) {
    _ref.listen<Locale>(
      appLocaleProvider,
      (_, locale) => load(locale.languageCode),
    );
    load(_ref.read(appLocaleProvider).languageCode);
  }
  final Ref _ref;
  Future<void> load(String locale) async {
    state = CatalogState(
      status: LoadStatus.loading,
      categories: state.categories,
      products: state.products,
    );
    try {
      final api = _ref.read(apiServiceProvider);
      final results = await Future.wait([
        api.getCommerceCategories(locale: locale),
        api.getCommerceProducts(locale: locale),
      ]);
      state = CatalogState(
        status: LoadStatus.ready,
        categories: results[0] as List<CommerceCategory>,
        products: results[1] as List<CommerceProduct>,
      );
    } catch (error) {
      final message = commerceErrorMessage(error);
      state = CatalogState(
        status: message == 'offline' ? LoadStatus.offline : LoadStatus.error,
        categories: state.categories,
        products: state.products,
        message: message,
      );
    }
  }

  List<CommerceProduct> productsFor(String? slug) => slug == null
      ? state.products
      : state.products.where((p) => p.category.slug == slug).toList();
}

final catalogControllerProvider =
    StateNotifierProvider<CatalogController, CatalogState>(
      (ref) => CatalogController(ref),
    );

class DeliveryLocationState {
  const DeliveryLocationState({
    this.status = LoadStatus.initial,
    this.pincode,
    this.decision,
    this.message,
  });
  final LoadStatus status;
  final String? pincode;
  final ServiceabilityDecision? decision;
  final String? message;
  bool get hasPincode => pincode != null;
}

class DeliveryLocationController extends StateNotifier<DeliveryLocationState> {
  DeliveryLocationController(this._ref) : super(const DeliveryLocationState());
  final Ref _ref;
  Future<bool> setPincode(String value) async {
    final normalized = value.trim();
    if (!RegExp(r'^[1-9][0-9]{5}$').hasMatch(normalized)) {
      state = const DeliveryLocationState(
        status: LoadStatus.error,
        message: 'invalid_pincode',
      );
      return false;
    }
    state = DeliveryLocationState(
      status: LoadStatus.loading,
      pincode: normalized,
    );
    try {
      final decision = await _ref
          .read(apiServiceProvider)
          .checkServiceability(normalized);
      state = DeliveryLocationState(
        status: LoadStatus.ready,
        pincode: normalized,
        decision: decision,
      );
      await _ref
          .read(cartControllerProvider.notifier)
          .selectGuestPincode(normalized);
      return true;
    } catch (error) {
      final message = commerceErrorMessage(error);
      state = DeliveryLocationState(
        status: message == 'offline' ? LoadStatus.offline : LoadStatus.error,
        pincode: normalized,
        message: message,
      );
      return false;
    }
  }
}

final deliveryLocationProvider =
    StateNotifierProvider<DeliveryLocationController, DeliveryLocationState>(
      (ref) => DeliveryLocationController(ref),
    );

class CartState {
  const CartState({this.status = LoadStatus.initial, this.cart, this.message});
  final LoadStatus status;
  final CommerceCart? cart;
  final String? message;
  int get itemCount => cart?.itemCount ?? 0;
  double quantityForSku(String skuId) =>
      cart?.items.where((item) => item.skuId == skuId).firstOrNull?.quantity ??
      0;
}

class CartController extends StateNotifier<CartState> {
  CartController(this._ref) : super(const CartState()) {
    _ref.listen<AuthState>(authControllerProvider, (previous, next) {
      if (next.isInitialized &&
          previous?.isAuthenticated != next.isAuthenticated) {
        initialize();
      }
    });
    initialize();
  }
  static const guestTokenKey = 'commerce_guest_cart_token';
  final Ref _ref;

  Future<void> initialize() async {
    state = CartState(status: LoadStatus.loading, cart: state.cart);
    final auth = _ref.read(authControllerProvider);
    if (!auth.isInitialized) return;
    try {
      final api = _ref.read(apiServiceProvider);
      final storage = _ref.read(secureStorageProvider);
      final guestToken = await storage.read(guestTokenKey);
      CommerceCart cart;
      if (auth.isAuthenticated && auth.session != null) {
        if (guestToken != null) {
          cart = await api.mergeGuestCart(
            accessToken: auth.session!.accessToken,
            guestToken: guestToken,
          );
          await storage.delete(guestTokenKey);
        } else {
          cart = await api.restoreCart(accessToken: auth.session!.accessToken);
        }
      } else if (guestToken != null) {
        try {
          cart = await api.restoreCart(guestToken: guestToken);
        } catch (_) {
          await storage.delete(guestTokenKey);
          cart = await _createGuest();
        }
      } else {
        cart = await _createGuest();
      }
      state = CartState(status: LoadStatus.ready, cart: cart);
    } catch (error) {
      _setError(error);
    }
  }

  Future<CommerceCart> _createGuest() async {
    final cart = await _ref.read(apiServiceProvider).createGuestCart();
    if (cart.guestToken != null) {
      await _ref
          .read(secureStorageProvider)
          .write(guestTokenKey, cart.guestToken!);
    }
    return cart;
  }

  Future<void> selectGuestPincode(String pincode) async {
    final auth = _ref.read(authControllerProvider);
    if (auth.isAuthenticated || state.cart == null) return;
    await _mutate(
      (api, token, access, cart) => api.setCartContext(
        guestToken: token,
        pincode: pincode,
        version: cart.version,
      ),
    );
  }

  Future<void> selectAddress(String addressId) async => _mutate(
    (api, token, access, cart) => api.setCartContext(
      accessToken: access,
      addressId: addressId,
      version: cart.version,
    ),
  );
  Future<void> addSku(CommerceSku sku) async => _mutate(
    (api, token, access, cart) => api.addCartItem(
      accessToken: access,
      guestToken: token,
      skuId: sku.id,
      quantity: sku.minimumOrderQuantity,
      version: cart.version,
    ),
  );
  Future<void> updateItem(CommerceCartItem item, double quantity) async {
    if (quantity <= 0) return removeItem(item);
    await _mutate(
      (api, token, access, cart) => api.updateCartItem(
        accessToken: access,
        guestToken: token,
        itemId: item.id,
        quantity: quantity,
        version: cart.version,
      ),
    );
  }

  Future<void> removeItem(CommerceCartItem item) async => _mutate(
    (api, token, access, cart) => api.deleteCartItem(
      accessToken: access,
      guestToken: token,
      itemId: item.id,
      version: cart.version,
    ),
  );

  Future<void> _mutate(
    Future<CommerceCart> Function(
      ApiService api,
      String? guestToken,
      String? accessToken,
      CommerceCart cart,
    )
    action,
  ) async {
    final cart = state.cart;
    if (cart == null) return;
    state = CartState(status: LoadStatus.loading, cart: cart);
    try {
      final auth = _ref.read(authControllerProvider);
      final guest = await _ref.read(secureStorageProvider).read(guestTokenKey);
      final updated = await action(
        _ref.read(apiServiceProvider),
        guest,
        auth.session?.accessToken,
        cart,
      );
      state = CartState(status: LoadStatus.ready, cart: updated);
    } catch (error) {
      _setError(error);
    }
  }

  void _setError(Object error) {
    final message = commerceErrorMessage(error);
    state = CartState(
      status: message == 'offline' ? LoadStatus.offline : LoadStatus.error,
      cart: state.cart,
      message: message,
    );
  }
}

final cartControllerProvider = StateNotifierProvider<CartController, CartState>(
  (ref) => CartController(ref),
);

class AddressState {
  const AddressState({
    this.status = LoadStatus.initial,
    this.items = const [],
    this.message,
  });
  final LoadStatus status;
  final List<CommerceAddress> items;
  final String? message;
}

class AddressController extends StateNotifier<AddressState> {
  AddressController(this._ref) : super(const AddressState());
  final Ref _ref;
  Future<void> load() async {
    final token = _ref.read(authControllerProvider).session?.accessToken;
    if (token == null) return;
    state = AddressState(status: LoadStatus.loading, items: state.items);
    try {
      state = AddressState(
        status: LoadStatus.ready,
        items: await _ref.read(apiServiceProvider).getAddresses(token),
      );
    } catch (error) {
      final message = commerceErrorMessage(error);
      state = AddressState(
        status: message == 'offline' ? LoadStatus.offline : LoadStatus.error,
        items: state.items,
        message: message,
      );
    }
  }

  Future<bool> save(Map<String, dynamic> data, {String? id}) async {
    final token = _ref.read(authControllerProvider).session?.accessToken;
    if (token == null) return false;
    try {
      await _ref
          .read(apiServiceProvider)
          .saveAddress(accessToken: token, data: data, addressId: id);
      await load();
      return true;
    } catch (error) {
      state = AddressState(
        status: LoadStatus.error,
        items: state.items,
        message: commerceErrorMessage(error),
      );
      return false;
    }
  }

  Future<void> delete(String id) async {
    final token = _ref.read(authControllerProvider).session?.accessToken;
    if (token == null) return;
    await _ref
        .read(apiServiceProvider)
        .deleteAddress(accessToken: token, addressId: id);
    await load();
  }

  Future<void> setDefault(String id) async {
    final token = _ref.read(authControllerProvider).session?.accessToken;
    if (token == null) return;
    await _ref
        .read(apiServiceProvider)
        .setDefaultAddress(accessToken: token, addressId: id);
    await load();
  }
}

final addressControllerProvider =
    StateNotifierProvider<AddressController, AddressState>(
      (ref) => AddressController(ref),
    );
