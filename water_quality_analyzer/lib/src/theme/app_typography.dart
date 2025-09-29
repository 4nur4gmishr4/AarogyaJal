import 'package:flutter/material.dart';

import 'app_colors.dart';

class AppTypography {
  static TextTheme textTheme = TextTheme(
    // Headings
    displayLarge: const TextStyle(
      fontFamily: 'Poppins',
      fontSize: 24,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
      height: 1.5,
    ),
    displayMedium: const TextStyle(
      fontFamily: 'Poppins',
      fontSize: 20,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
      height: 1.5,
    ),
    displaySmall: const TextStyle(
      fontFamily: 'Poppins',
      fontSize: 18,
      fontWeight: FontWeight.w600,
      color: AppColors.textPrimary,
      height: 1.5,
    ),
    
    // Body Text
    bodyLarge: const TextStyle(
      fontFamily: 'Roboto',
      fontSize: 16,
      fontWeight: FontWeight.w400,
      color: AppColors.textPrimary,
      height: 1.5,
    ),
    bodyMedium: const TextStyle(
      fontFamily: 'Roboto',
      fontSize: 14,
      fontWeight: FontWeight.w400,
      color: AppColors.textPrimary,
      height: 1.5,
    ),
    bodySmall: const TextStyle(
      fontFamily: 'Roboto',
      fontSize: 12,
      fontWeight: FontWeight.w400,
      color: AppColors.textSecondary,
      height: 1.5,
    ),
    
    // Labels
    labelLarge: const TextStyle(
      fontFamily: 'Roboto',
      fontSize: 16,
      fontWeight: FontWeight.w500,
      color: AppColors.textPrimary,
      height: 1.5,
    ),
    labelMedium: const TextStyle(
      fontFamily: 'Roboto',
      fontSize: 14,
      fontWeight: FontWeight.w500,
      color: AppColors.textPrimary,
      height: 1.5,
    ),
    labelSmall: const TextStyle(
      fontFamily: 'Roboto',
      fontSize: 12,
      fontWeight: FontWeight.w500,
      color: AppColors.textSecondary,
      height: 1.5,
    ),
  );
}
