import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/water_quality_provider.dart';
import '../widgets/risk_bar_chart.dart';
import '../widgets/risk_donut_chart.dart';
import '../theme/app_theme.dart';
import '../widgets/custom_app_bar.dart';

class StatisticsScreen extends StatelessWidget {
  const StatisticsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(
        title: 'Statistics',
        showBackButton: false,
      ),
      body: Consumer<WaterQualityProvider>(
        builder: (context, provider, child) {
          final assessment = provider.currentAssessment;
          final averageRisks = provider.getAverageRiskScores();

          if (assessment == null) {
            return const Center(
              child: Text('No assessment data available'),
            );
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                // Weekly Analysis Card
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Weekly Analysis',
                          style: Theme.of(context).textTheme.headlineMedium,
                        ),
                        const SizedBox(height: 16),
                        RiskBarChart(
                          title: 'Disease Risk Trends',
                          data: [
                            averageRisks['Cholera'] ?? 0,
                            averageRisks['Typhoid'] ?? 0,
                            averageRisks['Hepatitis A'] ?? 0,
                          ],
                          labels: const ['Cholera', 'Typhoid', 'Hepatitis A'],
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                // Risk Factor Distribution
                RiskDonutChart(
                  title: 'Risk Factor Distribution',
                  data: assessment.contributingFactors,
                ),
                const SizedBox(height: 24),

                // Parameter Summary Cards
                if (provider.currentParameters != null) ...[
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Parameter Summary',
                            style: Theme.of(context).textTheme.headlineMedium,
                          ),
                          const SizedBox(height: 16),
                          _buildParameterRow(
                            context,
                            'Temperature',
                            '${provider.currentParameters!.temperature}°C',
                          ),
                          _buildParameterRow(
                            context,
                            'Turbidity',
                            '${provider.currentParameters!.turbidity} NTU',
                          ),
                          _buildParameterRow(
                            context,
                            'pH Level',
                            '${provider.currentParameters!.pH}',
                          ),
                          _buildParameterRow(
                            context,
                            'E. coli Count',
                            '${provider.currentParameters!.eColiCount} CFU/100ml',
                          ),
                          _buildParameterRow(
                            context,
                            'Dissolved Oxygen',
                            '${provider.currentParameters!.dissolvedOxygen} mg/L',
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildParameterRow(BuildContext context, String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: Theme.of(context).textTheme.bodyLarge,
          ),
          Text(
            value,
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                  color: AppTheme.primaryAccent,
                  fontWeight: FontWeight.w600,
                ),
          ),
        ],
      ),
    );
  }
}
