class AuthSession {
  const AuthSession({
    required this.accessToken,
    this.refreshToken = '',
    required this.tokenType,
    this.accessExpiresInSeconds = 0,
    this.refreshExpiresInSeconds = 0,
    this.userId = '',
    this.phone = '',
    this.displayName,
  });

  final String accessToken;
  final String refreshToken;
  final String tokenType;
  final int accessExpiresInSeconds;
  final int refreshExpiresInSeconds;
  final String userId;
  final String phone;
  final String? displayName;

  factory AuthSession.fromJson(Map<String, dynamic> json) => AuthSession(
    accessToken: json['access_token'] as String? ?? '',
    refreshToken: json['refresh_token'] as String? ?? '',
    tokenType: json['token_type'] as String? ?? 'bearer',
    accessExpiresInSeconds:
        (json['access_expires_in_seconds'] as num?)?.toInt() ?? 0,
    refreshExpiresInSeconds:
        (json['refresh_expires_in_seconds'] as num?)?.toInt() ?? 0,
  );

  AuthSession withUser(CurrentCommerceUser user) => AuthSession(
    accessToken: accessToken,
    refreshToken: refreshToken,
    tokenType: tokenType,
    accessExpiresInSeconds: accessExpiresInSeconds,
    refreshExpiresInSeconds: refreshExpiresInSeconds,
    userId: user.id,
    phone: user.phone,
    displayName: user.displayName,
  );
}

class CurrentCommerceUser {
  const CurrentCommerceUser({
    required this.id,
    required this.phone,
    required this.preferredLocale,
    this.displayName,
  });

  final String id;
  final String phone;
  final String preferredLocale;
  final String? displayName;

  factory CurrentCommerceUser.fromJson(Map<String, dynamic> json) =>
      CurrentCommerceUser(
        id: json['id'] as String? ?? '',
        phone: json['phone_e164'] as String? ?? '',
        preferredLocale: json['preferred_locale'] as String? ?? 'en',
        displayName: json['display_name'] as String?,
      );
}

class OtpRequestResult {
  const OtpRequestResult({
    this.challengeId = '',
    required this.phone,
    required this.message,
    required this.expiresInSeconds,
    this.resendAfterSeconds = 0,
  });

  final String challengeId;
  final String phone;
  final String message;
  final int expiresInSeconds;
  final int resendAfterSeconds;

  factory OtpRequestResult.fromJson(Map<String, dynamic> json) =>
      OtpRequestResult(
        challengeId: json['challenge_id'] as String? ?? '',
        phone: json['phone'] as String? ?? '',
        message: json['message'] as String? ?? '',
        expiresInSeconds: (json['expires_in_seconds'] as num?)?.toInt() ?? 0,
        resendAfterSeconds:
            (json['resend_after_seconds'] as num?)?.toInt() ?? 0,
      );
}
