import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/water_quality_provider.dart';
import '../theme/app_theme.dart';

class AnalysisScreen extends StatelessWidget {
  const AnalysisScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Detailed Analysis'),
        elevation: 2,
        backgroundColor: const Color(0xFF3900B3),
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
          color: Colors.white,
        ),
      ),
      body: Consumer<WaterQualityProvider>(
        builder: (context, provider, child) {
          final assessment = provider.currentAssessment;
          final parameters = provider.currentParameters;

          if (assessment == null || parameters == null) {
            return const Center(
              child: Text('No analysis data available'),
            );
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Biological Factors Card
                _buildAnalysisCard(
                  context,
                  title: 'Biological Factors',
                  icon: Icons.bug_report_outlined,
                  items: {
                    'E. coli Count': '${parameters.eColiCount} CFU/100ml',
                    'Total Coliforms': '${parameters.totalColiforms} CFU/100ml',
                    'Risk Level': _getRiskLevel(
                      assessment.contributingFactors[
                              'Biological Contamination'] ??
                          0,
                    ),
                  },
                ),
                const SizedBox(height: 16),

                // Chemical Factors Card
                _buildAnalysisCard(
                  context,
                  title: 'Chemical Parameters',
                  icon: Icons.science_outlined,
                  items: {
                    'pH Level': parameters.pH.toString(),
                    'Dissolved Oxygen': '${parameters.dissolvedOxygen} mg/L',
                    'Nitrates': '${parameters.nitrates} mg/L',
                    'Risk Level': _getRiskLevel(
                      assessment.contributingFactors['Chemical Parameters'] ??
                          0,
                    ),
                  },
                ),
                const SizedBox(height: 16),

                // Physical Factors Card
                _buildAnalysisCard(
                  context,
                  title: 'Physical Conditions',
                  icon: Icons.water_drop_outlined,
                  items: {
                    'Temperature': '${parameters.temperature}°C',
                    'Turbidity': '${parameters.turbidity} NTU',
                    'Salinity': '${parameters.salinity} mg/L',
                    'Risk Level': _getRiskLevel(
                      assessment.contributingFactors['Physical Conditions'] ??
                          0,
                    ),
                  },
                ),
                const SizedBox(height: 16),

                // Environmental Factors Card
                _buildAnalysisCard(
                  context,
                  title: 'Environmental Factors',
                  icon: Icons.eco_outlined,
                  items: {
                    'Recent Flooding': parameters.recentFlooding ? 'Yes' : 'No',
                    'Population Density':
                        '${parameters.populationDensity} per km²',
                    'Sanitation Index': parameters.sanitationIndex.toString(),
                  },
                ),
                const SizedBox(height: 24),

                // Recommendations Section
                if (assessment.recommendations.isNotEmpty) ...[
                  Text(
                    'Recommended Actions',
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                  const SizedBox(height: 16),
                  ...assessment.recommendations
                      .map((rec) => _buildRecommendationCard(
                            context,
                            recommendation: rec,
                          )),
                ],
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildAnalysisCard(
    BuildContext context, {
    required String title,
    required IconData icon,
    required Map<String, String> items,
  }) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  icon,
                  color: AppTheme.primaryAccent,
                ),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
              ],
            ),
            const SizedBox(height: 16),
            ...items.entries.map(
              (entry) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 4.0),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      entry.key,
                      style: Theme.of(context).textTheme.bodyLarge,
                    ),
                    Text(
                      entry.value,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: entry.key == 'Risk Level'
                                ? _getRiskLevelColor(entry.value)
                                : AppTheme.primaryText,
                            fontWeight: FontWeight.w600,
                          ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRecommendationCard(
    BuildContext context, {
    required String recommendation,
  }) {
    return Card(
      color: AppTheme.primaryAccent.withOpacity(0.1),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Icon(
              Icons.lightbulb_outline,
              color: AppTheme.primaryAccent,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                recommendation,
                style: Theme.of(context).textTheme.bodyLarge,
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _getRiskLevel(double risk) {
    if (risk >= 0.75) return 'Severe';
    if (risk >= 0.5) return 'High';
    if (risk >= 0.25) return 'Moderate';
    return 'Low';
  }

  Color _getRiskLevelColor(String level) {
    switch (level) {
      case 'Severe':
        return Colors.purple;
      case 'High':
        return Colors.red;
      case 'Moderate':
        return Colors.orange;
      default:
        return Colors.green;
    }
  }
}
