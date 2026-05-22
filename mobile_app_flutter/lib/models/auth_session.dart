class AuthSession {
  const AuthSession({
    required this.accessToken,
    required this.tokenType,
    required this.userId,
    required this.phone,
  });

  final String accessToken;
  final String tokenType;
  final String userId;
  final String phone;

  factory AuthSession.fromJson(Map<String, dynamic> json) {
    return AuthSession(
      accessToken: json['access_token'] as String? ?? '',
      tokenType: json['token_type'] as String? ?? 'bearer',
      userId: json['user_id'] as String? ?? '',
      phone: json['phone'] as String? ?? '',
    );
  }

  Map<String, String> toStorage() {
    return {
      'access_token': accessToken,
      'token_type': tokenType,
      'user_id': userId,
      'phone': phone,
    };
  }

  factory AuthSession.fromStorage(Map<String, Object?> storage) {
    return AuthSession(
      accessToken: storage['access_token'] as String? ?? '',
      tokenType: storage['token_type'] as String? ?? 'bearer',
      userId: storage['user_id'] as String? ?? '',
      phone: storage['phone'] as String? ?? '',
    );
  }
}

class OtpRequestResult {
  const OtpRequestResult({
    required this.phone,
    required this.message,
    required this.expiresInSeconds,
  });

  final String phone;
  final String message;
  final int expiresInSeconds;
}