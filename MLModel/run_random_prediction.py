#!/usr/bin/env python3
"""
Run Waterborne Disease Prediction with Random Parameter Values

This script demonstrates the waterborne disease prediction system by generating
random water quality parameters and simulating predictions on them.
"""

import os
import sys
import numpy as np
import random
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import only the preprocessor to avoid TensorFlow dependency
from utils.data_preprocessor import DataPreprocessor


def generate_random_sensor_data(num_samples=1):
    """
    Generate random sensor data within realistic ranges
    
    Args:
        num_samples: Number of samples to generate
        
    Returns:
        List of dictionaries with random sensor data
    """
    data_samples = []
    
    # Define realistic ranges for water quality parameters
    param_ranges = {
        'ph': (5.0, 9.0),
        'turbidity': (0.5, 15.0),
        'dissolved_oxygen': (2.0, 12.0),
        'temperature': (15.0, 35.0),
        'conductivity': (50.0, 2500.0),
        'total_dissolved_solids': (50.0, 1500.0),
        'e_coli_count': (0.0, 500.0)
    }
    
    for _ in range(num_samples):
        sample = {}
        for param, (min_val, max_val) in param_ranges.items():
            sample[param] = round(random.uniform(min_val, max_val), 2)
        data_samples.append(sample)
    
    return data_samples


def generate_random_location_data():
    """
    Generate random location data
    
    Returns:
        Dictionary with random location data
    """
    return {
        'latitude': round(random.uniform(-90, 90), 6),
        'longitude': round(random.uniform(-180, 180), 6),
        'elevation': round(random.uniform(0, 1000), 2),
        'population_density': round(random.uniform(10, 5000), 2),
        'distance_to_water_source': round(random.uniform(0.1, 10), 2)
    }


def generate_random_historical_data(num_days=10):
    """
    Generate random historical data for time-series analysis
    
    Args:
        num_days: Number of days of historical data to generate
        
    Returns:
        Dictionary with historical data
    """
    timestamps = []
    ph_values = []
    turbidity_values = []
    e_coli_values = []
    
    base_date = datetime.now() - timedelta(days=num_days)
    
    for i in range(num_days):
        current_date = base_date + timedelta(days=i)
        timestamps.append(current_date.isoformat())
        ph_values.append(round(random.uniform(6.0, 8.5), 2))
        turbidity_values.append(round(random.uniform(0.5, 10.0), 2))
        e_coli_values.append(round(random.uniform(0, 300), 2))
    
    return {
        'timestamps': timestamps,
        'ph_values': ph_values,
        'turbidity_values': turbidity_values,
        'e_coli_values': e_coli_values
    }


def main():
    print("\n===== Waterborne Disease Prediction with Random Parameters =====\n")
    
    # Initialize components
    preprocessor = DataPreprocessor()
    predictor = WaterborneDiseasePredictor(use_lstm=True)
    
    # Load trained model if available
    model_path = os.path.join('models', 'trained_model.joblib')
    if os.path.exists(model_path):
        print(f"Loading trained model from {model_path}")
        predictor.load_model(model_path)
    else:
        print("No trained model found. Using default model.")
    
    # Generate random data
    print("\nGenerating random sensor data...")
    sensor_data = generate_random_sensor_data(1)[0]
    location_data = generate_random_location_data()
    historical_data = generate_random_historical_data(10)
    
    # Print generated data
    print("\nRandom Sensor Data:")
    for param, value in sensor_data.items():
        print(f"  {param}: {value}")
    
    print("\nRandom Location Data:")
    for param, value in location_data.items():
        print(f"  {param}: {value}")
    
    # Validate sensor data
    print("\nValidating sensor data...")
    is_valid, errors = preprocessor.validate_sensor_data(sensor_data)
    if not is_valid:
        print(f"Validation errors: {errors}")
        return
    
    # Detect outliers
    print("\nChecking for outliers...")
    is_outlier = preprocessor.detect_outliers([sensor_data])[0]
    if is_outlier:
        print("Warning: Outlier detected in sensor data")
    
    # Check for data drift
    print("\nChecking for data drift...")
    drift_result = preprocessor.check_data_drift(sensor_data)
    if drift_result['drift_detected']:
        print("Warning: Data drift detected")
        for param in drift_result['drift_parameters']:
            print(f"  Parameter {param['parameter']} shows drift (z-score: {param['z_score']:.2f})")
    
    # Preprocess data
    print("\nPreprocessing sensor data...")
    processed_data = preprocessor.preprocess_sensor_data(
        sensor_data, location_data, historical_data
    )
    
    # Make predictions
    print("\nGenerating predictions...")
    disease_probs = predictor.predict_proba(processed_data.reshape(1, -1))[0]
    
    # Get risk levels
    risk_levels = predictor.classify_risk_levels(disease_probs)
    risk_names = [predictor.get_risk_level_name(level) for level in risk_levels]
    
    # Get health recommendations
    recommendations = predictor.get_health_recommendations(risk_levels)
    
    # Print results
    print("\nPrediction Results:")
    print("\nDisease Probabilities:")
    for i, disease in enumerate(predictor.diseases):
        print(f"  {disease}: {disease_probs[i]:.4f} - Risk Level: {risk_names[i]}")
    
    print("\nHealth Recommendations:")
    for disease, recommendation in zip(predictor.diseases, recommendations):
        print(f"  {disease}: {recommendation}")


if __name__ == "__main__":
    main()