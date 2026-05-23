class CommodityGroup {
  const CommodityGroup({
    required this.category,
    required this.states,
    required this.commodities,
  });

  final String category;
  final List<String> states;
  final List<String> commodities;
}

class CommodityEntry {
  const CommodityEntry({
    required this.name,
    required this.category,
    required this.states,
  });

  final String name;
  final String category;
  final List<String> states;
}

class CommodityCatalog {
  static const List<CommodityGroup> groups = [
    CommodityGroup(
      category: 'Cereals & Millets',
      states: [
        'Punjab',
        'Haryana',
        'Uttar Pradesh',
        'Madhya Pradesh',
        'Rajasthan',
        'Bihar',
        'Karnataka',
        'Tamil Nadu',
      ],
      commodities: [
        'Paddy',
        'Rice',
        'Wheat',
        'Maize',
        'Jowar',
        'Bajra',
        'Ragi',
        'Barley',
        'Foxtail Millet',
        'Little Millet',
        'Barnyard Millet',
        'Kodo Millet',
        'Proso Millet',
      ],
    ),
    CommodityGroup(
      category: 'Pulses',
      states: [
        'Madhya Pradesh',
        'Maharashtra',
        'Rajasthan',
        'Uttar Pradesh',
        'Karnataka',
        'Telangana',
      ],
      commodities: [
        'Tur (Arhar)',
        'Gram (Chana)',
        'Moong',
        'Urad',
        'Masoor',
        'Field Pea',
        'Rajma',
        'Lobia (Cowpea)',
        'Horse Gram',
        'Moth Bean',
      ],
    ),
    CommodityGroup(
      category: 'Oilseeds',
      states: [
        'Gujarat',
        'Madhya Pradesh',
        'Rajasthan',
        'Maharashtra',
        'Karnataka',
        'Telangana',
      ],
      commodities: [
        'Groundnut',
        'Soybean',
        'Mustard',
        'Sunflower',
        'Sesame',
        'Castor',
        'Linseed',
        'Safflower',
        'Niger Seed',
        'Rapeseed',
      ],
    ),
    CommodityGroup(
      category: 'Vegetables',
      states: [
        'Uttar Pradesh',
        'West Bengal',
        'Maharashtra',
        'Karnataka',
        'Tamil Nadu',
        'Bihar',
      ],
      commodities: [
        'Potato',
        'Onion',
        'Tomato',
        'Brinjal',
        'Okra',
        'Cabbage',
        'Cauliflower',
        'Carrot',
        'Radish',
        'Beetroot',
        'Bottle Gourd',
        'Bitter Gourd',
        'Ridge Gourd',
        'Pumpkin',
        'Cucumber',
        'Capsicum',
        'Green Peas',
        'Beans',
        'Drumstick',
        'Spinach',
        'Green Chilli',
        'Garlic',
        'Ginger',
      ],
    ),
    CommodityGroup(
      category: 'Fruits & Plantation',
      states: [
        'Maharashtra',
        'Andhra Pradesh',
        'Tamil Nadu',
        'Karnataka',
        'Kerala',
        'Gujarat',
        'Himachal Pradesh',
      ],
      commodities: [
        'Banana',
        'Mango',
        'Coconut',
        'Apple',
        'Orange',
        'Grapes',
        'Guava',
        'Papaya',
        'Pomegranate',
        'Pineapple',
        'Lemon',
        'Arecanut',
        'Cashew',
        'Tea',
        'Coffee',
        'Rubber',
      ],
    ),
    CommodityGroup(
      category: 'Spices & Commercial Crops',
      states: [
        'Gujarat',
        'Rajasthan',
        'Madhya Pradesh',
        'Maharashtra',
        'Karnataka',
        'Kerala',
        'West Bengal',
        'Assam',
      ],
      commodities: [
        'Cotton',
        'Sugarcane',
        'Jute',
        'Turmeric',
        'Coriander',
        'Cumin',
        'Black Pepper',
        'Cardamom',
        'Clove',
        'Fenugreek',
        'Fennel',
        'Ajwain',
        'Dry Chilli',
        'Tobacco',
        'Mesta',
      ],
    ),
  ];

  static final List<CommodityEntry> entries = [
    for (final group in groups)
      for (final commodity in group.commodities)
        CommodityEntry(
          name: commodity,
          category: group.category,
          states: group.states,
        ),
  ];

  static final List<String> all = [for (final entry in entries) entry.name];

  static final List<String> categories = [for (final group in groups) group.category];

  static final List<String> allStates = () {
    final seen = <String>{};
    final ordered = <String>[];
    for (final group in groups) {
      for (final state in group.states) {
        if (seen.add(state)) {
          ordered.add(state);
        }
      }
    }
    return ordered;
  }();

  static List<CommodityEntry> search({
    String query = '',
    String? category,
    String? state,
  }) {
    final normalizedQuery = query.trim().toLowerCase();

    return entries.where((entry) {
      final matchesCategory = category == null || entry.category == category;
      final matchesState = state == null || entry.states.contains(state);
      final matchesQuery = normalizedQuery.isEmpty ||
          entry.name.toLowerCase().contains(normalizedQuery) ||
          entry.category.toLowerCase().contains(normalizedQuery) ||
          entry.states.any((item) => item.toLowerCase().contains(normalizedQuery));

      return matchesCategory && matchesState && matchesQuery;
    }).toList();
  }
}