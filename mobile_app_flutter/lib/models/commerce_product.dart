class CommerceProduct {
  const CommerceProduct({
    required this.id,
    required this.name,
    required this.category,
    required this.packLabel,
    required this.previewPricePaise,
    required this.grade,
    required this.origin,
    required this.description,
    this.localizedNames = const {},
    this.isFresh = false,
  });

  final String id;
  final String name;
  final Map<String, String> localizedNames;
  final String category;
  final String packLabel;
  final int previewPricePaise;
  final String grade;
  final String origin;
  final String description;
  final bool isFresh;

  String displayName(String languageCode) =>
      localizedNames[languageCode] ?? name;

  String get formattedPreviewPrice {
    final rupees = previewPricePaise ~/ 100;
    final paise = previewPricePaise % 100;
    return paise == 0
        ? 'Rs $rupees'
        : 'Rs $rupees.${paise.toString().padLeft(2, '0')}';
  }
}

class CommerceCategory {
  const CommerceCategory({
    required this.id,
    required this.label,
    required this.iconName,
  });

  final String id;
  final String label;
  final String iconName;
}
