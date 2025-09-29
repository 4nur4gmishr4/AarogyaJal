#!/usr/bin/env python3
"""
Data Preprocessor for Water-Borne Disease Prediction System

This module handles the preprocessing of IoT sensor data for the
water-borne disease prediction system, including feature engineering,
outlier detection, and data validation.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler
from typing import Dict, List, Tuple, Union, Optional
import logging
from sklearn.ensemble import IsolationForest
from datetime import datetime

class DataPreprocessor:
    def __init__(self):
        self.scaler = RobustScaler()  # More robust to outliers than StandardScaler
        self.quality_params = [
            'ph',
            'turbidity',
            'dissolved_oxygen',
            'temperature',
            'conductivity',
            'total_dissolved_solids',
            'e_coli_count'
        ]
        
        # Define normal ranges for water quality parameters
        self.normal_ranges = {
            'ph': (6.5, 8.5),
            'turbidity': (0, 5),  # NTU
            'dissolved_oxygen': (6.0, 8.0),  # mg/L
            'temperature': (20, 25),  # °C
            'conductivity': (100, 2000),  # µS/cm
            'total_dissolved_solids': (0, 1000),  # mg/L
            'e_coli_count': (0, 100)  # CFU/100mL
        }
        
        # Initialize outlier detector
        self.outlier_detector = IsolationForest(
            contamination=0.05,  # Expected proportion of outliers
            random_state=42
        )
        
        # Track data drift metrics
        self.drift_metrics = {
            'last_update': None,
            'param_means': {},
            'param_stds': {},
            'sample_count': 0
        }
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the preprocessor"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def detect_outliers(self, data_batch: List[Dict]) -> List[bool]:
        """Detect outliers in a batch of sensor data using Isolation Forest.
        
        Args:
            data_batch: List of dictionaries containing sensor readings
            
        Returns:
            List of boolean values indicating if each sample is an outlier (True) or not (False)
        """
        if not data_batch:
            return []
            
        # Convert to feature matrix
        features = []
        for data in data_batch:
            sample = [data.get(param, 0) for param in self.quality_params]
            features.append(sample)
        
        features = np.array(features)
        
        # Fit and predict
        # -1 for outliers and 1 for inliers, so we convert to boolean
        predictions = self.outlier_detector.fit_predict(features)
        return [pred == -1 for pred in predictions]
    
    def update_drift_metrics(self, data: Dict):
        """Update data drift metrics with new sensor data.
        
        Args:
            data: Dictionary containing sensor readings
        """
        self.drift_metrics['last_update'] = datetime.now()
        self.drift_metrics['sample_count'] += 1
        
        # Update running statistics for each parameter
        for param in self.quality_params:
            if param in data:
                value = data[param]
                
                # Initialize if first update
                if param not in self.drift_metrics['param_means']:
                    self.drift_metrics['param_means'][param] = value
                    self.drift_metrics['param_stds'][param] = 0
                else:
                    # Update mean and std using Welford's online algorithm
                    old_mean = self.drift_metrics['param_means'][param]
                    old_count = self.drift_metrics['sample_count'] - 1
                    
                    # Update mean
                    new_mean = old_mean + (value - old_mean) / self.drift_metrics['sample_count']
                    
                    # Update variance/std
                    new_var = self.drift_metrics['param_stds'][param]**2
                    new_var += (value - old_mean) * (value - new_mean)
                    
                    self.drift_metrics['param_means'][param] = new_mean
                    self.drift_metrics['param_stds'][param] = np.sqrt(new_var / self.drift_metrics['sample_count'])
    
    def check_data_drift(self, data: Dict, threshold: float = 2.0) -> Dict:
        """Check if new data indicates drift from historical patterns.
        
        Args:
            data: Dictionary containing sensor readings
            threshold: Z-score threshold for drift detection
            
        Returns:
            Dictionary with drift detection results
        """
        if self.drift_metrics['sample_count'] < 30:  # Need sufficient history
            return {'drift_detected': False, 'reason': 'Insufficient historical data'}
        
        drift_params = []
        for param in self.quality_params:
            if param in data and param in self.drift_metrics['param_means']:
                value = data[param]
                mean = self.drift_metrics['param_means'][param]
                std = max(self.drift_metrics['param_stds'][param], 1e-6)  # Avoid division by zero
                
                z_score = abs(value - mean) / std
                if z_score > threshold:
                    drift_params.append({
                        'parameter': param,
                        'value': value,
                        'mean': mean,
                        'std': std,
                        'z_score': z_score
                    })
        
        return {
            'drift_detected': len(drift_params) > 0,
            'drift_parameters': drift_params
        }
        
    def validate_sensor_data(self, data: Dict[str, float]) -> Tuple[bool, List[str]]:
        """Validate IoT sensor data against expected ranges and formats.
        
        Args:
            data: Dictionary containing sensor readings
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Check for required parameters
        for param in self.quality_params:
            if param not in data:
                errors.append(f"Missing required parameter: {param}")
                continue
            
            value = data[param]
            
            # Check for valid numeric values
            if not isinstance(value, (int, float)):
                errors.append(f"Invalid value type for {param}: {type(value)}")
                continue
                
            # Check if within normal range
            min_val, max_val = self.normal_ranges[param]
            if not min_val <= value <= max_val:
                self.logger.warning(
                    f"Parameter {param} outside normal range: {value} "
                    f"(normal: {min_val}-{max_val})"
                )
        
        return len(errors) == 0, errors
    
    def preprocess_sensor_data(self, data: Dict[str, float], location_data: Dict = None, historical_data: List[Dict] = None) -> np.ndarray:
        """Preprocess IoT sensor data for model input.
        
        Args:
            data: Dictionary containing sensor readings
            location_data: Optional dictionary with location information
            historical_data: Optional list of historical readings
            
        Returns:
            Preprocessed feature vector
        """
        # Validate data first
        is_valid, errors = self.validate_sensor_data(data)
        if not is_valid:
            raise ValueError(f"Invalid sensor data: {errors}")
        
        # Create feature vector
        feature_vector = np.array([[data[param] for param in self.quality_params]])
        
        # Scale features
        scaled_features = self.scaler.transform(feature_vector)
        
        # Add engineered features
        engineered_features = self._engineer_features(data, location_data, historical_data)
        
        # Combine scaled and engineered features
        final_features = np.concatenate(
            [scaled_features, engineered_features.reshape(1, -1)],
            axis=1
        )
        
        # Update drift metrics with new data
        self.update_drift_metrics(data)
        
        return final_features
    
    def _engineer_features(self, data: Dict[str, float], location_data: Dict = None, historical_data: List[Dict] = None) -> np.ndarray:
        """Create engineered features from raw sensor data.
        
        Args:
            data: Dictionary containing sensor readings
            location_data: Optional dictionary with location information
            historical_data: Optional list of historical readings
            
        Returns:
            Array of engineered features
        """
        features = []
        
        # Water Quality Index (WQI) calculation
        wqi = self._calculate_wqi(data)
        features.append(wqi)
        
        # pH deviation from neutral (7.0)
        ph_deviation = abs(data['ph'] - 7.0)
        features.append(ph_deviation)
        
        # Contamination risk score
        risk_score = self._calculate_risk_score(data)
        features.append(risk_score)
        
        # Advanced feature engineering
        # 1. Interaction terms between key parameters
        turbidity_ecoli = data.get('turbidity', 0) * data.get('e_coli_count', 0)
        features.append(turbidity_ecoli)
        
        temp_ecoli = data.get('temperature', 20) * data.get('e_coli_count', 0)
        features.append(temp_ecoli)
        
        ph_do_interaction = abs(data.get('ph', 7) - 7) * (8 - data.get('dissolved_oxygen', 8))
        features.append(ph_do_interaction)
        
        # 2. Seasonal factors (if timestamp available)
        if 'timestamp' in data:
            try:
                timestamp = data['timestamp']
                if isinstance(timestamp, str):
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                elif isinstance(timestamp, (int, float)):
                    dt = datetime.fromtimestamp(timestamp)
                else:
                    dt = datetime.now()
                    
                # Month as seasonal indicator (1-12)
                month = dt.month
                # Encode as sin/cos for cyclical feature
                month_sin = np.sin(2 * np.pi * month / 12)
                month_cos = np.cos(2 * np.pi * month / 12)
                features.extend([month_sin, month_cos])
                
                # Is rainy season (simplified - adjust for local climate)
                is_rainy_season = 1.0 if (month >= 6 and month <= 9) else 0.0
                features.append(is_rainy_season)
            except (ValueError, TypeError):
                # Default values if timestamp parsing fails
                features.extend([0.0, 1.0, 0.0])
        else:
            # Default values if no timestamp
            features.extend([0.0, 1.0, 0.0])
        
        # 3. Location-based features
        if location_data:
            # Population density (normalized to 0-1)
            pop_density = min(1.0, location_data.get('population_density', 0) / 10000)
            features.append(pop_density)
            
            # Elevation (normalized to 0-1, assuming 0-3000m range)
            elevation = min(1.0, location_data.get('elevation', 0) / 3000)
            features.append(elevation)
            
            # Distance to water source (normalized to 0-1, assuming 0-100km range)
            dist_to_water = min(1.0, location_data.get('distance_to_water_source', 0) / 100)
            features.append(dist_to_water)
        else:
            # Default values if no location data
            features.extend([0.5, 0.5, 0.5])
        
        # 4. Trend analysis from historical data
        if historical_data and len(historical_data) > 1:
            # Sort by timestamp if available
            if all('timestamp' in d for d in historical_data):
                try:
                    historical_data = sorted(historical_data, key=lambda x: x['timestamp'])
                except (TypeError, ValueError):
                    pass  # Continue with unsorted data if sorting fails
            
            # Calculate trends for key parameters
            for param in ['e_coli_count', 'turbidity', 'ph']:
                # Get last 5 readings or all if fewer
                recent = historical_data[-min(5, len(historical_data)):]
                values = [d.get(param, 0) for d in recent if param in d]
                
                if len(values) > 1:
                    # Simple linear trend (positive = increasing, negative = decreasing)
                    trend = (values[-1] - values[0]) / len(values)
                    # Normalize trend to approximately -1 to 1 range
                    if param == 'e_coli_count':
                        trend = np.tanh(trend / 20)  # Larger changes expected
                    elif param == 'turbidity':
                        trend = np.tanh(trend / 2)   # Moderate changes expected
                    elif param == 'ph':
                        trend = np.tanh(trend)       # Small changes expected
                    
                    features.append(trend)
                else:
                    features.append(0.0)  # No trend if insufficient data
        else:
            # Default values if no historical data
            features.extend([0.0, 0.0, 0.0])
        
        return np.array(features)
    
    def _calculate_wqi(self, data: Dict[str, float]) -> float:
        """Calculate Water Quality Index based on sensor parameters."""
        # Simplified WQI calculation
        weights = {
            'ph': 0.2,
            'turbidity': 0.2,
            'dissolved_oxygen': 0.2,
            'temperature': 0.1,
            'conductivity': 0.1,
            'total_dissolved_solids': 0.1,
            'e_coli_count': 0.1
        }
        
        wqi = 0
        for param, weight in weights.items():
            min_val, max_val = self.normal_ranges[param]
            value = data[param]
            # Normalize to 0-100 scale
            normalized = 100 * (1 - abs(value - np.mean([min_val, max_val])) / 
                               (max_val - min_val))
            wqi += normalized * weight
            
        return wqi
    
    def _calculate_risk_score(self, data: Dict[str, float]) -> float:
        """Calculate overall contamination risk score."""
        # Higher score indicates higher risk
        risk_score = 0
        
        # E. coli presence heavily influences risk
        if data['e_coli_count'] > 0:
            risk_score += 40 * (data['e_coli_count'] / self.normal_ranges['e_coli_count'][1])
        
        # Turbidity contribution
        if data['turbidity'] > self.normal_ranges['turbidity'][1]:
            risk_score += 20 * (data['turbidity'] / self.normal_ranges['turbidity'][1])
        
        # pH deviation contribution
        ph_deviation = abs(data['ph'] - 7.0)
        if ph_deviation > 1:
            risk_score += 20 * (ph_deviation / 7.0)
        
        # Normalize to 0-100
        return min(100, risk_score)