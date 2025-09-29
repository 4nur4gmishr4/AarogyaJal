import 'package:flutter/material.dart';
import '../models/educational_module.dart';

class CategorySelector extends StatelessWidget {
  final ModuleCategory selectedCategory;
  final Function(ModuleCategory) onCategorySelected;

  const CategorySelector({
    Key? key,
    required this.selectedCategory,
    required this.onCategorySelected,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 120,
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: ListView(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        children: ModuleCategory.values.map((category) {
          final isSelected = category == selectedCategory;
          return Padding(
            padding: const EdgeInsets.only(right: 16),
            child: InkWell(
              onTap: () => onCategorySelected(category),
              borderRadius: BorderRadius.circular(12),
              child: Container(
                width: 100,
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: isSelected
                      ? Theme.of(context).colorScheme.primaryContainer
                      : Theme.of(context).colorScheme.surfaceVariant,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      _getCategoryIcon(category),
                      color: isSelected
                          ? Theme.of(context).colorScheme.onPrimaryContainer
                          : Theme.of(context).colorScheme.onSurfaceVariant,
                    ),
                    const SizedBox(height: 8),
                    Text(
                      _getCategoryName(category),
                      style: Theme.of(context).textTheme.labelSmall?.copyWith(
                            color: isSelected
                                ? Theme.of(context).colorScheme.onPrimaryContainer
                                : Theme.of(context).colorScheme.onSurfaceVariant,
                          ),
                      textAlign: TextAlign.center,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
            ),
          );
        }).toList(),
      ),
    );
  }

  IconData _getCategoryIcon(ModuleCategory category) {
    switch (category) {
      case ModuleCategory.waterSafety:
        return Icons.water_drop;
      case ModuleCategory.handwashing:
        return Icons.clean_hands;
      case ModuleCategory.waterPurification:
        return Icons.filter_alt;
      case ModuleCategory.diseaseRecognition:
        return Icons.medical_services;
      case ModuleCategory.homeHygiene:
        return Icons.home;
      case ModuleCategory.communitySanitation:
        return Icons.people;
      case ModuleCategory.emergencyResponse:
        return Icons.emergency;
      case ModuleCategory.childHealth:
        return Icons.child_care;
    }
  }

  String _getCategoryName(ModuleCategory category) {
    return category.toString().split('.').last.replaceAll(RegExp(r'(?=[A-Z])'), ' ');
  }
}
