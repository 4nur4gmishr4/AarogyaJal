import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/water_quality_parameters.dart';

class BackendService {
  // Base URL for the Python backend API
  static const String baseUrl = 'http://localhost:8000'; // For web or iOS simulator. Using localhost for Windows development.
  // Use 'http://localhost:8000' for web or iOS simulator
  
  /// Get a response from the chatbot
  Future<String> getChatbotResponse(String userQuery) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'query': userQuery,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['response'];
      } else {
        throw Exception(
            'Failed to get chatbot response: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error getting chatbot response: $e');
    }
  }

  /// Analyze water quality parameters
  Future<Map<String, dynamic>> analyzeWaterQuality(
      WaterQualityParameters parameters, String location, String notes) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/analyze'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'parameters': parameters.toJson(),
          'location': location,
          'notes': notes,
        }),
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        throw Exception(
            'Failed to analyze water quality: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error analyzing water quality: $e');
    }
  }
}