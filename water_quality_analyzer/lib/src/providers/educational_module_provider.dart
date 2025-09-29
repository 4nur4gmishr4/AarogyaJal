import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/educational_module.dart';

class EducationalModuleProvider extends ChangeNotifier {
  final SharedPreferences _prefs;
  List<EducationalModule> _modules = [];
  String _currentLanguage = 'en';
  bool _isOfflineMode = false;
  Map<String, double> _progress = {};

  EducationalModuleProvider(this._prefs) {
    _loadInitialData();
  }

  // Getters
  List<EducationalModule> get modules => _modules;
  String get currentLanguage => _currentLanguage;
  bool get isOfflineMode => _isOfflineMode;
  Map<String, double> get progress => _progress;

  List<EducationalModule> getModulesByCategory(ModuleCategory category) {
    return _modules.where((m) => m.category == category).toList();
  }

  Future<void> _loadInitialData() async {
    try {
      _currentLanguage = _prefs.getString('selected_language') ?? 'en';
      _isOfflineMode = _prefs.getBool('offline_mode') ?? false;
      await _loadProgress();
      await _loadModules();
      notifyListeners();
    } catch (e) {
      debugPrint('Error loading initial data: $e');
      // Set default values
      _currentLanguage = 'en';
      _isOfflineMode = false;
      _modules = [];
      _progress = {};
      notifyListeners();
    }
  }

  Future<void> _loadModules() async {
    try {
      // TODO: Implement API call or local data loading
      // For now, loading dummy data
      _modules = [
        EducationalModule(
          id: 'water_safety_101',
          title: 'Water Safety Basics',
          description:
              'Learn the fundamentals of water safety and contamination prevention',
          category: ModuleCategory.waterSafety,
          difficulty: ModuleDifficulty.beginner,
          thumbnailUrl: 'assets/images/water_safety.png',
          contents: [
            ModuleContent(
              id: 'intro_video',
              title: 'Introduction to Water Safety',
              type: ContentType.video,
              content: 'assets/videos/water_safety_intro.mp4',
              orderIndex: 0,
            ),
            ModuleContent(
              id: 'safety_basics',
              title: 'Basic Water Safety Guidelines',
              type: ContentType.text,
              content:
                  'Learn about the fundamental principles of water safety...',
              orderIndex: 1,
            ),
            ModuleContent(
              id: 'contamination_types',
              title: 'Types of Water Contamination',
              type: ContentType.infographic,
              content: 'assets/images/contamination_types.png',
              orderIndex: 2,
            ),
          ],
          languages: ['en', 'hi', 'bn', 'as'],
          estimatedMinutes: 30,
        ),
      ];
    } catch (e) {
      debugPrint('Error loading modules: $e');
      _modules = [];
    }
  }

  Future<void> _loadProgress() async {
    try {
      final progressData = _prefs.getString('modules_progress');
      if (progressData != null) {
        // TODO: Implement progress loading from SharedPreferences
        // For now, just initialize an empty progress map
        _progress = {};
      } else {
        _progress = {};
      }
    } catch (e) {
      debugPrint('Error loading progress: $e');
      _progress = {};
    }
  }

  Future<void> setLanguage(String languageCode) async {
    _currentLanguage = languageCode;
    await _prefs.setString('selected_language', languageCode);
    notifyListeners();
  }

  Future<void> toggleOfflineMode() async {
    _isOfflineMode = !_isOfflineMode;
    await _prefs.setBool('offline_mode', _isOfflineMode);
    notifyListeners();
  }

  Future<void> updateProgress(String moduleId, double progress) async {
    _progress[moduleId] = progress;
    // TODO: Implement progress saving to SharedPreferences
    notifyListeners();
  }

  Future<void> downloadModule(String moduleId) async {
    // TODO: Implement module downloading for offline use
    notifyListeners();
  }

  Future<void> completeQuiz(String moduleId, String quizId, int score) async {
    // TODO: Implement quiz completion and achievement unlocking
    notifyListeners();
  }

  List<Achievement> getUnlockedAchievements() {
    // TODO: Implement achievement tracking
    return [];
  }
}
