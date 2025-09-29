import 'dart:math' as math;
import 'package:flutter/material.dart';

class ParameterGauge extends StatelessWidget {
  final String title;
  final double value;
  final double minValue;
  final double maxValue;
  final String unit;
  final List<Color> gradientColors;

  const ParameterGauge({
    super.key,
    required this.title,
    required this.value,
    required this.minValue,
    required this.maxValue,
    required this.unit,
    this.gradientColors = const [
      Color(0xFF4CAF50), // Safe
      Color(0xFFFFA726), // Warning
      Color(0xFFEF5350), // Danger
    ],
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      surfaceTintColor: Colors.transparent,
      shadowColor: Colors.black12,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              title,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 120,
              width: 120,
              child: CustomPaint(
                painter: GaugePainter(
                  value: value,
                  minValue: minValue,
                  maxValue: maxValue,
                  gradientColors: gradientColors,
                ),
                child: Center(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        value.toStringAsFixed(1),
                        style:
                            Theme.of(context).textTheme.headlineSmall?.copyWith(
                                  fontWeight: FontWeight.bold,
                                ),
                      ),
                      Text(
                        unit,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class GaugePainter extends CustomPainter {
  final double value;
  final double minValue;
  final double maxValue;
  final List<Color> gradientColors;

  GaugePainter({
    required this.value,
    required this.minValue,
    required this.maxValue,
    required this.gradientColors,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = math.min(size.width, size.height) * 0.4;

    // Draw background arc
    final bgPaint = Paint()
      ..color = Colors.grey[200]!
      ..style = PaintingStyle.stroke
      ..strokeWidth = 12
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      math.pi * 0.8,
      math.pi * 1.4,
      false,
      bgPaint,
    );

    // Draw value arc
    final progress = (value - minValue) / (maxValue - minValue);
    final sweepAngle = math.pi * 1.4 * progress;

    final gradient = SweepGradient(
      colors: gradientColors,
      stops: const [0.0, 0.5, 1.0],
      startAngle: math.pi * 0.8,
      endAngle: math.pi * 2.2,
    );

    final valuePaint = Paint()
      ..shader = gradient.createShader(
        Rect.fromCircle(center: center, radius: radius),
      )
      ..style = PaintingStyle.stroke
      ..strokeWidth = 12
      ..strokeCap = StrokeCap.round;

    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      math.pi * 0.8,
      sweepAngle,
      false,
      valuePaint,
    );

    // Draw ticks
    final tickPaint = Paint()
      ..color = Colors.grey[400]!
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2;

    for (var i = 0; i <= 10; i++) {
      final angle = math.pi * 0.8 + (math.pi * 1.4 * i / 10);
      final outerPoint = Offset(
        center.dx + (radius + 10) * math.cos(angle),
        center.dy + (radius + 10) * math.sin(angle),
      );
      final innerPoint = Offset(
        center.dx + (radius - 10) * math.cos(angle),
        center.dy + (radius - 10) * math.sin(angle),
      );
      canvas.drawLine(innerPoint, outerPoint, tickPaint);
    }
  }

  @override
  bool shouldRepaint(covariant GaugePainter oldDelegate) {
    return oldDelegate.value != value ||
        oldDelegate.minValue != minValue ||
        oldDelegate.maxValue != maxValue;
  }
}
