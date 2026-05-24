import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';

import '../localization/app_strings.dart';
import '../models/farmer_profile.dart';
import '../providers/farmer_profile_provider.dart';
import '../theme/app_theme.dart';

class FarmerProfileScreen extends ConsumerStatefulWidget {
  const FarmerProfileScreen({super.key});

  @override
  ConsumerState<FarmerProfileScreen> createState() => _FarmerProfileScreenState();
}

class _FarmerProfileScreenState extends ConsumerState<FarmerProfileScreen> {
  final _nameController = TextEditingController();
  final _stateController = TextEditingController(text: 'Tamil Nadu');
  final _districtController = TextEditingController(text: 'Tiruppur');
  final _villageController = TextEditingController(text: 'Sample Village');
  final _landSizeController = TextEditingController(text: '2.5');
  final _soilTypeController = TextEditingController(text: 'Loamy');
  final _latitudeController = TextEditingController(text: '11.4064');
  final _longitudeController = TextEditingController(text: '77.3506');
  final _bankAccountController = TextEditingController();

  @override
  void initState() {
    super.initState();
    Future.microtask(() => ref.read(farmerProfileControllerProvider.notifier).loadProfile());
  }

  @override
  void dispose() {
    _nameController.dispose();
    _stateController.dispose();
    _districtController.dispose();
    _villageController.dispose();
    _landSizeController.dispose();
    _soilTypeController.dispose();
    _latitudeController.dispose();
    _longitudeController.dispose();
    _bankAccountController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final profileState = ref.watch(farmerProfileControllerProvider);
    final profile = profileState.profile;

    if (profile != null) {
      _hydrateForm(profile);
    }

    return Scaffold(
      appBar: AppBar(title: Text(l10n.text('farmer_profile_title'))),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (profileState.errorMessage != null) ...[
              _Banner(message: profileState.errorMessage!, color: AppTheme.errorRed),
              const SizedBox(height: 12),
            ],
            if (profileState.statusMessage != null) ...[
              _Banner(message: profileState.statusMessage!, color: AppTheme.successGreen),
              const SizedBox(height: 12),
            ],
            if (profile != null) ...[
              _ProfileSummary(profile: profile),
              const SizedBox(height: 20),
            ],
            _ProfileForm(
              nameController: _nameController,
              stateController: _stateController,
              districtController: _districtController,
              villageController: _villageController,
              landSizeController: _landSizeController,
              soilTypeController: _soilTypeController,
              latitudeController: _latitudeController,
              longitudeController: _longitudeController,
              bankAccountController: _bankAccountController,
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: profileState.isLoading
                        ? null
                        : () => ref.read(farmerProfileControllerProvider.notifier).loadProfile(),
                    child: Text(l10n.text('sync_profile')),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: ElevatedButton(
                    onPressed: profileState.isSaving ? null : _saveProfile,
                    child: Text(profileState.isSaving ? l10n.text('saving') : l10n.text('save_profile')),
                  ),
                ),
              ],
            ),
            if (profileState.isLoading) ...[
              const SizedBox(height: 16),
              const Center(child: CircularProgressIndicator()),
            ],
          ],
        ),
      ),
    );
  }

  void _hydrateForm(FarmerProfile profile) {
    _nameController.text = profile.name;
    _stateController.text = profile.state;
    _districtController.text = profile.district;
    _villageController.text = profile.village;
    _landSizeController.text = profile.landSizeAcres.toString();
    _soilTypeController.text = profile.soilType;
    _latitudeController.text = profile.latitude.toString();
    _longitudeController.text = profile.longitude.toString();
    _bankAccountController.text = profile.bankAccount ?? '';
  }

  void _saveProfile() {
    final l10n = AppStrings.of(context);
    final landSize = double.tryParse(_landSizeController.text.trim());
    final latitude = double.tryParse(_latitudeController.text.trim());
    final longitude = double.tryParse(_longitudeController.text.trim());

    if (_nameController.text.trim().isEmpty ||
        _stateController.text.trim().isEmpty ||
        _districtController.text.trim().isEmpty ||
        _villageController.text.trim().isEmpty ||
        _soilTypeController.text.trim().isEmpty ||
        landSize == null ||
        latitude == null ||
        longitude == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(l10n.text('fill_required_fields'))),
      );
      return;
    }

    final request = FarmerProfileRequest(
      name: _nameController.text.trim(),
      state: _stateController.text.trim(),
      district: _districtController.text.trim(),
      village: _villageController.text.trim(),
      landSizeAcres: landSize,
      soilType: _soilTypeController.text.trim(),
      latitude: latitude,
      longitude: longitude,
      bankAccount: _bankAccountController.text.trim().isEmpty
          ? null
          : _bankAccountController.text.trim(),
    );

    ref.read(farmerProfileControllerProvider.notifier).saveProfile(request);
  }
}

class _ProfileSummary extends StatelessWidget {
  const _ProfileSummary({required this.profile});

  final FarmerProfile profile;

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    final createdAt = DateFormat('dd MMM yyyy').format(profile.createdAt);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.lightGray),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(l10n.text('backend_profile_snapshot'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 12),
          Text('${l10n.text('name')}: ${profile.name}'),
          Text('${l10n.text('phone')}: ${profile.phone}'),
          Text('${l10n.text('kyc')}: ${profile.kycStatus}'),
          Text(l10n.text('land_size', params: {'value': profile.landSizeAcres.toString()})),
          Text('${l10n.text('village')}: ${profile.village}, ${profile.district}, ${profile.state}'),
          Text(l10n.text('created', params: {'value': createdAt})),
        ],
      ),
    );
  }
}

class _ProfileForm extends StatelessWidget {
  const _ProfileForm({
    required this.nameController,
    required this.stateController,
    required this.districtController,
    required this.villageController,
    required this.landSizeController,
    required this.soilTypeController,
    required this.latitudeController,
    required this.longitudeController,
    required this.bankAccountController,
  });

  final TextEditingController nameController;
  final TextEditingController stateController;
  final TextEditingController districtController;
  final TextEditingController villageController;
  final TextEditingController landSizeController;
  final TextEditingController soilTypeController;
  final TextEditingController latitudeController;
  final TextEditingController longitudeController;
  final TextEditingController bankAccountController;

  @override
  Widget build(BuildContext context) {
    final l10n = AppStrings.of(context);
    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppTheme.lightGray),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(l10n.text('farmer_profile_form'), style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 16),
          TextField(controller: nameController, decoration: InputDecoration(labelText: l10n.text('name'))),
          const SizedBox(height: 12),
          TextField(controller: stateController, decoration: InputDecoration(labelText: l10n.text('state'))),
          const SizedBox(height: 12),
          TextField(controller: districtController, decoration: InputDecoration(labelText: l10n.text('district'))),
          const SizedBox(height: 12),
          TextField(controller: villageController, decoration: InputDecoration(labelText: l10n.text('village'))),
          const SizedBox(height: 12),
          TextField(
            controller: landSizeController,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: InputDecoration(labelText: l10n.text('land_size_acres')),
          ),
          const SizedBox(height: 12),
          TextField(controller: soilTypeController, decoration: InputDecoration(labelText: l10n.text('soil_type'))),
          const SizedBox(height: 12),
          TextField(
            controller: latitudeController,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: InputDecoration(labelText: l10n.text('latitude')),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: longitudeController,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: InputDecoration(labelText: l10n.text('longitude')),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: bankAccountController,
            decoration: InputDecoration(labelText: l10n.text('bank_account_optional')),
          ),
        ],
      ),
    );
  }
}

class _Banner extends StatelessWidget {
  const _Banner({required this.message, required this.color});

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
      child: Text(message, style: TextStyle(color: color, fontWeight: FontWeight.w600)),
    );
  }
}