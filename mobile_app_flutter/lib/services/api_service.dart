import 'package:dio/dio.dart';

import '../models/auth_session.dart';
import '../models/farmer_profile.dart';
import '../models/marketplace.dart';
import '../models/price_insight.dart';

class ApiService {
  ApiService({Dio? dio})
      : _dio = dio ??
            Dio(
              BaseOptions(
                baseUrl: _baseUrl,
                connectTimeout: const Duration(seconds: 4),
                receiveTimeout: const Duration(seconds: 4),
                sendTimeout: const Duration(seconds: 4),
                headers: const {
                  'Content-Type': 'application/json',
                },
              ),
            );

  static const String _baseUrl = String.fromEnvironment(
    'CROPPULSE_API_BASE_URL',
    defaultValue: 'http://10.0.2.2:8000',
  );

  final Dio _dio;

  Future<OtpRequestResult> requestOtp(String phoneNumber) async {
    final formattedPhone = _normalizeIndianPhone(phoneNumber);

    final response = await _dio.post<Map<String, dynamic>>(
      '/api/v2/auth/request-otp',
      data: {'phone': formattedPhone},
    );

    final data = response.data ?? const <String, dynamic>{};
    return OtpRequestResult(
      phone: (data['phone'] as String?) ?? formattedPhone,
      message: (data['message'] as String?) ?? 'OTP sent',
      expiresInSeconds: (data['expires_in_seconds'] as num?)?.toInt() ?? 600,
    );
  }

  Future<AuthSession> verifyOtp({
    required String phoneNumber,
    required String otp,
  }) async {
    final response = await _dio.post<Map<String, dynamic>>(
      '/api/v2/auth/verify-otp',
      data: {
        'phone': _normalizeIndianPhone(phoneNumber),
        'otp': otp,
      },
    );

    final data = response.data;
    if (data == null) {
      throw const FormatException('Empty auth response body');
    }

    return AuthSession.fromJson(data);
  }

  Future<FarmerProfile> getFarmerProfile({
    required String accessToken,
  }) async {
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
        .map((item) => MarketplaceSearchResult.fromJson(item as Map<String, dynamic>))
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

  Future<PriceInsight> getPriceInsight(PriceInsightRequestPayload request) async {
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
      analysis: 'Live API was unavailable, so this recommendation uses offline benchmark data for ${request.state}.',
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
    return Options(
      headers: {
        'Authorization': 'Bearer $accessToken',
      },
    );
  }
}