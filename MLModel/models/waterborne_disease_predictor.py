#!/usr/bin/env python3
"""
Water-Borne Disease Predictor Model

This module implements an enhanced ensemble model for predicting water-borne diseases
based on water quality parameters from IoT sensors. It combines Random Forest, LSTM,
XGBoost, and SVM classifiers for robust predictions with time-series capabilities.
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model, save_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_recall_curve
from typing import Dict, List, Tuple, Union, Optional, Any
import joblib
import logging
import os
import shap
from datetime import datetime

class WaterborneDiseasePredictor:
    def __init__(self, use_lstm: bool = True):
        """
        Initialize the Waterborne Disease Predictor with an ensemble of models.
        
        Args:
            use_lstm: Whether to include LSTM in the ensemble (requires time-series data)
        """
        self.diseases = [
            'cholera',
            'typhoid',
            'hepatitis_a',
            'giardiasis',
            'cryptosporidiosis'
        ]
        
        self.risk_levels = [
            'low',
            'medium',
            'high',
            'critical'
        ]
        
        # Initialize base models
        self.rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            bootstrap=True,
            class_weight='balanced',
            random_state=42
        )
        
        self.xgb_model = XGBClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            gamma=1,
            reg_alpha=0.1,
            reg_lambda=1,
            scale_pos_weight=2,
            random_state=42
        )
        
        self.svm_model = SVC(
            kernel='rbf',
            C=10,
            gamma='scale',
            probability=True,
            class_weight='balanced',
            random_state=42
        )
        
        # LSTM model for time-series analysis
        self.use_lstm = use_lstm
        self.lstm_model = None
        self.lstm_timesteps = 5  # Default lookback window
        self.lstm_features = None  # Will be set during training
        
        # Model collection and weights
        self.models = {
            'random_forest': self.rf_model,
            'xgboost': self.xgb_model,
            'svm': self.svm_model
        }
        
        # Default weights (will be optimized during training)
        self.model_weights = {
            'random_forest': 0.35,
            'xgboost': 0.35,
            'svm': 0.10,
            'lstm': 0.20  # Only used if LSTM is enabled
        }
        
        # Model performance tracking
        self.model_performance = {}
        self.feature_importance = {}
        self.last_training_date = None
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure logging for the model"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _build_lstm_model(self, input_shape: Tuple[int, int]) -> Sequential:
        """Build and compile LSTM model for time-series prediction.
        
        Args:
            input_shape: Shape of input data (timesteps, features)
            
        Returns:
            Compiled Keras LSTM model
        """
        model = Sequential([
            LSTM(64, input_shape=input_shape, return_sequences=True),
            BatchNormalization(),
            Dropout(0.2),
            LSTM(32),
            BatchNormalization(),
            Dropout(0.2),
            Dense(16, activation='relu'),
            BatchNormalization(),
            Dense(len(self.diseases), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def _prepare_lstm_sequences(self, X: np.ndarray, y: np.ndarray = None) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """Prepare time-series sequences for LSTM model.
        
        Args:
            X: Feature matrix
            y: Optional target labels
            
        Returns:
            Tuple of (X_sequences, y_sequences) where y_sequences may be None
        """
        # Store feature dimension for future use
        if self.lstm_features is None:
            self.lstm_features = X.shape[1]
        
        # Create sequences
        sequences_X = []
        sequences_y = [] if y is not None else None
        
        # For each possible sequence in the dataset
        for i in range(len(X) - self.lstm_timesteps + 1):
            # Extract sequence
            seq = X[i:i+self.lstm_timesteps]
            sequences_X.append(seq)
            
            # If we have labels, use the label of the last timestep in sequence
            if y is not None:
                sequences_y.append(y[i+self.lstm_timesteps-1])
        
        if len(sequences_X) == 0:  # Handle case with insufficient data
            if y is not None:
                return np.empty((0, self.lstm_timesteps, self.lstm_features)), np.empty(0)
            return np.empty((0, self.lstm_timesteps, self.lstm_features)), None
        
        # Convert to numpy arrays
        X_seq = np.array(sequences_X)
        y_seq = np.array(sequences_y) if sequences_y else None
        
        return X_seq, y_seq
    
    def train(self, X: np.ndarray, y: np.ndarray, validation_method: str = 'kfold', 
              n_splits: int = 5, location_groups: List = None, 
              time_groups: List = None) -> Dict[str, Any]:
        """Train the ensemble model with advanced validation options.
        
        Args:
            X: Feature matrix
            y: Target labels
            validation_method: One of 'kfold', 'stratified', 'geographic', 'temporal'
            n_splits: Number of splits for cross-validation
            location_groups: Location identifiers for geographic validation
            time_groups: Time period identifiers for temporal validation
            
        Returns:
            Dictionary containing model performance metrics
        """
        self.last_training_date = datetime.now()
        self.logger.info(f"Starting model training with {validation_method} validation")
        
        # Initialize metrics collection
        all_metrics = {
            'accuracy': [],
            'precision': [],
            'recall': [],
            'f1': [],
            'auc': [],
            'confusion_matrices': []
        }
        
        # Set up cross-validation strategy
        if validation_method == 'kfold':
            cv = KFold(n_splits=n_splits, shuffle=True, random_state=42)
            splits = cv.split(X, y)
        elif validation_method == 'stratified':
            cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
            splits = cv.split(X, y)
        elif validation_method == 'geographic' and location_groups is not None:
            # Leave-one-group-out for geographic validation
            unique_locations = np.unique(location_groups)
            splits = [(np.where(location_groups != loc)[0], np.where(location_groups == loc)[0]) 
                     for loc in unique_locations]
        elif validation_method == 'temporal' and time_groups is not None:
            # Forward chaining for temporal validation
            unique_times = np.sort(np.unique(time_groups))
            splits = []
            for i in range(len(unique_times) - 1):
                train_idx = np.where(time_groups <= unique_times[i])[0]
                test_idx = np.where(time_groups == unique_times[i+1])[0]
                splits.append((train_idx, test_idx))
        else:
            # Default to simple train/test split
            train_idx, test_idx = train_test_split(
                np.arange(len(X)), test_size=0.2, random_state=42, stratify=y
            )
            splits = [(train_idx, test_idx)]
        
        # Perform cross-validation
        fold = 1
        for train_idx, test_idx in splits:
            self.logger.info(f"Training fold {fold}/{len(list(splits))}")
            
            # Split data
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Train traditional ML models
            for name, model in self.models.items():
                self.logger.info(f"Training {name} model...")
                model.fit(X_train, y_train)
            
            # Train LSTM if enabled and we have enough data
            if self.use_lstm and len(X_train) > self.lstm_timesteps:
                self.logger.info("Training LSTM model...")
                # Prepare sequences
                X_train_seq, y_train_seq = self._prepare_lstm_sequences(X_train, y_train)
                
                if len(X_train_seq) > 0:  # Only train if we have sequences
                    # Build and train LSTM model
                    self.lstm_model = self._build_lstm_model((self.lstm_timesteps, X_train.shape[1]))
                    self.lstm_model.fit(
                        X_train_seq, y_train_seq,
                        epochs=50,
                        batch_size=32,
                        validation_split=0.2,
                        verbose=0,
                        callbacks=[tf.keras.callbacks.EarlyStopping(
                            monitor='val_loss', patience=5, restore_best_weights=True
                        )]
                    )
            
            # Evaluate ensemble
            y_pred = self.predict(X_test)
            y_proba = self.predict_proba(X_test)
            
            # Calculate metrics
            report = classification_report(y_test, y_pred, output_dict=True)
            cm = confusion_matrix(y_test, y_pred)
            
            # Calculate AUC for each class and average
            auc_scores = []
            for i in range(len(self.diseases)):
                if len(np.unique(y_test)) > 1:  # Only calculate if we have multiple classes
                    # One-vs-rest AUC
                    y_true_binary = (y_test == i).astype(int)
                    y_score = y_proba[:, i]
                    try:
                        auc = roc_auc_score(y_true_binary, y_score)
                        auc_scores.append(auc)
                    except ValueError:
                        # Handle case where a class might not be present
                        pass
            
            # Store metrics for this fold
            all_metrics['accuracy'].append(report['accuracy'])
            all_metrics['precision'].append(np.mean([report[str(i)]['precision'] for i in range(len(self.diseases)) if str(i) in report]))
            all_metrics['recall'].append(np.mean([report[str(i)]['recall'] for i in range(len(self.diseases)) if str(i) in report]))
            all_metrics['f1'].append(np.mean([report[str(i)]['f1-score'] for i in range(len(self.diseases)) if str(i) in report]))
            all_metrics['auc'].append(np.mean(auc_scores) if auc_scores else 0)
            all_metrics['confusion_matrices'].append(cm)
            
            # Calculate feature importance for this fold
            self._calculate_feature_importance(X_train, y_train)
            
            fold += 1
        
        # Calculate confidence intervals
        metrics = {}
        for metric_name in ['accuracy', 'precision', 'recall', 'f1', 'auc']:
            values = all_metrics[metric_name]
            metrics[metric_name] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'ci_lower': np.percentile(values, 2.5),
                'ci_upper': np.percentile(values, 97.5)
            }
        
        # Average confusion matrix
        metrics['confusion_matrix'] = np.mean(all_metrics['confusion_matrices'], axis=0)
        
        # Store performance metrics
        self.model_performance = metrics
        
        # Log results
        self.logger.info("Model training completed")
        self.logger.info(f"Accuracy: {metrics['accuracy']['mean']:.4f} ± {metrics['accuracy']['std']:.4f}")
        self.logger.info(f"Precision: {metrics['precision']['mean']:.4f} ± {metrics['precision']['std']:.4f}")
        self.logger.info(f"Recall: {metrics['recall']['mean']:.4f} ± {metrics['recall']['std']:.4f}")
        self.logger.info(f"F1 Score: {metrics['f1']['mean']:.4f} ± {metrics['f1']['std']:.4f}")
        self.logger.info(f"AUC: {metrics['auc']['mean']:.4f} ± {metrics['auc']['std']:.4f}")
        
        return metrics
    
    def _calculate_feature_importance(self, X: np.ndarray, y: np.ndarray):
        """Calculate and store feature importance from tree-based models.
        
        Args:
            X: Feature matrix
            y: Target labels
        """
        # Get feature importance from Random Forest
        rf_importance = self.rf_model.feature_importances_
        
        # Get feature importance from XGBoost
        xgb_importance = self.xgb_model.feature_importances_
        
        # Average the importances
        avg_importance = (rf_importance + xgb_importance) / 2
        
        # Store or update feature importance
        if not self.feature_importance:
            self.feature_importance = avg_importance
        else:
            self.feature_importance = (self.feature_importance + avg_importance) / 2
        
        self.logger.info("Model training completed")
        self.logger.info(f"Classification Report:\n{metrics['classification_report']}")
        
        return metrics
    
    def predict(self, X: np.ndarray, return_risk_levels: bool = False) -> np.ndarray:
        """Generate predictions using the ensemble model.
        
        Args:
            X: Feature matrix
            return_risk_levels: If True, return risk levels instead of disease labels
            
        Returns:
            Array of predicted disease labels or risk levels
        """
        # Get probability predictions
        proba = self.predict_proba(X)
        
        # Get disease predictions
        disease_predictions = np.argmax(proba, axis=1)
        
        if return_risk_levels:
            # Convert probabilities to risk levels
            risk_levels = self.classify_risk_levels(proba)
            return risk_levels
        
        return disease_predictions
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Generate probability predictions for each disease.
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of prediction probabilities for each disease
        """
        predictions = {}
        
        # Get probability predictions from traditional ML models
        for name, model in self.models.items():
            predictions[name] = model.predict_proba(X)
        
        # Get LSTM predictions if available
        if self.use_lstm and self.lstm_model is not None and len(X) >= self.lstm_timesteps:
            # Prepare sequences for LSTM
            X_seq, _ = self._prepare_lstm_sequences(X)
            
            if len(X_seq) > 0:  # Only predict if we have sequences
                lstm_pred = self.lstm_model.predict(X_seq)
                
                # For samples without enough history, use the prediction for the first valid sequence
                lstm_full = np.zeros((len(X), lstm_pred.shape[1]))
                
                # Fill predictions where we have them
                valid_indices = np.arange(self.lstm_timesteps - 1, len(X))
                lstm_full[valid_indices[:len(lstm_pred)]] = lstm_pred
                
                # Fill missing predictions with the first valid prediction
                if len(lstm_pred) > 0:
                    for i in range(self.lstm_timesteps - 1):
                        lstm_full[i] = lstm_pred[0]
                
                predictions['lstm'] = lstm_full
        
        # Weighted ensemble probabilities
        ensemble_proba = np.zeros_like(predictions['random_forest'])
        total_weight = 0
        
        for name, pred in predictions.items():
            if name in self.model_weights:
                weight = self.model_weights[name]
                ensemble_proba += pred * weight
                total_weight += weight
        
        # Normalize by actual weights used
        if total_weight > 0:
            ensemble_proba /= total_weight
        
        return ensemble_proba
    
    def classify_risk_levels(self, probabilities: np.ndarray) -> np.ndarray:
        """Classify risk levels based on prediction probabilities.
        
        Args:
            probabilities: Array of prediction probabilities
            
        Returns:
            Array of risk level indices (0=low, 1=medium, 2=high, 3=critical)
        """
        # Define thresholds for risk levels
        # These can be adjusted based on domain knowledge and requirements
        thresholds = {
            'low': 0.25,      # 0-25% probability
            'medium': 0.50,   # 25-50% probability
            'high': 0.75,     # 50-75% probability
            'critical': 1.0   # 75-100% probability
        }
        
        # Get maximum probability for each sample
        max_proba = np.max(probabilities, axis=1)
        
        # Classify risk levels
        risk_levels = np.zeros(len(max_proba), dtype=int)
        
        # Low risk (default)
        risk_levels[:] = 0
        
        # Medium risk
        risk_levels[max_proba >= thresholds['low']] = 1
        
        # High risk
        risk_levels[max_proba >= thresholds['medium']] = 2
        
        # Critical risk
        risk_levels[max_proba >= thresholds['high']] = 3
        
        return risk_levels
    
    def get_risk_level_name(self, risk_level: int) -> str:
        """Get the name of a risk level.
        
        Args:
            risk_level: Risk level index (0-3)
            
        Returns:
            Risk level name
        """
        if 0 <= risk_level < len(self.risk_levels):
            return self.risk_levels[risk_level]
        return "unknown"
    
    def get_health_recommendations(self, risk_level: int) -> List[str]:
        """Get health recommendations based on risk level.
        
        Args:
            risk_level: Risk level index (0-3)
            
        Returns:
            List of health recommendation strings
        """
        recommendations = {
            0: [  # Low risk
                "Water is generally safe for consumption.",
                "Continue regular monitoring of water quality.",
                "Follow standard hygiene practices."
            ],
            1: [  # Medium risk
                "Consider boiling water before consumption.",
                "Use water filters certified for bacteria removal.",
                "Avoid consuming raw vegetables washed with this water.",
                "Increase frequency of water quality monitoring."
            ],
            2: [  # High risk
                "Boil water vigorously for at least 1 minute before consumption.",
                "Use bottled water for drinking and cooking.",
                "Avoid contact with water during bathing or washing.",
                "Alert local health authorities about potential contamination.",
                "Consider water treatment with chlorine or iodine tablets."
            ],
            3: [  # Critical risk
                "DO NOT consume or use this water without treatment.",
                "Use only bottled water for drinking, cooking, and hygiene.",
                "Immediately notify health authorities and water management.",
                "Seek medical attention if experiencing gastrointestinal symptoms.",
                "Implement emergency water treatment protocols.",
                "Consider evacuation if alternative water sources are unavailable."
            ]
        }
        
        if 0 <= risk_level < len(self.risk_levels):
            return recommendations[risk_level]
        return ["No specific recommendations available."]
    
    def save_model(self, path: str):
        """Save the trained model to disk.
        
        Args:
            path: Path to save the model
        """
        model_data = {
            'models': self.models,
            'weights': self.model_weights,
            'diseases': self.diseases
        }
        joblib.dump(model_data, path)
        self.logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load a trained model from disk.
        
        Args:
            path: Path to the saved model
        """
        model_data = joblib.load(path)
        self.models = model_data['models']
        self.model_weights = model_data['weights']
        self.diseases = model_data['diseases']
        self.logger.info(f"Model loaded from {path}")
    
    def get_disease_risk_factors(self, X: np.ndarray) -> Dict[str, List[str]]:
        """Analyze risk factors for predicted diseases.
        
        Args:
            X: Feature matrix
            
        Returns:
            Dictionary mapping diseases to their risk factors
        """
        predictions = self.predict(X)
        probabilities = self.predict_proba(X)
        
        risk_factors = {}
        for i, disease in enumerate(self.diseases):
            if predictions[i] == 1:  # If disease is predicted
                risk_factors[disease] = self._analyze_risk_factors(
                    X[i],
                    probabilities[i][1],
                    disease
                )
        
        return risk_factors
    
    def _analyze_risk_factors(self, features: np.ndarray, probability: float,
                            disease: str) -> List[str]:
        """Analyze specific risk factors for a disease prediction.
        
        Args:
            features: Single sample feature vector
            probability: Prediction probability
            disease: Disease name
            
        Returns:
            List of risk factor descriptions
        """
        risk_factors = []
        
        # Define disease-specific thresholds
        thresholds = {
            'cholera': {
                'ph': (6.0, 8.0),
                'temperature': (30, 40)
            },
            'typhoid': {
                'e_coli_count': (50, float('inf')),
                'turbidity': (5, float('inf'))
            },
            'hepatitis_a': {
                'e_coli_count': (100, float('inf')),
                'ph': (5.0, 6.0)
            },
            'giardiasis': {
                'turbidity': (10, float('inf')),
                'temperature': (25, 35)
            },
            'cryptosporidiosis': {
                'turbidity': (15, float('inf')),
                'ph': (6.0, 7.0)
            }
        }
        
        # Check disease-specific conditions
        if disease in thresholds:
            for param, (min_val, max_val) in thresholds[disease].items():
                param_idx = self.quality_params.index(param)
                value = features[param_idx]
                if min_val <= value <= max_val:
                    risk_factors.append(
                        f"Elevated {param} level ({value:.2f}) "
                        f"indicates {disease} risk"
                    )
        
        return risk_factors