import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../widgets/intelligence_card.dart';
import '../widgets/quick_stats.dart';
import 'price_insight_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  static const List<String> _roles = ['Farmer', 'Trader', 'Exporter'];
  String _selectedRole = 'Farmer';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        titleSpacing: 12,
        title: const Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('🌾', style: TextStyle(fontSize: 28)),
            SizedBox(width: 10),
            Flexible(
              child: Text(
                'CropPulse',
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
        actions: [
          Padding(
            padding: const EdgeInsets.only(right: 12),
            child: PopupMenuButton<String>(
              padding: EdgeInsets.zero,
              tooltip: 'Select role',
              initialValue: _selectedRole,
              itemBuilder: (context) => [
                for (final role in _roles)
                  PopupMenuItem<String>(
                    value: role,
                    child: Row(
                      children: [
                        Expanded(child: Text(role)),
                        if (role == _selectedRole)
                          const Icon(
                            Icons.check,
                            size: 18,
                            color: AppTheme.primaryGreen,
                          ),
                      ],
                    ),
                  ),
              ],
              onSelected: (role) {
                setState(() {
                  _selectedRole = role;
                });
              },
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
                decoration: BoxDecoration(
                  border: Border.all(color: AppTheme.primaryGreen),
                  borderRadius: BorderRadius.circular(10),
                  color: Colors.white,
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.person, size: 16, color: AppTheme.primaryGreen),
                    const SizedBox(width: 6),
                    Text(
                      _selectedRole,
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: AppTheme.primaryGreen,
                      ),
                    ),
                    const SizedBox(width: 4),
                    const Icon(Icons.keyboard_arrow_down, size: 16, color: AppTheme.primaryGreen),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header
            Center(
              child: Column(
                children: [
                  const Text('📈 Daily Intelligence Feed',
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  Text('Real-time market alerts & AI recommendations',
                      style: TextStyle(fontSize: 14, color: AppTheme.lightText)),
                ],
              ),
            ),
            const SizedBox(height: 24),

            // Intelligence Alerts
            const IntelligenceAlerts(),
            const SizedBox(height: 24),

            // Quick Stats
            const QuickStats(),
            const SizedBox(height: 24),

            Container(
              padding: const EdgeInsets.all(18),
              decoration: BoxDecoration(
                gradient: AppTheme.primaryGradient,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Need a selling recommendation?',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w700,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Open the price advisor to fetch live market guidance from the Phase 2 API or use offline fallback data.',
                    style: TextStyle(color: Colors.white, height: 1.4),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.white,
                      foregroundColor: AppTheme.primaryGreen,
                    ),
                    onPressed: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (_) => const PriceInsightScreen(),
                        ),
                      );
                    },
                    child: const Text('Open Price Advisor'),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class IntelligenceAlerts extends StatelessWidget {
  const IntelligenceAlerts({super.key});

  @override
  Widget build(BuildContext context) {
    final alerts = [
      {
        'emoji': '📈',
        'title': 'Rice prices rising (8.5%)',
        'subtitle': 'Peak demand expected in next 48 hours',
        'action': '🎯 Best selling window opening',
        'severity': 'high',
      },
      {
        'emoji': '🔥',
        'title': 'Peak demand conditions',
        'subtitle': 'Demand at 92% - Maximum buyer interest',
        'action': '💰 Optimal selling window',
        'severity': 'high',
      },
      {
        'emoji': '⛈️',
        'title': 'Heavy rainfall expected',
        'subtitle': 'May reduce supply in next 2-3 weeks',
        'action': '📊 Monitor supply closely',
        'severity': 'medium',
      },
      {
        'emoji': '⏰',
        'title': 'Best time to sell: Next 48 hours',
        'subtitle': 'Price forecast: ₹2,650/kg (peak demand)',
        'action': '🎯 Recommend selling now',
        'severity': 'high',
      },
    ];

    return Column(
      children: alerts.map((alert) {
        return IntelligenceCard(
          emoji: alert['emoji'] as String,
          title: alert['title'] as String,
          subtitle: alert['subtitle'] as String,
          action: alert['action'] as String,
          severity: alert['severity'] as String,
        );
      }).toList(),
    );
  }
}
