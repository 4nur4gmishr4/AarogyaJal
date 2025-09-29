import 'package:flutter/material.dart';

class AppColors {
  // Primary Colors
  static const Color primary = Color(0xFF6C63FF);
  static const Color primaryAccent = Color(0xFF3700B3);
  static const Color secondary = Color(0xFF4CAF50);
  static const Color background = Color(0xFFF9FAFB);
  static const Color cardBackground = Colors.white;

  // Chart Colors
  static const Color chartPurple = Color(0xFF6C63FF);
  static const Color chartBlue = Color(0xFF03A9F4);
  static const Color chartGrey = Color(0xFF9E9E9E);

  // Donut Chart Colors
  static const Color donutYellow = Color(0xFFFFC107);
  static const Color donutPurple = Color(0xFF6C63FF);
  static const Color donutDark = Color(0xFF1D1D1D);

  // Text Colors
  static const Color textPrimary = Color(0xFF1A1A1A);
  static const Color textSecondary = Color(0xFF6B7280);

  // Status Colors
  static const Color success = Color(0xFF4CAF50);
  static const Color warning = Color(0xFFFFA726);
  static const Color error = Color(0xFFEF5350);
  static const Color info = Color(0xFF42A5F5);

  // Risk Level Colors
  static const Color riskLow = Color(0xFF4CAF50);
  static const Color riskModerate = Color(0xFFFFA726);
  static const Color riskHigh = Color(0xFFEF5350);

  // Gradients
  static const LinearGradient primaryGradient = LinearGradient(
    colors: [primary, Color(0xFF8B85FF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient alertGradient = LinearGradient(
    colors: [Color(0x996C63FF), Color(0x994CAF50)],
    begin: Alignment.centerLeft,
    end: Alignment.centerRight,
  );

  // Card Shadow
  static List<BoxShadow> cardShadow = [
    BoxShadow(
      color: Colors.black.withOpacity(0.05),
      blurRadius: 10,
      offset: const Offset(0, 4),
    ),
  ];
}
