import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../localization/app_strings.dart';
import '../providers/auth_provider.dart';
import '../providers/farmer_profile_provider.dart';
import '../theme/app_theme.dart';
import 'farmer_profile_screen.dart';
import 'login_screen.dart';

class ProfileScreen extends ConsumerWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final l10n = AppStrings.of(context);
    final authState = ref.watch(authControllerProvider);
    final farmerProfileState = ref.watch(farmerProfileControllerProvider);
    final farmerProfile = farmerProfileState.profile;

    return Scaffold(
      appBar: AppBar(
        title: Text('👤 ${l10n.text('profile_title')}'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Profile Header
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: AppTheme.lightGray),
              ),
              child: Column(
                children: [
                  Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      color: AppTheme.primaryGreen.withValues(alpha: 0.2),
                      borderRadius: BorderRadius.circular(40),
                    ),
                    child: const Icon(Icons.person, size: 48, color: AppTheme.primaryGreen),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    authState.displayName,
                    style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    authState.isAuthenticated ? authState.phoneNumber : l10n.text('guest_user'),
                    style: TextStyle(fontSize: 14, color: AppTheme.lightText),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _buildStat(
                        farmerProfile?.landSizeAcres.toStringAsFixed(1) ?? '--',
                        l10n.text('acres'),
                      ),
                      _buildStat(farmerProfile?.kycStatus ?? 'pending', 'KYC'),
                      _buildStat(farmerProfile == null ? 'No' : 'Yes', l10n.text('profile')),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 24),

            if (farmerProfile != null)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                margin: const EdgeInsets.only(bottom: 16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: AppTheme.lightGray),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      l10n.text('synced_farmer_profile'),
                      style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                    const SizedBox(height: 8),
                    Text('${farmerProfile.village}, ${farmerProfile.district}, ${farmerProfile.state}'),
                    Text(l10n.text('soil', params: {'value': farmerProfile.soilType})),
                    if (farmerProfileState.statusMessage != null)
                      Padding(
                        padding: const EdgeInsets.only(top: 8),
                        child: Text(
                          farmerProfileState.statusMessage!,
                          style: const TextStyle(color: AppTheme.successGreen),
                        ),
                      ),
                  ],
                ),
              ),

            // Menu Items
            _buildMenuItem(Icons.edit, l10n.text('edit_farmer_profile'), () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => const FarmerProfileScreen(),
                ),
              );
            }),
            _buildMenuItem(
              authState.isAuthenticated ? Icons.logout : Icons.login,
              authState.isAuthenticated ? l10n.text('logout') : l10n.text('login'),
              () {
                if (authState.isAuthenticated) {
                  ref.read(authControllerProvider.notifier).logout();
                  return;
                }
                Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => const LoginScreen(),
                  ),
                );
              },
            ),
            _buildMenuItem(Icons.history, l10n.text('transaction_history'), () {}),
            _buildMenuItem(Icons.favorite_border, l10n.text('saved_listings'), () {}),
            _buildMenuItem(Icons.settings, l10n.text('settings'), () {}),
            _buildMenuItem(Icons.help_outline, l10n.text('help_support'), () {}),
            _buildMenuItem(Icons.lock_outline, l10n.text('account_sync_later'), () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text(l10n.text('account_sync_message')),
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildStat(String value, String label) {
    return Column(
      children: [
        Text(value, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        Text(label, style: TextStyle(fontSize: 12, color: AppTheme.lightText)),
      ],
    );
  }

  Widget _buildMenuItem(IconData icon, String title, VoidCallback onTap) {
    return Container(
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: Icon(icon, color: AppTheme.primaryGreen),
        title: Text(title),
        trailing: const Icon(Icons.chevron_right),
        onTap: onTap,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
      ),
    );
  }
}
