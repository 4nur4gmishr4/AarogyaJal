class WaterQualityParameters {
  final double temperature;
  final double turbidity;
  final double pH;
  final double dissolvedOxygen;
  final double nitrates;
  final int eColiCount;
  final int totalColiforms;
  final double salinity;
  final bool recentFlooding;
  final int populationDensity;
  final double sanitationIndex;

  const WaterQualityParameters({
    required this.temperature,
    required this.turbidity,
    required this.pH,
    required this.dissolvedOxygen,
    required this.nitrates,
    required this.eColiCount,
    required this.totalColiforms,
    required this.salinity,
    required this.recentFlooding,
    required this.populationDensity,
    required this.sanitationIndex,
  });

  Map<String, dynamic> toJson() => {
        'temperature': temperature,
        'turbidity': turbidity,
        'pH': pH,
        'dissolvedOxygen': dissolvedOxygen,
        'nitrates': nitrates,
        'eColiCount': eColiCount,
        'totalColiforms': totalColiforms,
        'salinity': salinity,
        'recentFlooding': recentFlooding,
        'populationDensity': populationDensity,
        'sanitationIndex': sanitationIndex,
      };

  factory WaterQualityParameters.fromJson(Map<String, dynamic> json) {
    return WaterQualityParameters(
      temperature: json['temperature'] as double,
      turbidity: json['turbidity'] as double,
      pH: json['pH'] as double,
      dissolvedOxygen: json['dissolvedOxygen'] as double,
      nitrates: json['nitrates'] as double,
      eColiCount: json['eColiCount'] as int,
      totalColiforms: json['totalColiforms'] as int,
      salinity: json['salinity'] as double,
      recentFlooding: json['recentFlooding'] as bool,
      populationDensity: json['populationDensity'] as int,
      sanitationIndex: json['sanitationIndex'] as double,
    );
  }
}
