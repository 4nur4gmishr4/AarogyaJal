enum ModuleCategory {
  waterSafety,
  handwashing,
  waterPurification,
  diseaseRecognition,
  homeHygiene,
  communitySanitation,
  emergencyResponse,
  childHealth,
}

enum ModuleDifficulty {
  beginner,
  intermediate,
  advanced,
}

class EducationalModule {
  final String id;
  final String title;
  final String description;
  final ModuleCategory category;
  final ModuleDifficulty difficulty;
  final String thumbnailUrl;
  final List<ModuleContent> contents;
  final List<String> languages;
  final int estimatedMinutes;
  final bool isDownloadable;
  final Map<String, dynamic> progress;
  final List<Achievement> achievements;

  const EducationalModule({
    required this.id,
    required this.title,
    required this.description,
    required this.category,
    required this.difficulty,
    required this.thumbnailUrl,
    required this.contents,
    required this.languages,
    required this.estimatedMinutes,
    this.isDownloadable = true,
    this.progress = const {},
    this.achievements = const [],
  });

  double get completionPercentage {
    if (progress.isEmpty) return 0.0;
    int completed = progress.values.where((v) => v == true).length;
    return (completed / contents.length) * 100;
  }
}

class ModuleContent {
  final String id;
  final String title;
  final ContentType type;
  final String content;
  final Map<String, String> localizedContent;
  final bool requiresInternet;
  final int orderIndex;

  const ModuleContent({
    required this.id,
    required this.title,
    required this.type,
    required this.content,
    this.localizedContent = const {},
    this.requiresInternet = false,
    required this.orderIndex,
  });
}

enum ContentType {
  video,
  audio,
  text,
  infographic,
  quiz,
  interactive,
}

class Achievement {
  final String id;
  final String title;
  final String description;
  final String iconPath;
  final int pointsValue;
  final bool isUnlocked;

  const Achievement({
    required this.id,
    required this.title,
    required this.description,
    required this.iconPath,
    required this.pointsValue,
    this.isUnlocked = false,
  });
}

class Quiz {
  final String id;
  final String title;
  final List<Question> questions;
  final int passingScore;
  final bool isCompleted;
  final int? bestScore;

  const Quiz({
    required this.id,
    required this.title,
    required this.questions,
    this.passingScore = 70,
    this.isCompleted = false,
    this.bestScore,
  });
}

class Question {
  final String id;
  final String question;
  final Map<String, String> localizedQuestions;
  final List<String> options;
  final Map<String, List<String>> localizedOptions;
  final int correctOptionIndex;
  final String? explanation;
  final String? imageUrl;

  const Question({
    required this.id,
    required this.question,
    this.localizedQuestions = const {},
    required this.options,
    this.localizedOptions = const {},
    required this.correctOptionIndex,
    this.explanation,
    this.imageUrl,
  });
}
