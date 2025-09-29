import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/water_quality_provider.dart';
import '../theme/app_theme.dart';

class RemindersScreen extends StatelessWidget {
  const RemindersScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Recommendations'),
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

          if (assessment == null || assessment.recommendations.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.check_circle_outline,
                    size: 64,
                    color: Colors.grey.withOpacity(0.5),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'No active recommendations',
                    style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                          color: Colors.grey,
                        ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Your water quality parameters are within safe limits',
                    style: Theme.of(context).textTheme.bodyMedium,
                    textAlign: TextAlign.center,
                  ),
                ],
              ),
            );
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16.0),
            itemCount: assessment.recommendations.length,
            itemBuilder: (context, index) {
              final recommendation = assessment.recommendations[index];
              return Card(
                margin: const EdgeInsets.only(bottom: 16.0),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Container(
                            padding: const EdgeInsets.all(8),
                            decoration: BoxDecoration(
                              color: AppTheme.primaryAccent.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(8),
                            ),
                            child: Icon(
                              _getIconForRecommendation(recommendation),
                              color: AppTheme.primaryAccent,
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  _getTitleForRecommendation(recommendation),
                                  style: Theme.of(context)
                                      .textTheme
                                      .headlineMedium,
                                ),
                                const SizedBox(height: 8),
                                Text(
                                  recommendation,
                                  style: Theme.of(context).textTheme.bodyLarge,
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Row(
                        children: [
                          Expanded(
                            child: OutlinedButton(
                              onPressed: () {
                                // TODO: Implement mark as done functionality
                              },
                              style: OutlinedButton.styleFrom(
                                foregroundColor: AppTheme.primaryAccent,
                                side: BorderSide(color: AppTheme.primaryAccent),
                                padding:
                                    const EdgeInsets.symmetric(vertical: 12),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                              ),
                              child: const Text('Mark as Done'),
                            ),
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: ElevatedButton(
                              onPressed: () {
                                // TODO: Implement reminder functionality
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: AppTheme.primaryAccent,
                                padding:
                                    const EdgeInsets.symmetric(vertical: 12),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                              ),
                              child: const Text('Set Reminder'),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              );
            },
          );
        },
      ),
    );
  }

  IconData _getIconForRecommendation(String recommendation) {
    if (recommendation.toLowerCase().contains('boil')) {
      return Icons.local_fire_department_outlined;
    }
    if (recommendation.toLowerCase().contains('filter') ||
        recommendation.toLowerCase().contains('physical')) {
      return Icons.filter_alt_outlined;
    }
    if (recommendation.toLowerCase().contains('chemical')) {
      return Icons.science_outlined;
    }
    return Icons.warning_amber_outlined;
  }

  String _getTitleForRecommendation(String recommendation) {
    if (recommendation.toLowerCase().contains('boil')) {
      return 'Water Treatment Required';
    }
    if (recommendation.toLowerCase().contains('filter') ||
        recommendation.toLowerCase().contains('physical')) {
      return 'Filtration Needed';
    }
    if (recommendation.toLowerCase().contains('chemical')) {
      return 'Chemical Treatment';
    }
    return 'Important Action Required';
  }
}
