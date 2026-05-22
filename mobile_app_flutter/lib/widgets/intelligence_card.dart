import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class IntelligenceCard extends StatelessWidget {
  final String emoji;
  final String title;
  final String subtitle;
  final String action;
  final String severity;

  const IntelligenceCard({
    super.key,
    required this.emoji,
    required this.title,
    required this.subtitle,
    required this.action,
    required this.severity,
  });

  @override
  Widget build(BuildContext context) {
    final borderColor = severity == 'high'
        ? AppTheme.errorRed
        : AppTheme.warningOrange;

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        border: Border(left: BorderSide(color: borderColor, width: 5)),
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.05),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Text(emoji, style: const TextStyle(fontSize: 24)),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  title,
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            subtitle,
            style: const TextStyle(fontSize: 13, color: AppTheme.lightText),
          ),
          const SizedBox(height: 12),
          Text(
            action,
            style: const TextStyle(
              fontSize: 13,
              fontWeight: FontWeight.w600,
              color: AppTheme.primaryGreen,
            ),
          ),
        ],
      ),
    );
  }
}
