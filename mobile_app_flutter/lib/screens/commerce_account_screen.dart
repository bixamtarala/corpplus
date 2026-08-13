import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import 'farmer_hub_screen.dart';
import 'intelligence_screen.dart';
import 'marketplace_screen.dart';
import 'profile_screen.dart';
import 'trader_hub_screen.dart';

class CommerceAccountScreen extends StatelessWidget {
  const CommerceAccountScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Account')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppTheme.primaryGreen.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Icon(
                  Icons.account_circle_outlined,
                  color: AppTheme.primaryGreen,
                  size: 36,
                ),
                SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Personal workspace',
                        style: TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      SizedBox(height: 4),
                      Text(
                        'Guest browsing is active. Sign-in remains available in Profile while production OTP is prepared.',
                        style: TextStyle(
                          color: AppTheme.lightText,
                          height: 1.35,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 18),
          const Text(
            'Account and tools',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.w800),
          ),
          const SizedBox(height: 8),
          _AccountTile(
            icon: Icons.person_outline,
            title: 'Profile and sign in',
            subtitle: 'Authentication and farmer profile controls',
            destination: const ProfileScreen(),
          ),
          _AccountTile(
            icon: Icons.grass_outlined,
            title: 'Farmer workspace',
            subtitle:
                'Existing farmer tools retained during commerce migration',
            destination: const FarmerHubScreen(),
          ),
          _AccountTile(
            icon: Icons.storefront_outlined,
            title: 'Trader workspace',
            subtitle: 'Existing procurement and marketplace tools',
            destination: const TraderHubScreen(),
          ),
          _AccountTile(
            icon: Icons.insights_outlined,
            title: 'Market intelligence',
            subtitle: 'Price and supply tools with visible fallback states',
            destination: const IntelligenceScreen(),
          ),
          _AccountTile(
            icon: Icons.swap_horiz,
            title: 'Legacy trading marketplace',
            subtitle:
                'Offer and listing prototype retained for supplier testing',
            destination: const MarketplaceScreen(),
          ),
          const SizedBox(height: 18),
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: AppTheme.primaryBlue.withValues(alpha: 0.08),
              borderRadius: BorderRadius.circular(14),
            ),
            child: const Text(
              'Business verification, orders, addresses, support cases, and supplier settlement will activate in later implementation slices.',
              style: TextStyle(height: 1.4),
            ),
          ),
        ],
      ),
    );
  }
}

class _AccountTile extends StatelessWidget {
  const _AccountTile({
    required this.icon,
    required this.title,
    required this.subtitle,
    required this.destination,
  });

  final IconData icon;
  final String title;
  final String subtitle;
  final Widget destination;

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      margin: const EdgeInsets.only(bottom: 8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(14),
        side: const BorderSide(color: AppTheme.lightGray),
      ),
      child: ListTile(
        leading: Icon(icon, color: AppTheme.primaryGreen),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.w700)),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.chevron_right),
        onTap: () => Navigator.of(
          context,
        ).push(MaterialPageRoute(builder: (_) => destination)),
      ),
    );
  }
}
