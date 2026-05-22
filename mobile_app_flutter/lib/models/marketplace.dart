class MarketplaceListingRequest {
  const MarketplaceListingRequest({
    required this.cropId,
    required this.quantityKg,
    required this.qualityGrade,
    required this.pricePerKg,
    required this.availableDate,
    this.description,
  });

  final String cropId;
  final double quantityKg;
  final String qualityGrade;
  final double pricePerKg;
  final String availableDate;
  final String? description;

  Map<String, dynamic> toJson() {
    return {
      'crop_id': cropId,
      'quantity_kg': quantityKg,
      'quality_grade': qualityGrade,
      'price_per_kg': pricePerKg,
      'available_date': availableDate,
      'description': description,
    };
  }
}

class MarketplaceListing extends MarketplaceListingRequest {
  const MarketplaceListing({
    required super.cropId,
    required super.quantityKg,
    required super.qualityGrade,
    required super.pricePerKg,
    required super.availableDate,
    super.description,
    required this.listingId,
    required this.userId,
    required this.createdAt,
    required this.status,
    required this.views,
  });

  final String listingId;
  final String userId;
  final DateTime createdAt;
  final String status;
  final int views;

  factory MarketplaceListing.fromJson(Map<String, dynamic> json) {
    return MarketplaceListing(
      cropId: json['crop_id'] as String? ?? '',
      quantityKg: (json['quantity_kg'] as num?)?.toDouble() ?? 0,
      qualityGrade: json['quality_grade'] as String? ?? '',
      pricePerKg: (json['price_per_kg'] as num?)?.toDouble() ?? 0,
      availableDate: json['available_date'] as String? ?? '',
      description: json['description'] as String?,
      listingId: json['listing_id'] as String? ?? '',
      userId: json['user_id'] as String? ?? '',
      createdAt: DateTime.tryParse(json['created_at'] as String? ?? '') ?? DateTime.now(),
      status: json['status'] as String? ?? 'active',
      views: (json['views'] as num?)?.toInt() ?? 0,
    );
  }
}

class MarketplaceSearchResult {
  const MarketplaceSearchResult({
    required this.listingId,
    required this.crop,
    required this.farmerName,
    required this.quantityKg,
    required this.qualityGrade,
    required this.pricePerKg,
    required this.availableDate,
    required this.state,
    required this.district,
  });

  final String listingId;
  final String crop;
  final String farmerName;
  final double quantityKg;
  final String qualityGrade;
  final double pricePerKg;
  final String availableDate;
  final String state;
  final String district;

  factory MarketplaceSearchResult.fromJson(Map<String, dynamic> json) {
    final location = json['location'] as Map<String, dynamic>? ?? const <String, dynamic>{};
    return MarketplaceSearchResult(
      listingId: json['listing_id'] as String? ?? '',
      crop: json['crop'] as String? ?? '',
      farmerName: json['farmer_name'] as String? ?? 'Farmer',
      quantityKg: (json['quantity_kg'] as num?)?.toDouble() ?? 0,
      qualityGrade: json['quality_grade'] as String? ?? '',
      pricePerKg: (json['price_per_kg'] as num?)?.toDouble() ?? 0,
      availableDate: json['available_date'] as String? ?? '',
      state: location['state'] as String? ?? '',
      district: location['district'] as String? ?? '',
    );
  }
}

class MarketplaceOfferRequest {
  const MarketplaceOfferRequest({
    required this.listingId,
    required this.offeredPricePerKg,
    required this.quantityKg,
    required this.pickupLocation,
    this.message,
  });

  final String listingId;
  final double offeredPricePerKg;
  final double quantityKg;
  final String pickupLocation;
  final String? message;

  Map<String, dynamic> toJson() {
    return {
      'listing_id': listingId,
      'offered_price_per_kg': offeredPricePerKg,
      'quantity_kg': quantityKg,
      'pickup_location': pickupLocation,
      'message': message,
    };
  }
}

class MarketplaceOffer extends MarketplaceOfferRequest {
  const MarketplaceOffer({
    required super.listingId,
    required super.offeredPricePerKg,
    required super.quantityKg,
    required super.pickupLocation,
    super.message,
    required this.offerId,
    required this.createdAt,
    required this.status,
  });

  final String offerId;
  final DateTime createdAt;
  final String status;

  factory MarketplaceOffer.fromJson(Map<String, dynamic> json) {
    return MarketplaceOffer(
      listingId: json['listing_id'] as String? ?? '',
      offeredPricePerKg: (json['offered_price_per_kg'] as num?)?.toDouble() ?? 0,
      quantityKg: (json['quantity_kg'] as num?)?.toDouble() ?? 0,
      pickupLocation: json['pickup_location'] as String? ?? '',
      message: json['message'] as String?,
      offerId: json['offer_id'] as String? ?? '',
      createdAt: DateTime.tryParse(json['created_at'] as String? ?? '') ?? DateTime.now(),
      status: json['status'] as String? ?? 'pending',
    );
  }
}