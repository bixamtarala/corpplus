import 'package:dio/dio.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/app_update_info.dart';

class AppUpdateService {
  AppUpdateService({Dio? dio, String? metadataUrl, String? fallbackPlayStoreUrl})
      : _dio = dio ??
            Dio(
              BaseOptions(
                connectTimeout: const Duration(seconds: 8),
                receiveTimeout: const Duration(seconds: 8),
              ),
            ),
        metadataUrl = metadataUrl ??
            const String.fromEnvironment(
              'CROPPULSE_UPDATE_METADATA_URL',
              defaultValue:
                  'https://github.com/bixamtarala/corpplus/releases/download/mobile-latest/update-metadata.json',
            ),
        fallbackPlayStoreUrl = fallbackPlayStoreUrl ??
            const String.fromEnvironment(
              'CROPPULSE_PLAY_STORE_URL',
              defaultValue: 'https://play.google.com/store/apps/details?id=com.croppulse.mobile',
            );

  static const String _dismissedVersionKey = 'dismissed_update_version_code';

  final Dio _dio;
  final String metadataUrl;
  final String fallbackPlayStoreUrl;

  Future<AppUpdateInfo?> getAvailableUpdate() async {
    final latestUpdate = await fetchLatestUpdate();
    if (latestUpdate == null) {
      return null;
    }

    final packageInfo = await PackageInfo.fromPlatform();
    final currentVersionCode = int.tryParse(packageInfo.buildNumber) ?? 0;

    if (latestUpdate.versionCode <= currentVersionCode) {
      return null;
    }

    return latestUpdate;
  }

  Future<AppUpdateInfo?> fetchLatestUpdate() async {
    try {
      final response = await _dio.get<Map<String, dynamic>>(metadataUrl);
      final data = response.data;
      if (data == null) {
        return null;
      }

      final update = AppUpdateInfo.fromJson(data);
      if (update.playStoreUrl == null || update.playStoreUrl!.isEmpty) {
        return update.copyWith(playStoreUrl: fallbackPlayStoreUrl);
      }

      return update;
    } on DioException {
      return null;
    } on FormatException {
      return null;
    }
  }

  Future<bool> shouldPromptForVersion(int versionCode) async {
    final preferences = await SharedPreferences.getInstance();
    final dismissedVersion = preferences.getInt(_dismissedVersionKey);
    return dismissedVersion != versionCode;
  }

  Future<void> dismissVersion(int versionCode) async {
    final preferences = await SharedPreferences.getInstance();
    await preferences.setInt(_dismissedVersionKey, versionCode);
  }
}