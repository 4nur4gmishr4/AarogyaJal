enum RiskLevel { low, moderate, high, severe }

class RiskAssessment {
  final double choleraRiskScore;
  final double typhoidRiskScore;
  final double hepatitisARiskScore;
  final Map<String, double> contributingFactors;
  final List<String> recommendations;

  const RiskAssessment({
    required this.choleraRiskScore,
    required this.typhoidRiskScore,
    required this.hepatitisARiskScore,
    required this.contributingFactors,
    required this.recommendations,
  });

  RiskLevel getOverallRiskLevel() {
    double maxRisk = [choleraRiskScore, typhoidRiskScore, hepatitisARiskScore]
        .reduce((curr, next) => curr > next ? curr : next);

    if (maxRisk >= 0.75) return RiskLevel.severe;
    if (maxRisk >= 0.5) return RiskLevel.high;
    if (maxRisk >= 0.25) return RiskLevel.moderate;
    return RiskLevel.low;
  }

  Map<String, dynamic> toJson() => {
        'choleraRiskScore': choleraRiskScore,
        'typhoidRiskScore': typhoidRiskScore,
        'hepatitisARiskScore': hepatitisARiskScore,
        'contributingFactors': contributingFactors,
        'recommendations': recommendations,
      };

  factory RiskAssessment.fromJson(Map<String, dynamic> json) {
    return RiskAssessment(
      choleraRiskScore: json['choleraRiskScore'] as double,
      typhoidRiskScore: json['typhoidRiskScore'] as double,
      hepatitisARiskScore: json['hepatitisARiskScore'] as double,
      contributingFactors:
          Map<String, double>.from(json['contributingFactors']),
      recommendations: List<String>.from(json['recommendations']),
    );
  }
  
  RiskAssessment copyWith({
    double? choleraRiskScore,
    double? typhoidRiskScore,
    double? hepatitisARiskScore,
    Map<String, double>? contributingFactors,
    List<String>? recommendations,
  }) {
    return RiskAssessment(
      choleraRiskScore: choleraRiskScore ?? this.choleraRiskScore,
      typhoidRiskScore: typhoidRiskScore ?? this.typhoidRiskScore,
      hepatitisARiskScore: hepatitisARiskScore ?? this.hepatitisARiskScore,
      contributingFactors: contributingFactors ?? this.contributingFactors,
      recommendations: recommendations ?? this.recommendations,
    );
  }
}
