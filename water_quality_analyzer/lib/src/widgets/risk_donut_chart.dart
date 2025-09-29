import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../theme/app_theme.dart';

class RiskDonutChart extends StatelessWidget {
  final Map<String, double> data;
  final String title;

  const RiskDonutChart({
    super.key,
    required this.data,
    required this.title,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            const SizedBox(height: 24),
            SizedBox(
              height: 200,
              child: PieChart(
                PieChartData(
                  sectionsSpace: 4,
                  centerSpaceRadius: 40,
                  sections: data.entries.map((entry) {
                    final colors = [
                      AppTheme.donutYellow,
                      AppTheme.donutPurple,
                      AppTheme.donutDark,
                    ];
                    final index = data.keys.toList().indexOf(entry.key);

                    return PieChartSectionData(
                      color: colors[index % colors.length],
                      value: entry.value,
                      title: '${(entry.value * 100).toInt()}%',
                      radius: 80,
                      titleStyle: const TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    );
                  }).toList(),
                ),
              ),
            ),
            const SizedBox(height: 16),
            Column(
              children: data.entries.map((entry) {
                final colors = [
                  AppTheme.donutYellow,
                  AppTheme.donutPurple,
                  AppTheme.donutDark,
                ];
                final index = data.keys.toList().indexOf(entry.key);

                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4.0),
                  child: Row(
                    children: [
                      Container(
                        width: 16,
                        height: 16,
                        decoration: BoxDecoration(
                          color: colors[index % colors.length],
                          shape: BoxShape.circle,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        entry.key,
                        style: Theme.of(context).textTheme.bodyLarge,
                      ),
                    ],
                  ),
                );
              }).toList(),
            ),
          ],
        ),
      ),
    );
  }
}
