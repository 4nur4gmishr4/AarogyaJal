import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/water_quality_provider.dart';
import '../widgets/metric_card.dart';
import '../widgets/risk_bar_chart.dart';
import '../widgets/animated_gauge.dart';
import '../theme/app_theme.dart';
import '../models/risk_assessment.dart';
import '../widgets/custom_app_bar.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(
        title: 'AarogyaJal',
        showBackButton: false,
      ),
      body: SafeArea(
        child: Consumer<WaterQualityProvider>(
          builder: (context, provider, child) {
            final assessment = provider.currentAssessment;

            return SingleChildScrollView(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Good Morning',
                            style: TextStyle(
                              fontSize: 24,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Text(
                            'Today, ${DateTime.now().day} ${_getMonth(DateTime.now().month)} ${DateTime.now().year}',
                            style: Theme.of(context).textTheme.bodyMedium,
                          ),
                        ],
                      ),
                      IconButton(
                        icon: const Icon(Icons.notifications_outlined),
                        onPressed: () {
                          // Navigate to notifications
                        },
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  if (assessment != null) ...[
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(
                          'Water Quality Parameters',
                          style: Theme.of(context).textTheme.headlineMedium,
                        ),
                        IconButton(
                          icon: const Icon(Icons.refresh),
                          onPressed: () {
                            // Force rebuild to trigger animations
                            setState(() {});
                          },
                        ),
                      ],
                    ),
                    const SizedBox(height: 16),
                    _buildGaugesGrid(context, provider),
                    const SizedBox(height: 24),
                    Card(
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Text(
                                  'Risk Assessment',
                                  style: Theme.of(context)
                                      .textTheme
                                      .headlineMedium,
                                ),
                                _buildRiskLevelChip(
                                    assessment.getOverallRiskLevel()),
                              ],
                            ),
                            const SizedBox(height: 24),
                            Row(
                              children: [
                                Expanded(
                                  child: MetricCard(
                                    title: 'Cholera Risk',
                                    value:
                                        '${(assessment.choleraRiskScore * 100).toInt()}',
                                    unit: '%',
                                    icon: Icons.coronavirus_outlined,
                                    iconColor: AppTheme.chartPurple,
                                  ),
                                ),
                                const SizedBox(width: 16),
                                Expanded(
                                  child: MetricCard(
                                    title: 'Typhoid Risk',
                                    value:
                                        '${(assessment.typhoidRiskScore * 100).toInt()}',
                                    unit: '%',
                                    icon: Icons.sick_outlined,
                                    iconColor: AppTheme.chartBlue,
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 16),
                            MetricCard(
                              title: 'Hepatitis A Risk',
                              value:
                                  '${(assessment.hepatitisARiskScore * 100).toInt()}',
                              unit: '%',
                              icon: Icons.medical_services_outlined,
                              iconColor: AppTheme.chartGrey,
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),
                    RiskBarChart(
                      title: 'Risk Factors Analysis',
                      data: [
                        assessment.contributingFactors[
                                'Biological Contamination'] ??
                            0,
                        assessment.contributingFactors['Chemical Parameters'] ??
                            0,
                        assessment.contributingFactors['Physical Conditions'] ??
                            0,
                      ],
                      labels: const [
                        'Biological',
                        'Chemical',
                        'Physical',
                      ],
                    ),
                    const SizedBox(height: 24),
                    if (assessment.recommendations.isNotEmpty)
                      Card(
                        child: Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Recommendations',
                                style:
                                    Theme.of(context).textTheme.headlineMedium,
                              ),
                              const SizedBox(height: 16),
                              ...assessment.recommendations
                                  .map((rec) => Padding(
                                        padding: const EdgeInsets.symmetric(
                                            vertical: 4.0),
                                        child: Row(
                                          children: [
                                            Icon(
                                              Icons.info_outline,
                                              color: AppTheme.primaryAccent,
                                              size: 20,
                                            ),
                                            const SizedBox(width: 8),
                                            Expanded(
                                              child: Text(
                                                rec,
                                                style: Theme.of(context)
                                                    .textTheme
                                                    .bodyLarge,
                                              ),
                                            ),
                                          ],
                                        ),
                                      )),
                            ],
                          ),
                        ),
                      ),
                  ] else
                    const Center(
                      child: Text(
                          'No assessment data available. Add new water quality parameters to begin.'),
                    ),
                ],
              ),
            );
          },
        ),
      ),
    );
  }

  String _getMonth(int month) {
    const months = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December'
    ];
    return months[month - 1];
  }

  Widget _buildRiskLevelChip(RiskLevel level) {
    late final Color color;
    late final String text;

    switch (level) {
      case RiskLevel.low:
        color = Colors.green;
        text = 'Low Risk';
      case RiskLevel.moderate:
        color = Colors.orange;
        text = 'Moderate Risk';
      case RiskLevel.high:
        color = Colors.red;
        text = 'High Risk';
      case RiskLevel.severe:
        color = Colors.purple;
        text = 'Severe Risk';
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Text(
        text,
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.w600,
          fontSize: 12,
        ),
      ),
    );
  }

  Widget _buildGaugesGrid(BuildContext context, WaterQualityProvider provider) {
    final parameters = provider.currentParameters;
    if (parameters == null) return const SizedBox.shrink();

    return GridView.count(
      crossAxisCount: 2,
      mainAxisSpacing: 16,
      crossAxisSpacing: 16,
      childAspectRatio: 0.85,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      children: [
        AnimatedGauge(
          title: 'Temperature',
          value: parameters.temperature,
          minValue: 0,
          maxValue: 40,
          unit: '°C',
          color: Colors.red,
          icon: Icons.thermostat,
        ),
        AnimatedGauge(
          title: 'Turbidity',
          value: parameters.turbidity,
          minValue: 0,
          maxValue: 10,
          unit: 'NTU',
          color: Colors.brown,
          icon: Icons.opacity,
        ),
        AnimatedGauge(
          title: 'pH Level',
          value: parameters.pH,
          minValue: 0,
          maxValue: 14,
          unit: '',
          color: Colors.purple,
          icon: Icons.science,
        ),
        AnimatedGauge(
          title: 'Dissolved Oxygen',
          value: parameters.dissolvedOxygen,
          minValue: 0,
          maxValue: 20,
          unit: 'mg/L',
          color: Colors.blue,
          icon: Icons.air,
        ),
        AnimatedGauge(
          title: 'Nitrates',
          value: parameters.nitrates,
          minValue: 0,
          maxValue: 50,
          unit: 'mg/L',
          color: Colors.green,
          icon: Icons.grass,
        ),
        AnimatedGauge(
          title: 'Salinity',
          value: parameters.salinity,
          minValue: 0,
          maxValue: 40,
          unit: 'ppt',
          color: Colors.teal,
          icon: Icons.water_drop,
        ),
        AnimatedGauge(
          title: 'E. coli Count',
          value: parameters.eColiCount.toDouble(),
          minValue: 0,
          maxValue: 500,
          unit: 'CFU',
          color: Colors.orange,
          icon: Icons.bug_report,
        ),
        AnimatedGauge(
          title: 'Total Coliform',
          value: parameters.totalColiforms.toDouble(),
          minValue: 0,
          maxValue: 1000,
          unit: 'CFU',
          color: Colors.amber,
          icon: Icons.biotech,
        ),
      ],
    );
  }
}
