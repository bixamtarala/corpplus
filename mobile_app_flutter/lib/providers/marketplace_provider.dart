import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/marketplace.dart';
import 'api_providers.dart';
import 'auth_provider.dart';

class MarketplaceState {
  const MarketplaceState({
    required this.isLoadingBuyOrders,
    required this.isSavingListing,
    required this.isMakingOffer,
    required this.buyOrders,
    required this.sellOrders,
    this.latestOffer,
    this.statusMessage,
    this.errorMessage,
  });

  factory MarketplaceState.initial() {
    return const MarketplaceState(
      isLoadingBuyOrders: false,
      isSavingListing: false,
      isMakingOffer: false,
      buyOrders: [],
      sellOrders: [],
    );
  }

  final bool isLoadingBuyOrders;
  final bool isSavingListing;
  final bool isMakingOffer;
  final List<MarketplaceSearchResult> buyOrders;
  final List<MarketplaceListing> sellOrders;
  final MarketplaceOffer? latestOffer;
  final String? statusMessage;
  final String? errorMessage;

  MarketplaceState copyWith({
    bool? isLoadingBuyOrders,
    bool? isSavingListing,
    bool? isMakingOffer,
    List<MarketplaceSearchResult>? buyOrders,
    List<MarketplaceListing>? sellOrders,
    MarketplaceOffer? latestOffer,
    String? statusMessage,
    String? errorMessage,
    bool clearStatus = false,
    bool clearError = false,
  }) {
    return MarketplaceState(
      isLoadingBuyOrders: isLoadingBuyOrders ?? this.isLoadingBuyOrders,
      isSavingListing: isSavingListing ?? this.isSavingListing,
      isMakingOffer: isMakingOffer ?? this.isMakingOffer,
      buyOrders: buyOrders ?? this.buyOrders,
      sellOrders: sellOrders ?? this.sellOrders,
      latestOffer: latestOffer ?? this.latestOffer,
      statusMessage: clearStatus ? null : statusMessage ?? this.statusMessage,
      errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
    );
  }
}

class MarketplaceController extends StateNotifier<MarketplaceState> {
  MarketplaceController(this._ref) : super(MarketplaceState.initial());

  final Ref _ref;

  Future<void> loadBuyOrders({required String crop, String? stateFilter}) async {
    state = state.copyWith(isLoadingBuyOrders: true, clearError: true, clearStatus: true);
    try {
      final results = await _ref.read(apiServiceProvider).searchListings(
            crop: crop,
            state: stateFilter,
          );
      state = state.copyWith(
        isLoadingBuyOrders: false,
        buyOrders: results,
        statusMessage: results.isEmpty ? 'No active listings found.' : 'Marketplace listings synced.',
        clearError: true,
      );
    } on DioException catch (error) {
      state = state.copyWith(
        isLoadingBuyOrders: false,
        errorMessage: error.response?.data['detail']?.toString() ?? 'Could not load marketplace listings.',
        clearStatus: true,
      );
    }
  }

  Future<void> createListing(MarketplaceListingRequest request) async {
    final session = _ref.read(authControllerProvider).session;
    if (session == null || session.accessToken.isEmpty) {
      final listing = MarketplaceListing(
        cropId: request.cropId,
        quantityKg: request.quantityKg,
        qualityGrade: request.qualityGrade,
        pricePerKg: request.pricePerKg,
        availableDate: request.availableDate,
        description: request.description,
        listingId: 'guest-${DateTime.now().millisecondsSinceEpoch}',
        userId: 'guest-user',
        createdAt: DateTime.now(),
        status: 'draft',
        views: 0,
      );
      state = state.copyWith(
        sellOrders: [listing, ...state.sellOrders],
        statusMessage: 'Preview mode: listing saved locally as a draft.',
        clearError: true,
      );
      return;
    }

    state = state.copyWith(isSavingListing: true, clearError: true, clearStatus: true);
    try {
      final listing = await _ref.read(apiServiceProvider).createListing(
            accessToken: session.accessToken,
            request: request,
          );
      state = state.copyWith(
        isSavingListing: false,
        sellOrders: [listing, ...state.sellOrders],
        statusMessage: 'Listing created successfully.',
        clearError: true,
      );
    } on DioException catch (error) {
      state = state.copyWith(
        isSavingListing: false,
        errorMessage: error.response?.data['detail']?.toString() ?? 'Could not create listing.',
        clearStatus: true,
      );
    }
  }

  Future<void> makeOffer(MarketplaceOfferRequest request) async {
    final session = _ref.read(authControllerProvider).session;
    if (session == null || session.accessToken.isEmpty) {
      final offer = MarketplaceOffer(
        listingId: request.listingId,
        offeredPricePerKg: request.offeredPricePerKg,
        quantityKg: request.quantityKg,
        pickupLocation: request.pickupLocation,
        message: request.message,
        offerId: 'guest-offer-${DateTime.now().millisecondsSinceEpoch}',
        createdAt: DateTime.now(),
        status: 'draft',
      );
      state = state.copyWith(
        latestOffer: offer,
        statusMessage: 'Preview mode: offer saved locally for later sync.',
        clearError: true,
      );
      return;
    }

    state = state.copyWith(isMakingOffer: true, clearError: true, clearStatus: true);
    try {
      final offer = await _ref.read(apiServiceProvider).makeOffer(
            accessToken: session.accessToken,
            request: request,
          );
      state = state.copyWith(
        isMakingOffer: false,
        latestOffer: offer,
        statusMessage: 'Offer submitted successfully.',
        clearError: true,
      );
    } on DioException catch (error) {
      state = state.copyWith(
        isMakingOffer: false,
        errorMessage: error.response?.data['detail']?.toString() ?? 'Could not submit offer.',
        clearStatus: true,
      );
    }
  }
}

final marketplaceControllerProvider = StateNotifierProvider<MarketplaceController, MarketplaceState>((ref) {
  return MarketplaceController(ref);
});