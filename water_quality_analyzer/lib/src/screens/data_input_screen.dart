import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/water_quality_parameters.dart';
import '../providers/water_quality_provider.dart';
import '../theme/app_theme.dart';
import '../utils/parameter_limits.dart';

class DataInputScreen extends StatefulWidget {
  const DataInputScreen({super.key});

  @override
  State<DataInputScreen> createState() => _DataInputScreenState();
}

class _DataInputScreenState extends State<DataInputScreen> {
  final _formKey = GlobalKey<FormState>();

  final _temperatureController = TextEditingController();
  final _turbidityController = TextEditingController();
  final _phController = TextEditingController();
  final _dissolvedOxygenController = TextEditingController();
  final _nitratesController = TextEditingController();
  final _eColiCountController = TextEditingController();
  final _totalColiformsController = TextEditingController();
  final _salinityController = TextEditingController();
  final _populationDensityController = TextEditingController();
  final _sanitationIndexController = TextEditingController();
  bool _recentFlooding = false;
  final _locationController = TextEditingController();
  final _notesController = TextEditingController();

  @override
  void dispose() {
    _temperatureController.dispose();
    _turbidityController.dispose();
    _phController.dispose();
    _dissolvedOxygenController.dispose();
    _nitratesController.dispose();
    _eColiCountController.dispose();
    _totalColiformsController.dispose();
    _salinityController.dispose();
    _populationDensityController.dispose();
    _sanitationIndexController.dispose();
    _locationController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  String? _validateNumeric(String? value, String fieldName,
      {bool isInteger = false}) {
    if (value == null || value.isEmpty) {
      return '$fieldName is required';
    }

    if (isInteger) {
      final intValue = int.tryParse(value);
      if (intValue == null) {
        return '$fieldName must be a whole number';
      }

      // Check integer limits
      switch (fieldName.toLowerCase()) {
        case 'e. coli count':
          if (intValue < ParameterLimits.eColiCountMin ||
              intValue > ParameterLimits.eColiCountMax) {
            return 'Value must be between ${ParameterLimits.eColiCountMin} and ${ParameterLimits.eColiCountMax}';
          }
        case 'total coliforms':
          if (intValue < ParameterLimits.totalColiformsMin ||
              intValue > ParameterLimits.totalColiformsMax) {
            return 'Value must be between ${ParameterLimits.totalColiformsMin} and ${ParameterLimits.totalColiformsMax}';
          }
        case 'population density':
          if (intValue < ParameterLimits.populationDensityMin ||
              intValue > ParameterLimits.populationDensityMax) {
            return 'Value must be between ${ParameterLimits.populationDensityMin} and ${ParameterLimits.populationDensityMax}';
          }
      }
    } else {
      final doubleValue = double.tryParse(value);
      if (doubleValue == null) {
        return '$fieldName must be a number';
      }

      // Check double limits
      switch (fieldName.toLowerCase()) {
        case 'temperature':
          if (doubleValue < ParameterLimits.temperatureMin ||
              doubleValue > ParameterLimits.temperatureMax) {
            return 'Value must be between ${ParameterLimits.temperatureMin} and ${ParameterLimits.temperatureMax}';
          }
        case 'turbidity':
          if (doubleValue < ParameterLimits.turbidityMin ||
              doubleValue > ParameterLimits.turbidityMax) {
            return 'Value must be between ${ParameterLimits.turbidityMin} and ${ParameterLimits.turbidityMax}';
          }
        case 'ph level':
          if (doubleValue < ParameterLimits.phMin ||
              doubleValue > ParameterLimits.phMax) {
            return 'Value must be between ${ParameterLimits.phMin} and ${ParameterLimits.phMax}';
          }
        case 'dissolved oxygen':
          if (doubleValue < ParameterLimits.dissolvedOxygenMin ||
              doubleValue > ParameterLimits.dissolvedOxygenMax) {
            return 'Value must be between ${ParameterLimits.dissolvedOxygenMin} and ${ParameterLimits.dissolvedOxygenMax}';
          }
        case 'nitrates':
          if (doubleValue < ParameterLimits.nitratesMin ||
              doubleValue > ParameterLimits.nitratesMax) {
            return 'Value must be between ${ParameterLimits.nitratesMin} and ${ParameterLimits.nitratesMax}';
          }
        case 'salinity':
          if (doubleValue < ParameterLimits.salinityMin ||
              doubleValue > ParameterLimits.salinityMax) {
            return 'Value must be between ${ParameterLimits.salinityMin} and ${ParameterLimits.salinityMax}';
          }
        case 'sanitation index':
          if (doubleValue < ParameterLimits.sanitationIndexMin ||
              doubleValue > ParameterLimits.sanitationIndexMax) {
            return 'Value must be between ${ParameterLimits.sanitationIndexMin} and ${ParameterLimits.sanitationIndexMax}';
          }
      }
    }
    return null;
  }

  void _submitForm() async {
    if (_formKey.currentState?.validate() ?? false) {
      final parameters = WaterQualityParameters(
        temperature: double.parse(_temperatureController.text),
        turbidity: double.parse(_turbidityController.text),
        pH: double.parse(_phController.text),
        dissolvedOxygen: double.parse(_dissolvedOxygenController.text),
        nitrates: double.parse(_nitratesController.text),
        eColiCount: int.parse(_eColiCountController.text),
        totalColiforms: int.parse(_totalColiformsController.text),
        salinity: double.parse(_salinityController.text),
        recentFlooding: _recentFlooding,
        populationDensity: int.parse(_populationDensityController.text),
        sanitationIndex: double.parse(_sanitationIndexController.text),
      );

      // First set parameters locally for immediate feedback
      context
          .read<WaterQualityProvider>()
          .setWaterQualityParameters(parameters);

      // Show loading indicator
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Analyzing water quality...'),
          duration: Duration(seconds: 2),
        ),
      );

      try {
        // Send to backend for AI-powered analysis through the provider
        final location = _locationController.text.isNotEmpty
            ? _locationController.text
            : 'Unknown location';
        final notes = _notesController.text;

        await context.read<WaterQualityProvider>().analyzeWithBackend(
              parameters,
              location,
              notes,
            );

        // Show success message
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: const Text('Analysis completed with AI insights'),
              backgroundColor: AppTheme.primaryAccent,
            ),
          );
        }
      } catch (e) {
        // Show error message but keep local analysis
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Backend analysis failed: ${e.toString()}'),
              backgroundColor: Colors.red,
            ),
          );
        }
      }
    }
  }

  Widget _buildTextField({
    required String label,
    required TextEditingController controller,
    required String unit,
    bool isInteger = false,
    String? helperText,
  }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: TextFormField(
        controller: controller,
        keyboardType: const TextInputType.numberWithOptions(decimal: true),
        decoration: InputDecoration(
          labelText: label,
          helperText: helperText,
          suffixText: unit,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
          ),
        ),
        validator: (value) =>
            _validateNumeric(value, label, isInteger: isInteger),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Water Quality Parameters'),
        elevation: 2,
        backgroundColor: const Color(0xFF3900B3),
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.of(context).pop(),
          color: Colors.white,
        ),
      ),
      body: Form(
        key: _formKey,
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildTextField(
                label: 'Temperature',
                controller: _temperatureController,
                unit: '°C',
                helperText: ParameterLimits.getHelperText('temperature'),
              ),
              _buildTextField(
                label: 'Turbidity',
                controller: _turbidityController,
                unit: 'NTU',
                helperText: ParameterLimits.getHelperText('turbidity'),
              ),
              _buildTextField(
                label: 'pH Level',
                controller: _phController,
                unit: 'pH',
                helperText: ParameterLimits.getHelperText('ph'),
              ),
              _buildTextField(
                label: 'Dissolved Oxygen',
                controller: _dissolvedOxygenController,
                unit: 'mg/L',
                helperText: ParameterLimits.getHelperText('dissolved oxygen'),
              ),
              _buildTextField(
                label: 'Nitrates',
                controller: _nitratesController,
                unit: 'mg/L',
                helperText: ParameterLimits.getHelperText('nitrates'),
              ),
              _buildTextField(
                label: 'E. coli Count',
                controller: _eColiCountController,
                unit: 'CFU/100ml',
                isInteger: true,
                helperText: ParameterLimits.getHelperText('e.coli'),
              ),
              _buildTextField(
                label: 'Total Coliforms',
                controller: _totalColiformsController,
                unit: 'CFU/100ml',
                isInteger: true,
                helperText: ParameterLimits.getHelperText('total coliforms'),
              ),
              _buildTextField(
                label: 'Salinity',
                controller: _salinityController,
                unit: 'mg/L',
                helperText: ParameterLimits.getHelperText('salinity'),
              ),
              _buildTextField(
                label: 'Population Density',
                controller: _populationDensityController,
                unit: 'per km²',
                isInteger: true,
                helperText: ParameterLimits.getHelperText('population density'),
              ),
              _buildTextField(
                label: 'Sanitation Index',
                controller: _sanitationIndexController,
                unit: '',
                helperText: ParameterLimits.getHelperText('sanitation index'),
              ),
              SwitchListTile(
                title: const Text('Recent Flooding'),
                subtitle:
                    const Text('Has there been flooding in the past 30 days?'),
                value: _recentFlooding,
                onChanged: (bool value) {
                  setState(() {
                    _recentFlooding = value;
                  });
                },
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _locationController,
                decoration: InputDecoration(
                  labelText: 'Location',
                  hintText: 'e.g., Village name, GPS coordinates',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _notesController,
                decoration: InputDecoration(
                  labelText: 'Additional Notes',
                  hintText: 'Any other relevant information',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                maxLines: 3,
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _submitForm,
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppTheme.primaryAccent,
                  padding: const EdgeInsets.all(16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: const Text(
                  'Calculate Risk Assessment',
                  style: TextStyle(fontSize: 16),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
