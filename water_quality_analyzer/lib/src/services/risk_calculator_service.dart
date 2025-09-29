import 'dart:math' as math;
import '../models/water_quality_parameters.dart';
import '../models/risk_assessment.dart';

class RiskCalculatorService {
  double calculateEcoliRisk(WaterQualityParameters params) {
    // Implementation based on E. coli count, temperature, and pH
    double risk = 0.0;

    // E. coli count risk (WHO guidelines)
    if (params.eColiCount > 1000) {
      risk += 0.4;
    } else if (params.eColiCount > 100) {
      risk += 0.3;
    } else if (params.eColiCount > 10) {
      risk += 0.2;
    } else if (params.eColiCount > 0) {
      risk += 0.1;
    }

    // Temperature impact (optimal growth 30-40°C)
    if (params.temperature >= 30 && params.temperature <= 40) {
      risk += 0.3;
    } else if (params.temperature >= 20 && params.temperature < 30) {
      risk += 0.2;
    }

    // pH impact (optimal growth 6.0-8.0)
    if (params.pH >= 6.0 && params.pH <= 8.0) {
      risk += 0.3;
    } else if (params.pH > 4.0 && params.pH < 10.0) {
      risk += 0.1;
    }

    return math.min(risk, 1.0);
  }

  double assessChemicalContamination(WaterQualityParameters params) {
    double risk = 0.0;

    // Nitrates assessment (WHO guideline: 50mg/L max)
    if (params.nitrates > 50) {
      risk += 0.4;
    } else if (params.nitrates > 30) {
      risk += 0.3;
    } else if (params.nitrates > 10) {
      risk += 0.2;
    }

    // Dissolved oxygen assessment (healthy range: 6.5-8mg/L)
    if (params.dissolvedOxygen < 4) {
      risk += 0.4;
    } else if (params.dissolvedOxygen < 6) {
      risk += 0.2;
    }

    // pH assessment
    if (params.pH < 6.5 || params.pH > 8.5) {
      risk += 0.2;
    }

    return math.min(risk, 1.0);
  }

  double analyzePhysicalParameters(WaterQualityParameters params) {
    double risk = 0.0;

    // Turbidity assessment (WHO guideline: <5 NTU)
    if (params.turbidity > 10) {
      risk += 0.4;
    } else if (params.turbidity > 5) {
      risk += 0.2;
    }

    // Temperature assessment
    if (params.temperature > 35) {
      risk += 0.3;
    } else if (params.temperature > 25) {
      risk += 0.2;
    }

    // Salinity impact
    if (params.salinity > 2000) {
      risk += 0.3;
    } else if (params.salinity > 1000) {
      risk += 0.2;
    }

    return math.min(risk, 1.0);
  }

  double detectCholeraRisk(WaterQualityParameters params) {
    double risk = 0.0;

    risk += calculateEcoliRisk(params) * 0.4;
    risk += analyzePhysicalParameters(params) * 0.3;

    // Environmental factors
    if (params.recentFlooding) risk += 0.2;
    if (params.sanitationIndex < 0.5) risk += 0.1;

    // Population density impact
    if (params.populationDensity > 10000) {
      risk += 0.2;
    } else if (params.populationDensity > 5000) {
      risk += 0.1;
    }

    return math.min(risk, 1.0);
  }

  double detectTyphoidRisk(WaterQualityParameters params) {
    double risk = 0.0;

    risk += calculateEcoliRisk(params) * 0.35;
    risk += assessChemicalContamination(params) * 0.25;

    // Specific typhoid factors
    if (params.sanitationIndex < 0.4) risk += 0.2;
    if (params.totalColiforms > 500) risk += 0.2;

    return math.min(risk, 1.0);
  }

  double detectHepatitisARisk(WaterQualityParameters params) {
    double risk = 0.0;

    risk += calculateEcoliRisk(params) * 0.3;
    risk += analyzePhysicalParameters(params) * 0.3;

    // Specific hepatitis A factors
    if (params.sanitationIndex < 0.3) risk += 0.2;
    if (params.populationDensity > 8000) risk += 0.2;

    return math.min(risk, 1.0);
  }

  RiskAssessment calculateOverallRisk(WaterQualityParameters params) {
    double choleraRisk = detectCholeraRisk(params);
    double typhoidRisk = detectTyphoidRisk(params);
    double hepatitisRisk = detectHepatitisARisk(params);

    Map<String, double> contributingFactors = {
      'Biological Contamination': calculateEcoliRisk(params),
      'Chemical Parameters': assessChemicalContamination(params),
      'Physical Conditions': analyzePhysicalParameters(params),
    };

    List<String> recommendations = [];
    if (contributingFactors['Biological Contamination']! > 0.5) {
      recommendations
          .add('Urgent: Water requires biological treatment. Boil before use.');
    }
    if (contributingFactors['Chemical Parameters']! > 0.5) {
      recommendations.add('Chemical treatment or filtration recommended.');
    }
    if (contributingFactors['Physical Conditions']! > 0.5) {
      recommendations
          .add('Physical filtration needed to improve water quality.');
    }

    return RiskAssessment(
      choleraRiskScore: choleraRisk,
      typhoidRiskScore: typhoidRisk,
      hepatitisARiskScore: hepatitisRisk,
      contributingFactors: contributingFactors,
      recommendations: recommendations,
    );
  }
}
