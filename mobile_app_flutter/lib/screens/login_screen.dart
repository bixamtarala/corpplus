import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../providers/auth_provider.dart';
import '../theme/app_theme.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _phoneController = TextEditingController();
  final _otpController = TextEditingController();

  @override
  void dispose() {
    _phoneController.dispose();
    _otpController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final authState = ref.watch(authControllerProvider);

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: AppTheme.primaryGradient),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 420),
                child: Container(
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(24),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.12),
                        blurRadius: 24,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(l10n.text('sign_in_title'), style: const TextStyle(fontSize: 28, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 8),
                      Text(
                        l10n.text('sign_in_desc'),
                        style: TextStyle(color: AppTheme.lightText, height: 1.5),
                      ),
                      const SizedBox(height: 24),
                      TextField(
                        controller: _phoneController,
                        keyboardType: TextInputType.phone,
                        decoration: InputDecoration(
                          labelText: l10n.text('phone_number'),
                          hintText: '9876543210',
                          prefixText: '+91 ',
                        ),
                      ),
                      const SizedBox(height: 16),
                      if (authState.isOtpRequested) ...[
                        TextField(
                          controller: _otpController,
                          keyboardType: TextInputType.number,
                          decoration: InputDecoration(
                            labelText: l10n.text('otp'),
                            hintText: '123456',
                          ),
                        ),
                        const SizedBox(height: 12),
                      ],
                      if (authState.errorMessage != null) ...[
                        _MessageBanner(
                          message: authState.errorMessage!,
                          color: AppTheme.errorRed,
                        ),
                        const SizedBox(height: 12),
                      ],
                      if (authState.statusMessage != null) ...[
                        _MessageBanner(
                          message: authState.statusMessage!,
                          color: AppTheme.successGreen,
                        ),
                        const SizedBox(height: 12),
                      ],
                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton(
                          onPressed: authState.isLoading
                              ? null
                              : authState.isOtpRequested
                                  ? _onVerifyOtp
                                  : _onRequestOtp,
                          child: Text(authState.isOtpRequested ? l10n.text('verify_otp') : l10n.text('request_otp')),
                        ),
                      ),
                      if (authState.isOtpRequested) ...[
                        const SizedBox(height: 12),
                        SizedBox(
                          width: double.infinity,
                          child: OutlinedButton(
                            onPressed: authState.isLoading ? null : _onRequestOtp,
                            child: Text(l10n.text('resend_otp')),
                          ),
                        ),
                      ],
                      if (authState.isLoading) ...[
                        const SizedBox(height: 16),
                        const Center(child: CircularProgressIndicator()),
                      ],
                    ],
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  void _onRequestOtp() {
    ref.read(authControllerProvider.notifier).requestOtp(_phoneController.text.trim());
  }

  void _onVerifyOtp() {
    ref.read(authControllerProvider.notifier).verifyOtp(_otpController.text.trim());
  }
}

class _MessageBanner extends StatelessWidget {
  const _MessageBanner({required this.message, required this.color});

  final String message;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        message,
        style: TextStyle(color: color, fontWeight: FontWeight.w600),
      ),
    );
  }
}