class ParameterLimits {
  static const phMin = 0.0;
  static const phMax = 14.0;

  static const temperatureMin = 0.0;
  static const temperatureMax = 50.0;

  static const turbidityMin = 0.0;
  static const turbidityMax = 40.0;

  static const dissolvedOxygenMin = 0.0;
  static const dissolvedOxygenMax = 15.0;

  static const nitratesMin = 0.0;
  static const nitratesMax = 50.0;

  static const eColiCountMin = 0;
  static const eColiCountMax = 1000;

  static const totalColiformsMin = 0;
  static const totalColiformsMax = 1000;

  static const salinityMin = 0.0;
  static const salinityMax = 1000.0;

  static const populationDensityMin = 0;
  static const populationDensityMax = 50000;

  static const sanitationIndexMin = 0.0;
  static const sanitationIndexMax = 1.0;

  static String getHelperText(String parameter) {
    switch (parameter.toLowerCase()) {
      case 'ph':
        return 'Range: 0-14';
      case 'temperature':
        return 'Range: 0-50°C';
      case 'turbidity':
        return 'Range: 0-40 NTU';
      case 'dissolved oxygen':
        return 'Range: 0-15 mg/L';
      case 'nitrates':
        return 'Range: 0-50 mg/L';
      case 'e.coli':
        return 'Range: 0-1000 CFU/100ml';
      case 'total coliforms':
        return 'Range: 0-1000 CFU/100ml';
      case 'salinity':
        return 'Range: 0-1000 mg/L';
      case 'population density':
        return 'Range: 0-50000 per km²';
      case 'sanitation index':
        return 'Range: 0-1';
      default:
        return '';
    }
  }
}
