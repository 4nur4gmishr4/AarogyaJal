#!/usr/bin/env python3
"""
RESTful API for Water-Borne Disease Prediction System

This module implements the Flask-based API endpoints for the prediction system,
allowing mobile applications to submit IoT sensor data and receive predictions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import numpy as np
import logging
import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_preprocessor import DataPreprocessor
from models.waterborne_disease_predictor import WaterborneDiseasePredictor

app = Flask(__name__)
CORS(app)

# Initialize components
preprocessor = DataPreprocessor()
predictor = WaterborneDiseasePredictor()

# Load trained model
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'models',
    'trained_model.joblib'
)

if os.path.exists(MODEL_PATH):
    predictor.load_model(MODEL_PATH)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Generate predictions from IoT sensor data.
    
    Expected JSON payload:
    {
        "sensor_data": {
            "ph": float,
            "turbidity": float,
            "dissolved_oxygen": float,
            "temperature": float,
            "conductivity": float,
            "total_dissolved_solids": float,
            "e_coli_count": float
        }
    }
    """
    try:
        # Get sensor data from request
        data = request.get_json()
        if not data or 'sensor_data' not in data:
            return jsonify({
                'error': 'Missing sensor_data in request'
            }), 400
        
        sensor_data = data['sensor_data']
        
        # Validate sensor data
        is_valid, errors = preprocessor.validate_sensor_data(sensor_data)
        if not is_valid:
            return jsonify({
                'error': 'Invalid sensor data',
                'details': errors
            }), 400
        
        # Preprocess data
        features = preprocessor.preprocess_sensor_data(sensor_data)
        
        # Generate predictions
        disease_probabilities = predictor.predict_proba(features)
        predictions = predictor.predict(features)
        
        # Get risk factors
        risk_factors = predictor.get_disease_risk_factors(features)
        
        # Calculate water quality metrics
        wqi = preprocessor._calculate_wqi(sensor_data)
        risk_score = preprocessor._calculate_risk_score(sensor_data)
        
        # Prepare response
        response = {
            'predictions': {
                disease: float(prob)
                for disease, prob in zip(predictor.diseases, disease_probabilities[0])
            },
            'risk_factors': risk_factors,
            'water_quality': {
                'wqi': float(wqi),
                'risk_score': float(risk_score)
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Add alerts if necessary
        if risk_score > 70:
            response['alerts'] = [{
                'level': 'high',
                'message': 'High contamination risk detected',
                'recommended_actions': [
                    'Avoid water consumption',
                    'Notify local health authorities',
                    'Increase water quality monitoring frequency'
                ]
            }]
        elif risk_score > 40:
            response['alerts'] = [{
                'level': 'medium',
                'message': 'Moderate contamination risk detected',
                'recommended_actions': [
                    'Monitor water quality closely',
                    'Consider additional water treatment'
                ]
            }]
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

@app.route('/api/train', methods=['POST'])
def train():
    """Train the model with new data.
    
    Expected JSON payload:
    {
        "features": List[List[float]],
        "labels": List[int]
    }
    """
    try:
        data = request.get_json()
        if not data or 'features' not in data or 'labels' not in data:
            return jsonify({
                'error': 'Missing required training data'
            }), 400
        
        # Convert to numpy arrays
        X = np.array(data['features'])
        y = np.array(data['labels'])
        
        # Train model
        metrics = predictor.train(X, y)
        
        # Save updated model
        predictor.save_model(MODEL_PATH)
        
        return jsonify({
            'message': 'Model training completed successfully',
            'metrics': metrics
        })
    
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)