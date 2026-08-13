import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../models/auth_session.dart';
import '../services/api_service.dart';
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
  factory AuthState.initial() => const AuthState(
    isInitialized: false,
    isLoading: false,
    isAuthenticated: false,
    isOtpRequested: false,
    phoneNumber: '',
    displayName: 'CropPulse User',
  );
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
    bool clearSession = false,
  }) => AuthState(
    isInitialized: isInitialized ?? this.isInitialized,
    isLoading: isLoading ?? this.isLoading,
    isAuthenticated: isAuthenticated ?? this.isAuthenticated,
    isOtpRequested: isOtpRequested ?? this.isOtpRequested,
    phoneNumber: phoneNumber ?? this.phoneNumber,
    displayName: displayName ?? this.displayName,
    statusMessage: clearStatus ? null : statusMessage ?? this.statusMessage,
    errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
    session: clearSession ? null : session ?? this.session,
  );
}

class AuthController extends StateNotifier<AuthState> {
  AuthController(this._ref) : super(AuthState.initial()) {
    _restoreSession();
  }
  static const accessKey = 'commerce_access_token';
  static const refreshKey = 'commerce_refresh_token';
  final Ref _ref;

  Future<void> _restoreSession() async {
    final storage = _ref.read(secureStorageProvider);
    final access = await storage.read(accessKey);
    final refresh = await storage.read(refreshKey);
    if (access == null || refresh == null) {
      state = state.copyWith(isInitialized: true, clearError: true);
      return;
    }
    try {
      var session = AuthSession(
        accessToken: access,
        refreshToken: refresh,
        tokenType: 'bearer',
      );
      CurrentCommerceUser user;
      try {
        user = await _ref
            .read(apiServiceProvider)
            .getCurrentCommerceUser(access);
      } on DioException catch (error) {
        if (error.response?.statusCode != 401) rethrow;
        session = await _ref
            .read(apiServiceProvider)
            .refreshCommerceSession(refresh);
        await _saveTokens(session);
        user = await _ref
            .read(apiServiceProvider)
            .getCurrentCommerceUser(session.accessToken);
      }
      session = session.withUser(user);
      state = state.copyWith(
        isInitialized: true,
        isAuthenticated: true,
        session: session,
        phoneNumber: user.phone,
        displayName: user.displayName ?? _displayName(user.phone),
        clearError: true,
      );
    } catch (_) {
      await _clearTokens();
      state = state.copyWith(
        isInitialized: true,
        isAuthenticated: false,
        clearSession: true,
        clearError: true,
      );
    }
  }

  Future<void> requestOtp(String phoneNumber) async {
    final l10n = AppStrings(_ref.read(appLocaleProvider));
    state = state.copyWith(
      isLoading: true,
      phoneNumber: phoneNumber,
      clearError: true,
      clearStatus: true,
    );
    try {
      final result = await _ref
          .read(apiServiceProvider)
          .requestOtp(phoneNumber);
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        isOtpRequested: true,
        phoneNumber: phoneNumber,
        statusMessage: result.message,
        clearError: true,
      );
    } catch (error) {
      final message = commerceErrorMessage(error);
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        errorMessage: message == 'offline'
            ? l10n.text('commerce_offline')
            : message,
        clearStatus: true,
      );
    }
  }

  Future<void> verifyOtp(String otp) async {
    final l10n = AppStrings(_ref.read(appLocaleProvider));
    state = state.copyWith(
      isLoading: true,
      clearError: true,
      clearStatus: true,
    );
    try {
      var session = await _ref
          .read(apiServiceProvider)
          .verifyOtp(phoneNumber: state.phoneNumber, otp: otp);
      final user = await _ref
          .read(apiServiceProvider)
          .getCurrentCommerceUser(session.accessToken);
      session = session.withUser(user);
      await _saveTokens(session);
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        isAuthenticated: true,
        isOtpRequested: false,
        session: session,
        phoneNumber: user.phone,
        displayName: user.displayName ?? _displayName(user.phone),
        statusMessage: l10n.text('signed_in_successfully'),
        clearError: true,
      );
    } catch (error) {
      final message = commerceErrorMessage(error);
      state = state.copyWith(
        isInitialized: true,
        isLoading: false,
        errorMessage: message == 'offline'
            ? l10n.text('commerce_offline')
            : message,
        clearStatus: true,
      );
    }
  }

  Future<void> logout() async {
    final refresh = state.session?.refreshToken;
    if (refresh != null && refresh.isNotEmpty) {
      try {
        await _ref.read(apiServiceProvider).logoutCommerce(refresh);
      } catch (_) {}
    }
    await _clearTokens();
    state = AuthState.initial().copyWith(isInitialized: true);
  }

  Future<void> _saveTokens(AuthSession session) async {
    final storage = _ref.read(secureStorageProvider);
    await storage.write(accessKey, session.accessToken);
    await storage.write(refreshKey, session.refreshToken);
  }

  Future<void> _clearTokens() async {
    final storage = _ref.read(secureStorageProvider);
    await storage.delete(accessKey);
    await storage.delete(refreshKey);
  }

  String _displayName(String phone) =>
      'User ${phone.length >= 4 ? phone.substring(phone.length - 4) : phone}';
}

final authControllerProvider = StateNotifierProvider<AuthController, AuthState>(
  (ref) => AuthController(ref),
);
