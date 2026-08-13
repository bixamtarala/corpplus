import 'package:dio/dio.dart';

import '../models/auth_session.dart';
import '../models/commerce_api_models.dart';
import '../models/farmer_profile.dart';
import '../models/marketplace.dart';
import '../models/price_insight.dart';

class ApiService {
  ApiService({Dio? dio})
    : _dio =
          dio ??
          Dio(
            BaseOptions(
              baseUrl: _baseUrl,
              connectTimeout: const Duration(seconds: 4),
              receiveTimeout: const Duration(seconds: 4),
              sendTimeout: const Duration(seconds: 4),
              headers: const {'Content-Type': 'application/json'},
            ),
          );

  static const String _baseUrl = String.fromEnvironment(
    'CROPPULSE_API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  final Dio _dio;
  String _pendingChallengeId = '';

  Future<OtpRequestResult> requestOtp(String phoneNumber) async {
    final formattedPhone = _normalizeIndianPhone(phoneNumber);

    final response = await _dio.post<Map<String, dynamic>>(
      '/api/commerce/v1/auth/otp/request',
      data: {'phone': formattedPhone},
    );

    final data = response.data ?? const <String, dynamic>{};
    final result = OtpRequestResult.fromJson(data);
    _pendingChallengeId = result.challengeId;
    return result;
  }

  Future<AuthSession> verifyOtp({
    required String phoneNumber,
    required String otp,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/commerce/v1/auth/otp/verify',
      data: {
        'challenge_id': _pendingChallengeId,
        'phone': _normalizeIndianPhone(phoneNumber),
        'code': otp,
      },
    );

    final data = response.data;
    if (data == null) {
      throw const FormatException('Empty auth response body');
    }

    return AuthSession.fromJson(data);
  }

  Future<AuthSession> refreshCommerceSession(String refreshToken) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/commerce/v1/auth/refresh',
      data: {'refresh_token': refreshToken},
    );
    return AuthSession.fromJson(_requiredData(response, 'refresh'));
  }

  Future<CurrentCommerceUser> getCurrentCommerceUser(String accessToken) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/api/commerce/v1/auth/me',
      options: _authorizedOptions(accessToken),
    );
    return CurrentCommerceUser.fromJson(_requiredData(response, 'user'));
  }

  Future<void> logoutCommerce(String refreshToken) async {
    await _dio.post<void>(
      '/api/commerce/v1/auth/logout',
      data: {'refresh_token': refreshToken},
    );
  }

  Future<List<CommerceCategory>> getCommerceCategories({
    required String locale,
  }) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/api/commerce/v1/catalog/categories',
      queryParameters: {'locale': locale},
    );
    final data = _requiredData(response, 'categories');
    return (data['items'] as List<dynamic>? ?? const [])
        .map((item) => CommerceCategory.fromJson(item as Map<String, dynamic>))
        .toList(growable: false);
  }

  Future<List<CommerceProduct>> getCommerceProducts({
    required String locale,
    String? category,
    String? query,
  }) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/api/commerce/v1/catalog/products',
      queryParameters: {
        'locale': locale,
        'limit': 50,
        'category': ?category,
        if (query != null && query.trim().isNotEmpty) 'query': query.trim(),
      },
    );
    final data = _requiredData(response, 'products');
    return (data['items'] as List<dynamic>? ?? const [])
        .map((item) => CommerceProduct.fromJson(item as Map<String, dynamic>))
        .toList(growable: false);
  }

  Future<ServiceabilityDecision> checkServiceability(String pincode) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/api/commerce/v1/serviceability',
      queryParameters: {'pincode': pincode},
    );
    return ServiceabilityDecision.fromJson(
      _requiredData(response, 'serviceability'),
    );
  }

  Future<List<CommerceAddress>> getAddresses(String accessToken) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/api/commerce/v1/addresses',
      options: _authorizedOptions(accessToken),
    );
    final data = _requiredData(response, 'addresses');
    return (data['items'] as List<dynamic>? ?? const [])
        .map((item) => CommerceAddress.fromJson(item as Map<String, dynamic>))
        .toList(growable: false);
  }

  Future<CommerceAddress> saveAddress({
    required String accessToken,
    required Map<String, dynamic> data,
    String? addressId,
  }) async {
    final response = addressId == null
        ? await _dio.post<Map<String, dynamic>>(
            '/api/commerce/v1/addresses',
            data: data,
            options: _authorizedOptions(accessToken),
          )
        : await _dio.patch<Map<String, dynamic>>(
            '/api/commerce/v1/addresses/$addressId',
            data: data,
            options: _authorizedOptions(accessToken),
          );
    return CommerceAddress.fromJson(_requiredData(response, 'address'));
  }

  Future<void> deleteAddress({
    required String accessToken,
    required String addressId,
  }) => _dio.delete<void>(
    '/api/commerce/v1/addresses/$addressId',
    options: _authorizedOptions(accessToken),
  );

  Future<CommerceAddress> setDefaultAddress({
    required String accessToken,
    required String addressId,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/commerce/v1/addresses/$addressId/default',
      options: _authorizedOptions(accessToken),
    );
    return CommerceAddress.fromJson(_requiredData(response, 'address'));
  }

  Future<CommerceCart> createGuestCart({String? pincode}) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/commerce/v1/cart/guest',
      data: {'pincode': ?pincode},
    );
    return CommerceCart.fromJson(_requiredData(response, 'guest cart'));
  }

  Future<CommerceCart> restoreCart({
    String? accessToken,
    String? guestToken,
  }) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/api/commerce/v1/cart',
      options: _commerceOptions(
        accessToken: accessToken,
        guestToken: guestToken,
      ),
    );
    return CommerceCart.fromJson(_requiredData(response, 'cart'));
  }

  Future<CommerceCart> setCartContext({
    String? accessToken,
    String? guestToken,
    String? addressId,
    String? pincode,
    required int version,
  }) async {
    final response = await _dio.patch<Map<String, dynamic>>(
      '/api/commerce/v1/cart',
      data: {
        'expected_version': version,
        'address_id': ?addressId,
        'pincode': ?pincode,
      },
      options: _commerceOptions(
        accessToken: accessToken,
        guestToken: guestToken,
      ),
    );
    return CommerceCart.fromJson(_requiredData(response, 'cart'));
  }

  Future<CommerceCart> addCartItem({
    String? accessToken,
    String? guestToken,
    required String skuId,
    required double quantity,
    required int version,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/commerce/v1/cart/items',
      data: {
        'sku_id': skuId,
        'quantity': quantity,
        'expected_version': version,
      },
      options: _commerceOptions(
        accessToken: accessToken,
        guestToken: guestToken,
      ),
    );
    return CommerceCart.fromJson(_requiredData(response, 'cart'));
  }

  Future<CommerceCart> updateCartItem({
    String? accessToken,
    String? guestToken,
    required String itemId,
    required double quantity,
    required int version,
  }) async {
    final response = await _dio.patch<Map<String, dynamic>>(
      '/api/commerce/v1/cart/items/$itemId',
      data: {'quantity': quantity, 'expected_version': version},
      options: _commerceOptions(
        accessToken: accessToken,
        guestToken: guestToken,
      ),
    );
    return CommerceCart.fromJson(_requiredData(response, 'cart'));
  }

  Future<CommerceCart> deleteCartItem({
    String? accessToken,
    String? guestToken,
    required String itemId,
    required int version,
  }) async {
    final response = await _dio.delete<Map<String, dynamic>>(
      '/api/commerce/v1/cart/items/$itemId',
      queryParameters: {'expected_version': version},
      options: _commerceOptions(
        accessToken: accessToken,
        guestToken: guestToken,
      ),
    );
    return CommerceCart.fromJson(_requiredData(response, 'cart'));
  }

  Future<CommerceCart> mergeGuestCart({
    required String accessToken,
    required String guestToken,
    int? version,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/commerce/v1/cart/merge',
      data: {'expected_version': ?version},
      options: _commerceOptions(
        accessToken: accessToken,
        guestToken: guestToken,
      ),
    );
    return CommerceCart.fromJson(_requiredData(response, 'cart'));
  }

  Future<FarmerProfile> getFarmerProfile({required String accessToken}) async {
    final response = await _dio.get<Map<String, dynamic>>(
      '/api/v2/farmer/profile',
      options: _authorizedOptions(accessToken),
    );

    final data = response.data;
    if (data == null) {
      throw const FormatException('Empty farmer profile response body');
    }

    return FarmerProfile.fromJson(data);
  }

  Future<FarmerProfile> createFarmerProfile({
    required String accessToken,
    required FarmerProfileRequest request,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/v2/farmer/profile',
      data: request.toJson(),
      options: _authorizedOptions(accessToken),
    );

    final data = response.data;
    if (data == null) {
      throw const FormatException('Empty farmer profile response body');
    }

    return FarmerProfile.fromJson(data);
  }

  Future<List<MarketplaceSearchResult>> searchListings({
    required String crop,
    String? state,
    String? quality,
    double? maxPrice,
  }) async {
    final queryParameters = <String, dynamic>{'crop': crop};
    if (state?.isNotEmpty ?? false) {
      queryParameters['state'] = state;
    }
    if (quality?.isNotEmpty ?? false) {
      queryParameters['quality'] = quality;
    }
    if (maxPrice != null) {
      queryParameters['max_price'] = maxPrice;
    }

    final response = await _dio.get<Map<String, dynamic>>(
      '/api/v2/marketplace/search',
      queryParameters: queryParameters,
    );

    final data = response.data ?? const <String, dynamic>{};
    final results = (data['results'] as List<dynamic>? ?? const [])
        .map(
          (item) =>
              MarketplaceSearchResult.fromJson(item as Map<String, dynamic>),
        )
        .toList();
    return results;
  }

  Future<MarketplaceListing> createListing({
    required String accessToken,
    required MarketplaceListingRequest request,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/v2/marketplace/listings',
      data: request.toJson(),
      options: _authorizedOptions(accessToken),
    );

    final data = response.data;
    if (data == null) {
      throw const FormatException('Empty listing response body');
    }

    return MarketplaceListing.fromJson(data);
  }

  Future<MarketplaceOffer> makeOffer({
    required String accessToken,
    required MarketplaceOfferRequest request,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/v2/marketplace/offers',
      data: request.toJson(),
      options: _authorizedOptions(accessToken),
    );

    final data = response.data;
    if (data == null) {
      throw const FormatException('Empty offer response body');
    }

    return MarketplaceOffer.fromJson(data);
  }

  Future<PriceInsight> getPriceInsight(
    PriceInsightRequestPayload request,
  ) async {
    try {
      final response = await _dio.post<Map<String, dynamic>>(
        '/api/v2/intelligence/price-insight',
        data: request.toJson(),
      );

      final data = response.data;
      if (data == null) {
        throw const FormatException('Empty response body');
      }

      return PriceInsight.fromJson(data);
    } on DioException {
      return _buildFallbackInsight(request);
    } on FormatException {
      return _buildFallbackInsight(request);
    }
  }

  PriceInsight _buildFallbackInsight(PriceInsightRequestPayload request) {
    final basePrice = switch (request.crop.toLowerCase()) {
      'rice' => 2500.0,
      'wheat' => 2275.0,
      'cotton' => 6120.0,
      _ => 2400.0,
    };

    return PriceInsight(
      crop: request.crop,
      recommendedPrice: basePrice,
      marketTrend: 'rising',
      nearbyPrices: {
        'Coimbatore Mandi': basePrice - 60,
        'Erode Mandi': basePrice,
        'Salem Mandi': basePrice + 75,
      },
      bestSellingTime: 'Next 3-5 days',
      analysis:
          'Live API was unavailable, so this recommendation uses offline benchmark data for ${request.state}.',
      source: InsightSource.fallback,
    );
  }

  String _normalizeIndianPhone(String phoneNumber) {
    final digitsOnly = phoneNumber.replaceAll(RegExp(r'\D'), '');
    if (digitsOnly.length == 10) {
      return '+91$digitsOnly';
    }

    if (digitsOnly.length == 12 && digitsOnly.startsWith('91')) {
      return '+$digitsOnly';
    }

    if (phoneNumber.startsWith('+91')) {
      return phoneNumber;
    }

    throw const FormatException('Enter a valid 10-digit Indian phone number.');
  }

  Options _authorizedOptions(String accessToken) {
    return Options(headers: {'Authorization': 'Bearer $accessToken'});
  }

  Options _commerceOptions({String? accessToken, String? guestToken}) =>
      Options(
        headers: {
          if (accessToken != null) 'Authorization': 'Bearer $accessToken',
          'X-Guest-Cart-Token': ?guestToken,
        },
      );

  Map<String, dynamic> _requiredData(
    Response<Map<String, dynamic>> response,
    String label,
  ) {
    final data = response.data;
    if (data == null) throw FormatException('Empty $label response body');
    return data;
  }
}

String commerceErrorMessage(Object error) {
  if (error is DioException) {
    final data = error.response?.data;
    if (data is Map<String, dynamic>) {
      final envelope = data['error'];
      if (envelope is Map<String, dynamic> && envelope['message'] is String) {
        return envelope['message'] as String;
      }
      if (data['detail'] is String) return data['detail'] as String;
    }
    if (error.type == DioExceptionType.connectionError ||
        error.type == DioExceptionType.connectionTimeout ||
        error.type == DioExceptionType.receiveTimeout) {
      return 'offline';
    }
  }
  return error.toString();
}
