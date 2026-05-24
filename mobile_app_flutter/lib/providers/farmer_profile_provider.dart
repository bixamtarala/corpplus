import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../models/farmer_profile.dart';
import 'api_providers.dart';
import 'auth_provider.dart';

class FarmerProfileState {
  const FarmerProfileState({
    required this.isLoading,
    required this.isSaving,
    this.profile,
    this.statusMessage,
    this.errorMessage,
  });

  factory FarmerProfileState.initial() {
    return const FarmerProfileState(
      isLoading: false,
      isSaving: false,
    );
  }

  final bool isLoading;
  final bool isSaving;
  final FarmerProfile? profile;
  final String? statusMessage;
  final String? errorMessage;

  FarmerProfileState copyWith({
    bool? isLoading,
    bool? isSaving,
    FarmerProfile? profile,
    String? statusMessage,
    String? errorMessage,
    bool clearStatus = false,
    bool clearError = false,
  }) {
    return FarmerProfileState(
      isLoading: isLoading ?? this.isLoading,
      isSaving: isSaving ?? this.isSaving,
      profile: profile ?? this.profile,
      statusMessage: clearStatus ? null : statusMessage ?? this.statusMessage,
      errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
    );
  }
}

class FarmerProfileController extends StateNotifier<FarmerProfileState> {
  FarmerProfileController(this._ref) : super(FarmerProfileState.initial());

  final Ref _ref;

  Future<void> loadProfile() async {
    final l10n = AppStrings(_ref.read(appLocaleProvider));
    final session = _ref.read(authControllerProvider).session;
    if (session == null || session.accessToken.isEmpty) {
      state = state.copyWith(
        profile: state.profile ?? _guestProfile(),
        statusMessage: l10n.text('preview_local_draft'),
        clearError: true,
      );
      return;
    }

    state = state.copyWith(isLoading: true, clearError: true, clearStatus: true);

    try {
      final profile = await _ref.read(apiServiceProvider).getFarmerProfile(
            accessToken: session.accessToken,
          );
      state = state.copyWith(
        isLoading: false,
        profile: profile,
        statusMessage: l10n.text('farmer_profile_synced_success'),
        clearError: true,
      );
    } on DioException catch (error) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: error.response?.data['detail']?.toString() ?? l10n.text('could_not_load_farmer_profile'),
        clearStatus: true,
      );
    } on FormatException catch (error) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: error.message,
        clearStatus: true,
      );
    }
  }

  Future<void> saveProfile(FarmerProfileRequest request) async {
    final l10n = AppStrings(_ref.read(appLocaleProvider));
    final session = _ref.read(authControllerProvider).session;
    if (session == null || session.accessToken.isEmpty) {
      state = state.copyWith(
        profile: _guestProfile(request: request),
        statusMessage: l10n.text('preview_saved_locally'),
        clearError: true,
      );
      return;
    }

    state = state.copyWith(isSaving: true, clearError: true, clearStatus: true);

    try {
      final profile = await _ref.read(apiServiceProvider).createFarmerProfile(
            accessToken: session.accessToken,
            request: request,
          );
      state = state.copyWith(
        isSaving: false,
        profile: profile,
        statusMessage: l10n.text('farmer_profile_saved_success'),
        clearError: true,
      );
    } on DioException catch (error) {
      state = state.copyWith(
        isSaving: false,
        errorMessage: error.response?.data['detail']?.toString() ?? l10n.text('could_not_save_farmer_profile'),
        clearStatus: true,
      );
    } on FormatException catch (error) {
      state = state.copyWith(
        isSaving: false,
        errorMessage: error.message,
        clearStatus: true,
      );
    }
  }

  FarmerProfile _guestProfile({FarmerProfileRequest? request}) {
    final source = request;
    return FarmerProfile(
      name: source?.name ?? 'Guest Farmer',
      state: source?.state ?? 'Tamil Nadu',
      district: source?.district ?? 'Tiruppur',
      village: source?.village ?? 'Sample Village',
      landSizeAcres: source?.landSizeAcres ?? 2.5,
      soilType: source?.soilType ?? 'Loamy',
      latitude: source?.latitude ?? 11.4064,
      longitude: source?.longitude ?? 77.3506,
      bankAccount: source?.bankAccount,
      phone: 'Guest user',
      userId: 'guest-user',
      createdAt: DateTime.now(),
      kycStatus: 'guest',
    );
  }
}

final farmerProfileControllerProvider = StateNotifierProvider<FarmerProfileController, FarmerProfileState>((ref) {
  return FarmerProfileController(ref);
});