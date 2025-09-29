import 'package:flutter/material.dart';
import '../models/educational_module.dart';

class AchievementBanner extends StatelessWidget {
  final List<Achievement> achievements;

  const AchievementBanner({
    Key? key,
    required this.achievements,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (achievements.isEmpty) return const SizedBox.shrink();

    return Container(
      height: 80,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: achievements.length,
        itemBuilder: (context, index) {
          final achievement = achievements[index];
          return Padding(
            padding: const EdgeInsets.only(right: 16),
            child: Tooltip(
              message: achievement.description,
              child: CircleAvatar(
                radius: 32,
                backgroundColor: Theme.of(context).colorScheme.secondaryContainer,
                child: Image.asset(
                  achievement.iconPath,
                  width: 40,
                  height: 40,
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
