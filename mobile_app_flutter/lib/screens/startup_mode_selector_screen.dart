import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../theme/app_theme.dart';

enum AppLaunchMode { nativeApp, webApp }

class StartupModeSelectorScreen extends StatefulWidget {
  const StartupModeSelectorScreen({
    super.key,
    required this.defaultMode,
    required this.nativeScreen,
    required this.webScreen,
  });

  final AppLaunchMode defaultMode;
  final Widget nativeScreen;
  final Widget webScreen;

  @override
  State<StartupModeSelectorScreen> createState() =>
      _StartupModeSelectorScreenState();
}

class _StartupModeSelectorScreenState extends State<StartupModeSelectorScreen> {
  static const _startupModePreferenceKey = 'startup_mode';

  late AppLaunchMode _savedMode;
  bool _isOpeningMode = false;

  @override
  void initState() {
    super.initState();
    _savedMode = widget.defaultMode;
    _loadSavedMode();
  }

  Future<void> _loadSavedMode() async {
    final preferences = await SharedPreferences.getInstance();
    final savedValue = preferences.getString(_startupModePreferenceKey);
    final savedMode = _deserializeMode(savedValue);

    if (!mounted || savedMode == null) {
      return;
    }

    setState(() {
      _savedMode = savedMode;
    });
  }

  Future<void> _openMode(AppLaunchMode mode) async {
    if (_isOpeningMode) {
      return;
    }

    setState(() {
      _isOpeningMode = true;
      _savedMode = mode;
    });

    final preferences = await SharedPreferences.getInstance();
    await preferences.setString(
      _startupModePreferenceKey,
      _serializeMode(mode),
    );

    if (!mounted) {
      return;
    }

    final destination = mode == AppLaunchMode.nativeApp
        ? widget.nativeScreen
        : widget.webScreen;

    await Navigator.of(context).pushReplacement(
      MaterialPageRoute<void>(builder: (_) => destination),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(gradient: AppTheme.primaryGradient),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 520),
                child: Card(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Choose how to open CropPulse',
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        const SizedBox(height: 12),
                        const Text(
                          'Open the native Flutter experience or the live Streamlit web app. Your last choice is remembered, but you can switch here every time the app starts.',
                          style: TextStyle(
                            color: AppTheme.lightText,
                            height: 1.5,
                          ),
                        ),
                        const SizedBox(height: 24),
                        _ModeOptionCard(
                          icon: Icons.phone_android,
                          title: 'Native App',
                          description:
                              'Use the Flutter mobile interface for marketplace, intelligence, profile, and preview flows.',
                          isRecommended: _savedMode == AppLaunchMode.nativeApp,
                          buttonLabel: 'Open Native App',
                          onPressed: () => _openMode(AppLaunchMode.nativeApp),
                        ),
                        const SizedBox(height: 16),
                        _ModeOptionCard(
                          icon: Icons.language,
                          title: 'Web App',
                          description:
                              'Open the live Streamlit deployment inside the app shell when you want the currently hosted production experience.',
                          isRecommended: _savedMode == AppLaunchMode.webApp,
                          buttonLabel: 'Open Web App',
                          onPressed: () => _openMode(AppLaunchMode.webApp),
                          outlined: true,
                        ),
                        const SizedBox(height: 20),
                        if (_isOpeningMode)
                          const LinearProgressIndicator(minHeight: 3),
                        const SizedBox(height: 12),
                        Text(
                          _savedMode == AppLaunchMode.nativeApp
                              ? 'Last used: Native App'
                              : 'Last used: Web App',
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: AppTheme.darkText,
                                fontWeight: FontWeight.w600,
                              ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  static String _serializeMode(AppLaunchMode mode) {
    return mode == AppLaunchMode.nativeApp ? 'native' : 'web';
  }

  static AppLaunchMode? _deserializeMode(String? value) {
    switch (value) {
      case 'native':
        return AppLaunchMode.nativeApp;
      case 'web':
        return AppLaunchMode.webApp;
      default:
        return null;
    }
  }
}

class _ModeOptionCard extends StatelessWidget {
  const _ModeOptionCard({
    required this.icon,
    required this.title,
    required this.description,
    required this.isRecommended,
    required this.buttonLabel,
    required this.onPressed,
    this.outlined = false,
  });

  final IconData icon;
  final String title;
  final String description;
  final bool isRecommended;
  final String buttonLabel;
  final VoidCallback onPressed;
  final bool outlined;

  @override
  Widget build(BuildContext context) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 180),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isRecommended ? AppTheme.primaryGreen : AppTheme.lightGray,
          width: isRecommended ? 2 : 1,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                CircleAvatar(
                  backgroundColor: AppTheme.lightGray,
                  foregroundColor: AppTheme.primaryGreen,
                  child: Icon(icon),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    title,
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                ),
                if (isRecommended)
                  const Chip(
                    label: Text('Last used'),
                    visualDensity: VisualDensity.compact,
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              description,
              style: const TextStyle(color: AppTheme.lightText, height: 1.5),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: outlined
                  ? OutlinedButton(
                      onPressed: onPressed,
                      child: Text(buttonLabel),
                    )
                  : ElevatedButton(
                      onPressed: onPressed,
                      child: Text(buttonLabel),
                    ),
            ),
          ],
        ),
      ),
    );
  }
}