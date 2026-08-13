import 'package:flutter/material.dart';

import '../localization/app_strings.dart';
import '../providers/commerce_provider.dart';
import '../theme/app_theme.dart';

class CommerceStatePanel extends StatelessWidget {
  const CommerceStatePanel({
    super.key,
    required this.status,
    required this.onRetry,
    this.message,
  });
  final LoadStatus status;
  final VoidCallback onRetry;
  final String? message;
  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    if (status == LoadStatus.loading || status == LoadStatus.initial) {
      return const Center(child: CircularProgressIndicator());
    }
    final offline = status == LoadStatus.offline;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(28),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              offline ? Icons.cloud_off_outlined : Icons.error_outline,
              size: 48,
              color: AppTheme.lightText,
            ),
            const SizedBox(height: 12),
            Text(
              l10n.text(offline ? 'commerce_offline' : 'commerce_error'),
              textAlign: TextAlign.center,
              style: const TextStyle(fontWeight: FontWeight.w700),
            ),
            if (message != null && message != 'offline') ...[
              const SizedBox(height: 6),
              Text(
                message!,
                textAlign: TextAlign.center,
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(color: AppTheme.lightText),
              ),
            ],
            const SizedBox(height: 16),
            OutlinedButton.icon(
              onPressed: onRetry,
              icon: const Icon(Icons.refresh),
              label: Text(l10n.text('retry')),
            ),
          ],
        ),
      ),
    );
  }
}
