enum InsightSource {
  live,
  fallback,
}

class PriceInsightRequestPayload {
  const PriceInsightRequestPayload({
    required this.crop,
    required this.quantityKg,
    required this.state,
  });

  final String crop;
  final double quantityKg;
  final String state;

  Map<String, dynamic> toJson() {
    return {
      'crop': crop,
      'quantity_kg': quantityKg,
      'state': state,
    };
  }
}

class PriceInsight {
  const PriceInsight({
    required this.crop,
    required this.recommendedPrice,
    required this.marketTrend,
    required this.nearbyPrices,
    required this.bestSellingTime,
    required this.analysis,
    required this.source,
  });

  final String crop;
  final double recommendedPrice;
  final String marketTrend;
  final Map<String, double> nearbyPrices;
  final String bestSellingTime;
  final String analysis;
  final InsightSource source;

  factory PriceInsight.fromJson(
    Map<String, dynamic> json, {
    InsightSource source = InsightSource.live,
  }) {
    final rawPrices = (json['nearby_prices'] as Map<String, dynamic>? ?? {})
        .map((key, value) => MapEntry(key, (value as num).toDouble()));

    return PriceInsight(
      crop: (json['crop'] ?? 'Rice') as String,
      recommendedPrice: (json['recommended_price'] as num?)?.toDouble() ?? 0,
      marketTrend: (json['market_trend'] ?? 'stable') as String,
      nearbyPrices: rawPrices,
      bestSellingTime: (json['best_selling_time'] ?? 'Monitor markets daily') as String,
      analysis: (json['analysis'] ?? 'No analysis available yet.') as String,
      source: source,
    );
  }
}