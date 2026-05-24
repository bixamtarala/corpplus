class AppUpdateInfo {
  const AppUpdateInfo({
    required this.versionName,
    required this.versionCode,
    required this.downloadUrl,
    this.playStoreUrl,
    this.releaseNotes,
    this.publishedAt,
    this.forceUpdate = false,
  });

  final String versionName;
  final int versionCode;
  final String downloadUrl;
  final String? playStoreUrl;
  final String? releaseNotes;
  final String? publishedAt;
  final bool forceUpdate;

  AppUpdateInfo copyWith({
    String? versionName,
    int? versionCode,
    String? downloadUrl,
    String? playStoreUrl,
    String? releaseNotes,
    String? publishedAt,
    bool? forceUpdate,
  }) {
    return AppUpdateInfo(
      versionName: versionName ?? this.versionName,
      versionCode: versionCode ?? this.versionCode,
      downloadUrl: downloadUrl ?? this.downloadUrl,
      playStoreUrl: playStoreUrl ?? this.playStoreUrl,
      releaseNotes: releaseNotes ?? this.releaseNotes,
      publishedAt: publishedAt ?? this.publishedAt,
      forceUpdate: forceUpdate ?? this.forceUpdate,
    );
  }

  factory AppUpdateInfo.fromJson(Map<String, dynamic> json) {
    final rawVersionCode =
        json['version_code'] ?? json['versionCode'] ?? json['build_number'] ?? json['buildNumber'];
    final rawVersionName = json['version_name'] ?? json['versionName'];
    final rawDownloadUrl = json['download_url'] ?? json['downloadUrl'];

    final versionCode = rawVersionCode is num
        ? rawVersionCode.toInt()
        : int.tryParse(rawVersionCode?.toString() ?? '');
    final versionName = rawVersionName?.toString();
    final downloadUrl = rawDownloadUrl?.toString();

    if (versionCode == null || versionName == null || downloadUrl == null) {
      throw const FormatException('Update metadata is missing version or download fields.');
    }

    return AppUpdateInfo(
      versionName: versionName,
      versionCode: versionCode,
      downloadUrl: downloadUrl,
      playStoreUrl: (json['play_store_url'] ?? json['playStoreUrl'])?.toString(),
      releaseNotes: (json['release_notes'] ?? json['releaseNotes'])?.toString(),
      publishedAt: (json['published_at'] ?? json['publishedAt'])?.toString(),
      forceUpdate: (json['force_update'] ?? json['forceUpdate']) == true,
    );
  }
}