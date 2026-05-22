import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/auth_session.dart';
import 'api_providers.dart';

class AuthState {
  const AuthState({
    required this.isInitialized,
    required this.isLoading,
    required this.isAuthenticated,
    required this.isOtpRequested,
    required this.phoneNumber,
    required this.displayName,
    this.statusMessage,
    this.errorMessage,
    this.session,
  });

  factory AuthState.initial() {
    return const AuthState(
      isInitialized: false,
      isLoading: false,
      isAuthenticated: false,
      isOtpRequested: false,
      phoneNumber: '',
      displayName: 'CropPulse User',
    );
  }

  final bool isInitialized;
  final bool isLoading;
  final bool isAuthenticated;
  final bool isOtpRequested;
  final String phoneNumber;
  final String displayName;
  final String? statusMessage;
  final String? errorMessage;
  final AuthSession? session;

  AuthState copyWith({
    bool? isInitialized,
    bool? isLoading,
    bool? isAuthenticated,
    bool? isOtpRequested,
    String? phoneNumber,
    String? displayName,
    String? statusMessage,
    String? errorMessage,
    AuthSession? session,
    bool clearStatus = false,
    bool clearError = false,
  }) {
    return AuthState(
      isInitialized: isInitialized ?? this.isInitialized,
      isLoading: isLoading ?? this.isLoading,
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      isOtpRequested: isOtpRequested ?? this.isOtpRequested,
      phoneNumber: phoneNumber ?? this.phoneNumber,
      displayName: displayName ?? this.displayName,
      statusMessage: clearStatus ? null : statusMessage ?? this.statusMessage,
      errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
      session: session ?? this.session,
    );
  }
}

class AuthController extends StateNotifier<AuthState> {
  AuthController(this._ref) : super(AuthState.initial()) {
    _restoreSession();
  }

  static const _tokenKey = 'auth_access_token';
  static const _tokenTypeKey = 'auth_token_type';
  static const _userIdKey = 'auth_user_id';
  static const _phoneKey = 'auth_phone';

  final Ref _ref;

  Future<void> _restoreSession() async {
    final prefs = await _ref.read(sharedPreferencesProvider.future);
    final token = prefs.getString(_tokenKey);
    final phone = prefs.getString(_phoneKey);

    if (token == null || phone == null) {
      state = state.copyWith(isInitialized: true, clearError: true, clearStatus: true);
      return;
    }

    final session = AuthSession.fromStorage({
      'access_token': token,
      'token_type': prefs.getString(_tokenTypeKey),
      'user_id': prefs.getString(_userIdKey),
      'phone': phone,
    });

    state = state.copyWith(
      isInitialized: true,
      isAuthenticated: true,
      session: session,
      phoneNumber: session.phone,
      displayName: _displayNameFromPhone(session.phone),
      clearError: true,
      clearStatus: true,
    );
  }

  Future<void> requestOtp(String phoneNumber) async {
    state = state.copyWith(
      isLoading: true,
      phoneNumber: phoneNumber,
      clearError: true,
      clearStatus: true,
    );

    try {
      final result = await _ref.read(apiServiceProvider).requestOtp(phoneNumber);
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        isOtpRequested: true,
        phoneNumber: result.phone,
        statusMessage: '${result.message}. Use the mock code 123456 for now.',
        clearError: true,
      );
    } on DioException catch (error) {
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        errorMessage: error.response?.data['detail']?.toString() ?? 'Could not request OTP.',
        clearStatus: true,
      );
    } on FormatException catch (error) {
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        errorMessage: error.message,
        clearStatus: true,
      );
    }
  }

  Future<void> verifyOtp(String otp) async {
    state = state.copyWith(isLoading: true, clearError: true, clearStatus: true);

    try {
      final session = await _ref.read(apiServiceProvider).verifyOtp(
            phoneNumber: state.phoneNumber,
            otp: otp,
          );
      final prefs = await _ref.read(sharedPreferencesProvider.future);
      await prefs.setString(_tokenKey, session.accessToken);
      await prefs.setString(_tokenTypeKey, session.tokenType);
      await prefs.setString(_userIdKey, session.userId);
      await prefs.setString(_phoneKey, session.phone);

      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        isAuthenticated: true,
        isOtpRequested: false,
        session: session,
        phoneNumber: session.phone,
        displayName: _displayNameFromPhone(session.phone),
        statusMessage: 'Signed in successfully.',
        clearError: true,
      );
    } on DioException catch (error) {
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        errorMessage: error.response?.data['detail']?.toString() ?? 'Could not verify OTP.',
        clearStatus: true,
      );
    } on FormatException catch (error) {
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        errorMessage: error.message,
        clearStatus: true,
      );
    }
  }

  Future<void> logout() async {
    final prefs = await _ref.read(sharedPreferencesProvider.future);
    await prefs.remove(_tokenKey);
    await prefs.remove(_tokenTypeKey);
    await prefs.remove(_userIdKey);
    await prefs.remove(_phoneKey);

    state = AuthState.initial().copyWith(isInitialized: true);
  }

  String _displayNameFromPhone(String phone) {
    final visible = phone.length >= 4 ? phone.substring(phone.length - 4) : phone;
    return 'User $visible';
  }
}

final authControllerProvider = StateNotifierProvider<AuthController, AuthState>((ref) {
  return AuthController(ref);
});