class FarmerProfileRequest {
  const FarmerProfileRequest({
    required this.name,
    required this.state,
    required this.district,
    required this.village,
    required this.landSizeAcres,
    required this.soilType,
    required this.latitude,
    required this.longitude,
    this.bankAccount,
  });

  final String name;
  final String state;
  final String district;
  final String village;
  final double landSizeAcres;
  final String soilType;
  final double latitude;
  final double longitude;
  final String? bankAccount;

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'state': state,
      'district': district,
      'village': village,
      'land_size_acres': landSizeAcres,
      'soil_type': soilType,
      'latitude': latitude,
      'longitude': longitude,
      'bank_account': bankAccount,
    };
  }
}

class FarmerProfile extends FarmerProfileRequest {
  const FarmerProfile({
    required super.name,
    required super.state,
    required super.district,
    required super.village,
    required super.landSizeAcres,
    required super.soilType,
    required super.latitude,
    required super.longitude,
    super.bankAccount,
    required this.phone,
    required this.userId,
    required this.createdAt,
    required this.kycStatus,
  });

  final String phone;
  final String userId;
  final DateTime createdAt;
  final String kycStatus;

  factory FarmerProfile.fromJson(Map<String, dynamic> json) {
    return FarmerProfile(
      name: json['name'] as String? ?? '',
      state: json['state'] as String? ?? '',
      district: json['district'] as String? ?? '',
      village: json['village'] as String? ?? '',
      landSizeAcres: (json['land_size_acres'] as num?)?.toDouble() ?? 0,
      soilType: json['soil_type'] as String? ?? '',
      latitude: (json['latitude'] as num?)?.toDouble() ?? 0,
      longitude: (json['longitude'] as num?)?.toDouble() ?? 0,
      bankAccount: json['bank_account'] as String?,
      phone: json['phone'] as String? ?? '',
      userId: json['user_id'] as String? ?? '',
      createdAt: DateTime.tryParse(json['created_at'] as String? ?? '') ?? DateTime.now(),
      kycStatus: json['kyc_status'] as String? ?? 'pending',
    );
  }
}