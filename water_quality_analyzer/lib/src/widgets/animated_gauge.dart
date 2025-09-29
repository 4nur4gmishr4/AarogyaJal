import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter/animation.dart';

class AnimatedGauge extends StatefulWidget {
  final String title;
  final double value;
  final double minValue;
  final double maxValue;
  final String unit;
  final Color color; // This will be used as an accent color
  final IconData icon;

  const AnimatedGauge({
    Key? key,
    required this.title,
    required this.value,
    required this.minValue,
    required this.maxValue,
    required this.unit,
    required this.color,
    required this.icon,
  }) : super(key: key);

  @override
  State<AnimatedGauge> createState() => _AnimatedGaugeState();
}

class _AnimatedGaugeState extends State<AnimatedGauge>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    );

    // Animation sequence: 0 -> 180 -> final value
    final normalizedValue = (widget.value - widget.minValue) /
        (widget.maxValue - widget.minValue) *
        180;

    _animation = TweenSequence<double>([
      TweenSequenceItem(
        tween: Tween<double>(begin: 0, end: 180),
        weight: 40,
      ),
      TweenSequenceItem(
        tween: Tween<double>(begin: 180, end: normalizedValue),
        weight: 60,
      ),
    ]).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  // Get color based on value (red for bad, green for good)
  Color _getValueColor() {
    // Calculate normalized value between 0 and 1
    final normalizedValue = (widget.value - widget.minValue) / (widget.maxValue - widget.minValue);
    
    // Clamp to ensure it's between 0 and 1
    final clampedValue = normalizedValue.clamp(0.0, 1.0);
    
    // Red for bad (0.0), green for good (1.0)
    if (clampedValue < 0.5) {
      // From red to yellow
      return Color.lerp(Colors.red, Colors.yellow, clampedValue * 2) ?? Colors.red;
    } else {
      // From yellow to green
      return Color.lerp(Colors.yellow, Colors.green, (clampedValue - 0.5) * 2) ?? Colors.green;
    }
  }
  
  @override
  Widget build(BuildContext context) {
    final valueColor = _getValueColor();
    
    return Card(
      elevation: 1,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  widget.title,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 14,
                  ),
                ),
                Icon(
                  widget.icon,
                  color: valueColor,
                  size: 20,
                ),
              ],
            ),
            const SizedBox(height: 12),
            AnimatedBuilder(
              animation: _animation,
              builder: (context, child) {
                return CustomPaint(
                  size: const Size(double.infinity, 80),
                  painter: MinimalGaugePainter(
                    angle: _animation.value,
                    color: valueColor,
                  ),
                );
              },
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  '${widget.value.toStringAsFixed(1)}',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: valueColor,
                  ),
                ),
                Text(
                  ' ${widget.unit}',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              ],
            ),
            Text(
              'Range: ${widget.minValue} - ${widget.maxValue}',
              style: TextStyle(
                fontSize: 12,
                color: Colors.grey[600],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class MinimalGaugePainter extends CustomPainter {
  final double angle;
  final Color color;

  MinimalGaugePainter({required this.angle, required this.color});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2 + 10);
    final radius = math.min(size.width / 2, size.height / 2) - 10;
    
    // Draw background arc - thin and light
    final backgroundPaint = Paint()
      ..color = Colors.grey.withOpacity(0.15)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 6;
    
    // Draw tick marks
    final tickPaint = Paint()
      ..color = Colors.grey.withOpacity(0.3)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1;
      
    // Draw small tick marks
    for (int i = 0; i <= 60; i++) {
      if (i % 10 == 0) continue; // Skip major ticks
      final tickAngle = math.pi + (i / 60) * math.pi;
      final innerPoint = Offset(
        center.dx + (radius - 2) * math.cos(tickAngle),
        center.dy + (radius - 2) * math.sin(tickAngle),
      );
      final outerPoint = Offset(
        center.dx + radius * math.cos(tickAngle),
        center.dy + radius * math.sin(tickAngle),
      );
      canvas.drawLine(innerPoint, outerPoint, tickPaint);
    }
    
    // Draw major tick marks
    final majorTickPaint = Paint()
      ..color = Colors.grey.withOpacity(0.5)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 1.5;
      
    for (int i = 0; i <= 60; i += 10) {
      final tickAngle = math.pi + (i / 60) * math.pi;
      final innerPoint = Offset(
        center.dx + (radius - 5) * math.cos(tickAngle),
        center.dy + (radius - 5) * math.sin(tickAngle),
      );
      final outerPoint = Offset(
        center.dx + radius * math.cos(tickAngle),
        center.dy + radius * math.sin(tickAngle),
      );
      canvas.drawLine(innerPoint, outerPoint, majorTickPaint);
    }
    
    // Draw background arc
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      math.pi,
      math.pi,
      false,
      backgroundPaint,
    );
    
    // Draw value arc - thicker and colored
    final valuePaint = Paint()
      ..color = color
      ..style = PaintingStyle.stroke
      ..strokeWidth = 6
      ..strokeCap = StrokeCap.round;
    
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      math.pi,
      angle * math.pi / 180,
      false,
      valuePaint,
    );
    
    // Draw a small circle at the center
    final centerPaint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;
    
    canvas.drawCircle(
      center,
      3,
      centerPaint,
    );
  }

  @override
  bool shouldRepaint(covariant MinimalGaugePainter oldDelegate) {
    return oldDelegate.angle != angle || oldDelegate.color != color;
  }
}