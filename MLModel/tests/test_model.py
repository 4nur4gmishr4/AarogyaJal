#!/usr/bin/env python3
"""
Test suite for the Water-Borne Disease Prediction System.

This module contains comprehensive tests for data preprocessing,
model prediction, and API functionality.
"""

import json
import numpy as np
import os
import pytest
import sys
from flask import Flask
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_preprocessor import DataPreprocessor
from models.waterborne_disease_predictor import WaterborneDiseasePredictor
from api.app import app

# Test data
VALID_SENSOR_DATA = {
    'ph': 7.2,
    'turbidity': 3.5,
    'dissolved_oxygen': 6.5,
    'temperature': 22.0,
    'conductivity': 400.0,
    'total_dissolved_solids': 300.0,
    'e_coli_count': 10.0
}

INVALID_SENSOR_DATA = {
    'ph': 14.5,  # Invalid pH
    'turbidity': -1.0,  # Invalid turbidity
    'dissolved_oxygen': 6.5,
    'temperature': 22.0,
    'conductivity': 400.0,
    'total_dissolved_solids': 300.0,
    'e_coli_count': 10.0
}

@pytest.fixture
def preprocessor():
    """Create a DataPreprocessor instance for testing."""
    return DataPreprocessor()

@pytest.fixture
def predictor():
    """Create a WaterborneDiseasePredictor instance for testing."""
    return WaterborneDiseasePredictor()

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_data_preprocessor_validation_valid_data(preprocessor):
    """Test data validation with valid sensor data."""
    is_valid, errors = preprocessor.validate_sensor_data(VALID_SENSOR_DATA)
    assert is_valid
    assert not errors

def test_data_preprocessor_validation_invalid_data(preprocessor):
    """Test data validation with invalid sensor data."""
    is_valid, errors = preprocessor.validate_sensor_data(INVALID_SENSOR_DATA)
    assert not is_valid
    assert len(errors) == 2
    assert any('pH' in error for error in errors)
    assert any('turbidity' in error for error in errors)

def test_data_preprocessor_feature_engineering(preprocessor):
    """Test feature engineering from sensor data."""
    features = preprocessor.preprocess_sensor_data(VALID_SENSOR_DATA)
    assert isinstance(features, np.ndarray)
    assert features.shape[1] > len(VALID_SENSOR_DATA)  # Should have engineered features

def test_wqi_calculation(preprocessor):
    """Test Water Quality Index calculation."""
    wqi = preprocessor._calculate_wqi(VALID_SENSOR_DATA)
    assert isinstance(wqi, (float, np.float64))
    assert 0 <= wqi <= 100

def test_risk_score_calculation(preprocessor):
    """Test contamination risk score calculation."""
    risk_score = preprocessor._calculate_risk_score(VALID_SENSOR_DATA)
    assert isinstance(risk_score, (float, np.float64))
    assert 0 <= risk_score <= 100

def test_model_prediction(predictor):
    """Test model prediction functionality."""
    # Create dummy features
    features = np.random.rand(1, 10)
    
    # Test prediction
    predictions = predictor.predict(features)
    assert isinstance(predictions, np.ndarray)
    assert len(predictions.shape) == 1

    # Test probability prediction
    probabilities = predictor.predict_proba(features)
    assert isinstance(probabilities, np.ndarray)
    assert probabilities.shape[1] == len(predictor.diseases)
    assert np.allclose(np.sum(probabilities, axis=1), 1.0)

def test_model_risk_factors(predictor):
    """Test disease risk factor analysis."""
    features = np.random.rand(1, 10)
    risk_factors = predictor.get_disease_risk_factors(features)
    assert isinstance(risk_factors, dict)
    assert all(disease in predictor.diseases for disease in risk_factors.keys())

def test_api_health_check(client):
    """Test API health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data

def test_api_predict_valid_data(client):
    """Test prediction endpoint with valid data."""
    response = client.post('/api/predict',
                         json={'sensor_data': VALID_SENSOR_DATA},
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'predictions' in data
    assert 'water_quality' in data
    assert 'risk_factors' in data
    assert 'timestamp' in data

def test_api_predict_invalid_data(client):
    """Test prediction endpoint with invalid data."""
    response = client.post('/api/predict',
                         json={'sensor_data': INVALID_SENSOR_DATA},
                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'details' in data

def test_api_predict_missing_data(client):
    """Test prediction endpoint with missing data."""
    response = client.post('/api/predict',
                         json={},
                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Missing sensor_data in request' in data['error']

def test_api_train(client):
    """Test model training endpoint."""
    # Mock training data
    training_data = {
        'features': np.random.rand(100, 10).tolist(),
        'labels': np.random.randint(0, 5, 100).tolist()
    }
    
    response = client.post('/api/train',
                         json=training_data,
                         content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'metrics' in data

if __name__ == '__main__':
    pytest.main([__file__])