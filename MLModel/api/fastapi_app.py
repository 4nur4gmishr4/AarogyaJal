#!/usr/bin/env python3
"""
RESTful API for Water-Borne Disease Prediction System using FastAPI

This module implements the FastAPI-based API endpoints for the prediction system,
allowing mobile applications to submit IoT sensor data and receive predictions with
robust input validation and error handling.
"""

import os
import sys
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

import numpy as np
from fastapi import FastAPI, HTTPException, Depends, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validator, root_validator

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_preprocessor import DataPreprocessor
from models.waterborne_disease_predictor import WaterborneDiseasePredictor

# Initialize FastAPI app
app = FastAPI(
    title="Water-Borne Disease Prediction API",
    description="API for predicting water-borne diseases from IoT sensor data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
preprocessor = DataPreprocessor()
predictor = WaterborneDiseasePredictor(use_lstm=True)

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

# Pydantic models for request/response validation
class SensorData(BaseModel):
    """Model for IoT sensor data validation"""
    ph: float = Field(..., ge=0, le=14, description="pH level (0-14)")
    turbidity: float = Field(..., ge=0, description="Turbidity in NTU")
    dissolved_oxygen: float = Field(..., ge=0, description="Dissolved oxygen in mg/L")
    temperature: float = Field(..., description="Water temperature in Celsius")
    conductivity: float = Field(..., ge=0, description="Electrical conductivity in μS/cm")
    total_dissolved_solids: float = Field(..., ge=0, description="TDS in mg/L")
    e_coli_count: float = Field(..., ge=0, description="E. coli count in CFU/100mL")
    
    @validator('temperature')
    def validate_temperature(cls, v):
        if v < -10 or v > 50:  # Reasonable range for water temperature
            raise ValueError("Temperature must be between -10°C and 50°C")
        return v

class LocationData(BaseModel):
    """Optional location data for enhanced predictions"""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    elevation: Optional[float] = None
    population_density: Optional[float] = None
    distance_to_water_source: Optional[float] = None

class HistoricalData(BaseModel):
    """Optional historical data for time-series analysis"""
    timestamps: List[str]
    ph_values: List[float]
    turbidity_values: List[float]
    e_coli_values: List[float]
    
    @validator('timestamps')
    def validate_timestamps(cls, v):
        if len(v) < 2:
            raise ValueError("At least 2 historical data points are required")
        return v
    
    @root_validator
    def validate_lists_length(cls, values):
        timestamps = values.get('timestamps', [])
        for field in ['ph_values', 'turbidity_values', 'e_coli_values']:
            if len(values.get(field, [])) != len(timestamps):
                raise ValueError(f"{field} must have the same length as timestamps")
        return values

class PredictionRequest(BaseModel):
    """Model for prediction request validation"""
    sensor_data: SensorData
    location_data: Optional[LocationData] = None
    historical_data: Optional[HistoricalData] = None

class Alert(BaseModel):
    """Model for alert information"""
    level: str
    message: str
    recommended_actions: List[str]

class WaterQuality(BaseModel):
    """Model for water quality metrics"""
    wqi: float
    risk_score: float

class PredictionResponse(BaseModel):
    """Model for prediction response validation"""
    predictions: Dict[str, float]
    risk_factors: Dict[str, List[str]]
    risk_level: str
    health_recommendations: List[str]
    water_quality: WaterQuality
    alerts: Optional[List[Alert]] = None
    timestamp: str

class TrainingData(BaseModel):
    """Model for training data validation"""
    features: List[List[float]]
    labels: List[int]
    
    @validator('labels')
    def validate_labels(cls, v, values):
        if 'features' in values and len(values['features']) != len(v):
            raise ValueError("Number of labels must match number of feature rows")
        return v

class TrainingResponse(BaseModel):
    """Model for training response validation"""
    message: str
    metrics: Dict[str, Any]

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(request: PredictionRequest):
    """Generate predictions from IoT sensor data"""
    try:
        # Extract sensor data
        sensor_data = request.sensor_data.dict()
        
        # Extract optional data if provided
        location_data = request.location_data.dict() if request.location_data else None
        historical_data = request.historical_data.dict() if request.historical_data else None
        
        # Preprocess data
        features = preprocessor.preprocess_sensor_data(
            sensor_data, 
            location_data=location_data, 
            historical_data=historical_data
        )
        
        # Check for outliers
        is_outlier = preprocessor.detect_outliers(features)
        if is_outlier.any():
            logger.warning(f"Outliers detected in input data: {is_outlier}")
        
        # Update drift metrics
        preprocessor.update_drift_metrics(features)
        
        # Check for data drift
        drift_detected, drift_metrics = preprocessor.check_data_drift()
        if drift_detected:
            logger.warning(f"Data drift detected: {drift_metrics}")
        
        # Generate predictions
        disease_probabilities = predictor.predict_proba(features)
        predictions = predictor.predict(features)
        risk_level_index = predictor.predict(features, return_risk_levels=True)[0]
        
        # Get risk factors and recommendations
        risk_factors = predictor.get_disease_risk_factors(features)
        risk_level_name = predictor.get_risk_level_name(risk_level_index)
        health_recommendations = predictor.get_health_recommendations(risk_level_index)
        
        # Calculate water quality metrics
        wqi = preprocessor._calculate_wqi(sensor_data)
        risk_score = preprocessor._calculate_risk_score(sensor_data)
        
        # Prepare response
        response = {
            "predictions": {
                disease: float(prob)
                for disease, prob in zip(predictor.diseases, disease_probabilities[0])
            },
            "risk_factors": risk_factors,
            "risk_level": risk_level_name,
            "health_recommendations": health_recommendations,
            "water_quality": {
                "wqi": float(wqi),
                "risk_score": float(risk_score)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        # Add alerts if necessary
        alerts = []
        if risk_score > 70:
            alerts.append({
                "level": "high",
                "message": "High contamination risk detected",
                "recommended_actions": [
                    "Avoid water consumption",
                    "Notify local health authorities",
                    "Increase water quality monitoring frequency"
                ]
            })
        elif risk_score > 40:
            alerts.append({
                "level": "medium",
                "message": "Moderate contamination risk detected",
                "recommended_actions": [
                    "Monitor water quality closely",
                    "Consider additional water treatment"
                ]
            })
        
        if drift_detected:
            alerts.append({
                "level": "warning",
                "message": "Data drift detected - model may need retraining",
                "recommended_actions": [
                    "Collect additional training data",
                    "Validate sensor calibration",
                    "Consider model retraining"
                ]
            })
        
        if alerts:
            response["alerts"] = alerts
        
        return response
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/train", response_model=TrainingResponse, tags=["Training"])
async def train(data: TrainingData):
    """Train the model with new data"""
    try:
        # Convert to numpy arrays
        X = np.array(data.features)
        y = np.array(data.labels)
        
        # Train model
        metrics = predictor.train(X, y)
        
        # Save updated model
        predictor.save_model(MODEL_PATH)
        
        return {
            "message": "Model training completed successfully",
            "metrics": metrics
        }
    
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    
    except Exception as e:
        logger.error(f"Error training model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/model/info", tags=["Model"])
async def model_info():
    """Get information about the current model"""
    return {
        "model_type": "Ensemble (Random Forest, XGBoost, SVM, LSTM)",
        "diseases": predictor.diseases,
        "risk_levels": predictor.risk_levels,
        "last_training_date": predictor.last_training_date,
        "feature_importance": {
            f"feature_{i}": float(importance) 
            for i, importance in enumerate(predictor.feature_importance)
        } if hasattr(predictor, 'feature_importance') and predictor.feature_importance is not None else {}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=True)