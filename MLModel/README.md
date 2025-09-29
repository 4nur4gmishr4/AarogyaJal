# Water-Borne Disease Prediction System

## Overview

This project implements an advanced machine learning system for predicting water-borne diseases based on IoT sensor data. The system analyzes real-time water quality parameters to provide early warnings and risk assessments for various water-borne diseases.

## Features

- **Real-time IoT Sensor Integration**: Process data from water quality sensors including:
  - pH levels
  - Turbidity
  - Dissolved oxygen
  - Temperature
  - Conductivity
  - Total dissolved solids
  - E. coli count

- **Multi-Disease Prediction**: Detects risk patterns for common water-borne diseases:
  - Cholera
  - Typhoid
  - Hepatitis A
  - Giardiasis
  - Cryptosporidiosis

- **Ensemble ML Model**: Combines multiple algorithms for robust predictions:
  - Random Forest
  - XGBoost
  - Support Vector Machine

- **Real-time Risk Assessment**:
  - Water Quality Index (WQI) calculation
  - Contamination risk scoring
  - Disease-specific risk factor analysis

- **Mobile-Ready API**: RESTful endpoints for seamless mobile integration

## Project Structure

```
ML MODEL/
├── api/
│   └── app.py                  # Flask API implementation
├── models/
│   └── waterborne_disease_predictor.py  # Core ML model
├── utils/
│   └── data_preprocessor.py    # Data preprocessing utilities
├── tests/                      # Test suite
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ML\ MODEL
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the API Server

```bash
python api/app.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### Predict Disease Risk

```
POST /api/predict
```

Example request:
```json
{
  "sensor_data": {
    "ph": 7.2,
    "turbidity": 3.5,
    "dissolved_oxygen": 6.5,
    "temperature": 22.0,
    "conductivity": 400.0,
    "total_dissolved_solids": 300.0,
    "e_coli_count": 10.0
  }
}
```

Example response:
```json
{
  "predictions": {
    "cholera": 0.12,
    "typhoid": 0.08,
    "hepatitis_a": 0.03,
    "giardiasis": 0.05,
    "cryptosporidiosis": 0.02
  },
  "risk_factors": {
    "cholera": ["Elevated temperature indicates risk"]
  },
  "water_quality": {
    "wqi": 82.5,
    "risk_score": 35.0
  },
  "timestamp": "2024-03-06T10:30:00Z"
}
```

#### Train Model

```
POST /api/train
```

Allows updating the model with new training data.

## Model Training

The system uses an ensemble approach combining multiple machine learning algorithms:

1. **Random Forest**: Handles non-linear relationships and feature interactions
2. **XGBoost**: Provides robust predictions through gradient boosting
3. **Support Vector Machine**: Offers additional classification capability

The ensemble weights are optimized for water quality analysis:
- Random Forest: 40%
- XGBoost: 40%
- SVM: 20%

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Smart India Hackathon 2025 for the project opportunity
- Contributors and reviewers who helped improve the system