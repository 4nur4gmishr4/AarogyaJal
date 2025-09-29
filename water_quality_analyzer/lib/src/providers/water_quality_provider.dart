import 'package:flutter/foundation.dart';
import '../models/water_quality_parameters.dart';
import '../models/risk_assessment.dart';
import '../services/risk_calculator_service.dart';
import '../services/backend_service.dart';

class WaterQualityProvider with ChangeNotifier {
  final RiskCalculatorService _calculator = RiskCalculatorService();
  final BackendService _backendService = BackendService();
  WaterQualityParameters? _currentParameters;
  RiskAssessment? _currentAssessment;
  List<RiskAssessment> _historicalAssessments = [];
  bool _isLoading = false;

  WaterQualityParameters? get currentParameters => _currentParameters;
  RiskAssessment? get currentAssessment => _currentAssessment;
  List<RiskAssessment> get historicalAssessments => _historicalAssessments;
  bool get isLoading => _isLoading;

  void setWaterQualityParameters(WaterQualityParameters parameters) {
    _currentParameters = parameters;
    _calculateRisk();
    notifyListeners();
  }
  
  Future<void> analyzeWithBackend(WaterQualityParameters parameters, String location, String notes) async {
    _isLoading = true;
    notifyListeners();
    
    try {
      final result = await _backendService.analyzeWaterQuality(parameters, location, notes);
      
      // Update the assessment with additional insights from the backend if needed
      // This could be extended to incorporate AI-generated recommendations
      if (_currentAssessment != null) {
        // Add any AI-generated recommendations to the existing ones
        if (result.containsKey('analysis')) {
          // Parse recommendations from the analysis text
          final analysisText = result['analysis'] as String;
          if (analysisText.contains('Recommendation') || analysisText.contains('recommendation')) {
            final recommendations = _parseRecommendations(analysisText);
            _currentAssessment = _currentAssessment!.copyWith(
              recommendations: [..._currentAssessment!.recommendations, ...recommendations],
            );
          }
        }
      }
      
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      rethrow;
    }
  }
  
  List<String> _parseRecommendations(String analysisText) {
    // Simple parsing logic to extract recommendations
    // This could be improved with more sophisticated text parsing
    final recommendations = <String>[];
    
    // Split by newlines and look for recommendation patterns
    final lines = analysisText.split('\n');
    for (final line in lines) {
      if (line.toLowerCase().contains('recommend') && line.trim().isNotEmpty) {
        recommendations.add(line.trim());
      }
    }
    
    return recommendations;
  }

  void _calculateRisk() {
    if (_currentParameters != null) {
      _currentAssessment =
          _calculator.calculateOverallRisk(_currentParameters!);
      _historicalAssessments = [_currentAssessment!, ..._historicalAssessments];
      notifyListeners();
    }
  }

  void clearHistory() {
    _historicalAssessments = [];
    notifyListeners();
  }

  Map<String, double> getAverageRiskScores() {
    if (_historicalAssessments.isEmpty) return {};

    double avgCholera = 0;
    double avgTyphoid = 0;
    double avgHepatitisA = 0;

    for (var assessment in _historicalAssessments) {
      avgCholera += assessment.choleraRiskScore;
      avgTyphoid += assessment.typhoidRiskScore;
      avgHepatitisA += assessment.hepatitisARiskScore;
    }

    int total = _historicalAssessments.length;
    return {
      'Cholera': avgCholera / total,
      'Typhoid': avgTyphoid / total,
      'Hepatitis A': avgHepatitisA / total,
    };
  }
}
