import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/water_quality_parameters.dart';

class GeminiService {
  static const String apiKey = 'AIzaSyDAb6lZo9wLV0ntHKrQIusl0k-NLktiMcg';
  static const String model = 'gemini-2.5-flash';
  static const String baseUrl =
      'https://generativelanguage.googleapis.com/v1/models';

  static const String _waterQualityContext = '''
Context: Water Quality Analysis System
Focus Areas:
- Water quality parameters and their significance
- Waterborne diseases and their prevention
- Water treatment methods and recommendations
- Public health implications of water quality
- Safety measures and preventive actions
''';

  Future<Map<String, dynamic>> analyzeWaterQuality(
      WaterQualityParameters params) async {
    try {
      final prompt = _buildAnalysisPrompt(params);
      final response = await http.post(
        Uri.parse('$baseUrl/$model:generateText?key=$apiKey'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'contents': [
            {
              'parts': [
                {'text': '$_waterQualityContext\n\n$prompt'}
              ]
            }
          ],
          'generationConfig': {
            'temperature': 0.7,
            'topK': 40,
            'topP': 0.95,
            'maxOutputTokens': 1024,
          },
          'safetySettings': [
            {
              'category': 'HARM_CATEGORY_HARASSMENT',
              'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
            },
            {
              'category': 'HARM_CATEGORY_HATE_SPEECH',
              'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
            },
            {
              'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
              'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
            },
            {
              'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
              'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
            }
          ]
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return _parseAnalysisResponse(data);
      } else {
        throw Exception(
            'Failed to analyze water quality: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error analyzing water quality: $e');
    }
  }

  String _buildAnalysisPrompt(WaterQualityParameters params) {
    return '''
Analyze the following water quality parameters:
- Temperature: ${params.temperature}°C
- Turbidity: ${params.turbidity} NTU
- pH: ${params.pH}
- Dissolved Oxygen: ${params.dissolvedOxygen} mg/L
- Nitrates: ${params.nitrates} mg/L
- E. coli Count: ${params.eColiCount} CFU/100mL
- Total Coliforms: ${params.totalColiforms} CFU/100mL
- Salinity: ${params.salinity} ppt
- Population Density: ${params.populationDensity} people/km²
- Sanitation Index: ${params.sanitationIndex}
- Recent Flooding: ${params.recentFlooding ? 'Yes' : 'No'}

Please provide:
1. Overall water quality assessment
2. Potential health risks and diseases
3. Recommended preventive measures
4. Treatment suggestions
''';
  }

  Map<String, dynamic> _parseAnalysisResponse(Map<String, dynamic> data) {
    final content = data['candidates'][0]['content']['parts'][0]['text'];

    // Parse the response into structured data
    // This is a simplified version - enhance based on actual API response format
    return {
      'analysis': content,
      'timestamp': DateTime.now().toIso8601String(),
    };
  }

  Future<String> getChatbotResponse(String userQuery) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/$model:generateText?key=$apiKey'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'contents': [
            {
              'parts': [
                {
                  'text':
                      '$_waterQualityContext\n\nUser Query: $userQuery\n\nProvide a helpful response focused on water quality and health.'
                }
              ]
            }
          ],
          'generationConfig': {
            'temperature': 0.7,
            'topK': 40,
            'topP': 0.95,
            'maxOutputTokens': 1024,
          }
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['candidates'][0]['content']['parts'][0]['text'];
      } else {
        throw Exception(
            'Failed to get chatbot response: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error getting chatbot response: $e');
    }
  }
}
