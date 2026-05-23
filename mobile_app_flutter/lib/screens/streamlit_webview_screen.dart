import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

import '../theme/app_theme.dart';

class StreamlitWebViewScreen extends StatefulWidget {
  const StreamlitWebViewScreen({super.key, required this.url});

  final String url;

  @override
  State<StreamlitWebViewScreen> createState() => _StreamlitWebViewScreenState();
}

class _StreamlitWebViewScreenState extends State<StreamlitWebViewScreen> {
  bool _isLaunching = true;
  bool _launchFailed = false;

  @override
  void initState() {
    super.initState();
    _launchExternalBrowser();
  }

  Future<void> _launchExternalBrowser() async {
    final uri = Uri.parse(widget.url);
    final didLaunch = await launchUrl(
      uri,
      mode: LaunchMode.externalApplication,
    );

    if (!mounted) {
      return;
    }

    setState(() {
      _isLaunching = false;
      _launchFailed = !didLaunch;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('CropPulse Web App'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 420),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  _launchFailed ? Icons.error_outline : Icons.open_in_browser,
                  size: 56,
                  color: _launchFailed ? AppTheme.errorRed : AppTheme.primaryGreen,
                ),
                const SizedBox(height: 20),
                Text(
                  _launchFailed
                      ? 'Could not open the browser automatically.'
                      : 'Opening CropPulse in your browser...',
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 12),
                Text(
                  _launchFailed
                      ? 'Tap the button below to open the live Streamlit app in your browser.'
                      : 'If nothing happens, tap the button below to open the live Streamlit app outside the mobile shell.',
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: AppTheme.lightText, height: 1.5),
                ),
                const SizedBox(height: 24),
                if (_isLaunching) const CircularProgressIndicator(),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: _launchExternalBrowser,
                    icon: const Icon(Icons.open_in_new),
                    label: const Text('Open in Browser'),
                  ),
                ),
                const SizedBox(height: 12),
                SelectableText(
                  widget.url,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: AppTheme.lightText),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}