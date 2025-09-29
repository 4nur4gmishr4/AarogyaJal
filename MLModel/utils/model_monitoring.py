#!/usr/bin/env python3
"""
Model Monitoring and Retraining Pipeline

This module implements data drift detection and automated model retraining
to ensure the prediction system maintains accuracy over time as data patterns change.
"""

import numpy as np
import pandas as pd
import joblib
import os
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Union, Optional, Any

class ModelMonitor:
    def __init__(self, model_path: str, drift_threshold: float = 0.05, 
                 retraining_interval_days: int = 30):
        """
        Initialize the model monitoring system.
        
        Args:
            model_path: Path to the trained model file
            drift_threshold: Threshold for data drift detection
            retraining_interval_days: Minimum days between retraining
        """
        self.model_path = model_path
        self.drift_threshold = drift_threshold
        self.retraining_interval_days = retraining_interval_days
        
        # Initialize monitoring metrics
        self.metrics_history = []
        self.drift_scores = {}
        self.last_retraining_date = None
        self.performance_history = []
        
        # Data collection for retraining
        self.new_data_features = []
        self.new_data_labels = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load monitoring history if exists
        self._load_monitoring_history()
    
    def _load_monitoring_history(self):
        """
        Load monitoring history from disk if available.
        """
        history_path = os.path.join(os.path.dirname(self.model_path), 'monitoring_history.json')
        if os.path.exists(history_path):
            try:
                with open(history_path, 'r') as f:
                    history = json.load(f)
                    
                self.metrics_history = history.get('metrics_history', [])
                self.drift_scores = history.get('drift_scores', {})
                self.last_retraining_date = history.get('last_retraining_date')
                self.performance_history = history.get('performance_history', [])
                
                self.logger.info(f"Loaded monitoring history with {len(self.metrics_history)} records")
            except Exception as e:
                self.logger.error(f"Error loading monitoring history: {str(e)}")
    
    def _save_monitoring_history(self):
        """
        Save monitoring history to disk.
        """
        history_path = os.path.join(os.path.dirname(self.model_path), 'monitoring_history.json')
        try:
            history = {
                'metrics_history': self.metrics_history,
                'drift_scores': self.drift_scores,
                'last_retraining_date': self.last_retraining_date,
                'performance_history': self.performance_history
            }
            
            with open(history_path, 'w') as f:
                json.dump(history, f, indent=2, default=str)
                
            self.logger.info(f"Saved monitoring history to {history_path}")
        except Exception as e:
            self.logger.error(f"Error saving monitoring history: {str(e)}")
    
    def record_prediction(self, features: np.ndarray, prediction: np.ndarray, 
                         actual_label: Optional[np.ndarray] = None):
        """
        Record a prediction for monitoring purposes.
        
        Args:
            features: Input features used for prediction
            prediction: Model's prediction
            actual_label: Actual label if available (for supervised monitoring)
        """
        timestamp = datetime.now().isoformat()
        
        # Store prediction record
        record = {
            'timestamp': timestamp,
            'prediction': prediction.tolist() if isinstance(prediction, np.ndarray) else prediction,
        }
        
        # If we have the actual label, store it and compute accuracy
        if actual_label is not None:
            record['actual_label'] = actual_label.tolist() if isinstance(actual_label, np.ndarray) else actual_label
            record['correct'] = (prediction == actual_label).tolist() if isinstance(prediction, np.ndarray) else (prediction == actual_label)
            
            # Store for potential retraining
            self.new_data_features.append(features)
            self.new_data_labels.append(actual_label)
        
        # Add to metrics history
        self.metrics_history.append(record)
        
        # Periodically save history
        if len(self.metrics_history) % 100 == 0:
            self._save_monitoring_history()
    
    def detect_data_drift(self, current_data: np.ndarray, reference_data: np.ndarray, 
                         method: str = 'distribution') -> Tuple[bool, Dict]:
        """
        Detect data drift between current and reference datasets.
        
        Args:
            current_data: Current dataset features
            reference_data: Reference dataset features (e.g., training data)
            method: Method for drift detection ('distribution', 'statistics')
            
        Returns:
            Tuple of (drift_detected, drift_metrics)
        """
        drift_detected = False
        drift_metrics = {}
        
        try:
            if method == 'distribution':
                # KL divergence for distribution comparison
                from scipy.stats import entropy
                
                # For each feature
                for i in range(current_data.shape[1]):
                    # Get feature values
                    current_values = current_data[:, i]
                    reference_values = reference_data[:, i]
                    
                    # Create histograms
                    hist_current, bin_edges = np.histogram(current_values, bins=20, density=True)
                    hist_reference, _ = np.histogram(reference_values, bins=bin_edges, density=True)
                    
                    # Add small epsilon to avoid division by zero
                    hist_current = hist_current + 1e-10
                    hist_reference = hist_reference + 1e-10
                    
                    # Calculate KL divergence
                    kl_div = entropy(hist_current, hist_reference)
                    
                    # Store drift score
                    drift_metrics[f'feature_{i}_kl_divergence'] = float(kl_div)
                    
                    # Check if drift exceeds threshold
                    if kl_div > self.drift_threshold:
                        drift_detected = True
            
            elif method == 'statistics':
                # Statistical moments comparison
                for i in range(current_data.shape[1]):
                    # Get feature values
                    current_values = current_data[:, i]
                    reference_values = reference_data[:, i]
                    
                    # Calculate statistics
                    current_mean = np.mean(current_values)
                    reference_mean = np.mean(reference_values)
                    current_std = np.std(current_values)
                    reference_std = np.std(reference_values)
                    
                    # Calculate relative differences
                    mean_diff = abs(current_mean - reference_mean) / (abs(reference_mean) + 1e-10)
                    std_diff = abs(current_std - reference_std) / (abs(reference_std) + 1e-10)
                    
                    # Store drift metrics
                    drift_metrics[f'feature_{i}_mean_diff'] = float(mean_diff)
                    drift_metrics[f'feature_{i}_std_diff'] = float(std_diff)
                    
                    # Check if drift exceeds threshold
                    if mean_diff > self.drift_threshold or std_diff > self.drift_threshold:
                        drift_detected = True
            
            # Update drift scores
            self.drift_scores[datetime.now().isoformat()] = drift_metrics
            
            return drift_detected, drift_metrics
            
        except Exception as e:
            self.logger.error(f"Error detecting data drift: {str(e)}")
            return False, {'error': str(e)}
    
    def check_retraining_needed(self, performance_metrics: Optional[Dict] = None) -> bool:
        """
        Check if model retraining is needed based on drift and performance.
        
        Args:
            performance_metrics: Current model performance metrics (optional)
            
        Returns:
            Boolean indicating if retraining is needed
        """
        # Store performance metrics if provided
        if performance_metrics:
            self.performance_history.append({
                'timestamp': datetime.now().isoformat(),
                'metrics': performance_metrics
            })
        
        # Check if enough time has passed since last retraining
        if self.last_retraining_date:
            last_retraining = datetime.fromisoformat(self.last_retraining_date) \
                if isinstance(self.last_retraining_date, str) else self.last_retraining_date
            days_since_retraining = (datetime.now() - last_retraining).days
            if days_since_retraining < self.retraining_interval_days:
                self.logger.info(f"Only {days_since_retraining} days since last retraining, minimum interval is {self.retraining_interval_days} days")
                return False
        
        # Check if we have enough new data for retraining
        if len(self.new_data_labels) < 100:  # Arbitrary threshold
            self.logger.info(f"Not enough new labeled data for retraining: {len(self.new_data_labels)} samples")
            return False
        
        # Check if recent drift scores indicate significant drift
        recent_drift_scores = list(self.drift_scores.items())[-10:] if len(self.drift_scores) > 10 else self.drift_scores.items()
        drift_detected = False
        
        for _, metrics in recent_drift_scores:
            for metric_name, value in metrics.items():
                if 'diff' in metric_name and value > self.drift_threshold:
                    drift_detected = True
                    break
            if drift_detected:
                break
        
        # Check if performance has degraded
        performance_degraded = False
        if len(self.performance_history) >= 2:
            latest_performance = self.performance_history[-1]['metrics']
            previous_performance = self.performance_history[-2]['metrics']
            
            # Check accuracy or F1 score degradation
            for metric in ['accuracy', 'f1_score']:
                if metric in latest_performance and metric in previous_performance:
                    if latest_performance[metric] < previous_performance[metric] * 0.95:  # 5% degradation
                        performance_degraded = True
                        break
        
        # Decide if retraining is needed
        retraining_needed = drift_detected or performance_degraded
        
        if retraining_needed:
            self.logger.info(f"Retraining recommended: drift_detected={drift_detected}, performance_degraded={performance_degraded}")
        
        return retraining_needed
    
    def get_retraining_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get collected data for model retraining.
        
        Returns:
            Tuple of (features, labels) for retraining
        """
        if not self.new_data_features or not self.new_data_labels:
            raise ValueError("No new data available for retraining")
        
        # Convert lists to numpy arrays
        X = np.array(self.new_data_features)
        y = np.array(self.new_data_labels)
        
        return X, y
    
    def record_retraining(self, performance_metrics: Dict):
        """
        Record that model retraining has occurred.
        
        Args:
            performance_metrics: Performance metrics from retraining
        """
        self.last_retraining_date = datetime.now().isoformat()
        
        # Add to performance history
        self.performance_history.append({
            'timestamp': self.last_retraining_date,
            'metrics': performance_metrics,
            'retraining': True
        })
        
        # Clear collected data
        self.new_data_features = []
        self.new_data_labels = []
        
        # Save updated history
        self._save_monitoring_history()
        
        self.logger.info(f"Recorded retraining with metrics: {performance_metrics}")
    
    def generate_monitoring_report(self, output_path: Optional[str] = None) -> Dict:
        """
        Generate a monitoring report with drift and performance metrics.
        
        Args:
            output_path: Path to save the report (optional)
            
        Returns:
            Dictionary with report data
        """
        # Prepare report data
        report = {
            'generated_at': datetime.now().isoformat(),
            'model_path': self.model_path,
            'last_retraining_date': self.last_retraining_date,
            'drift_threshold': self.drift_threshold,
            'retraining_interval_days': self.retraining_interval_days,
            'new_data_samples': len(self.new_data_labels),
            'metrics_history_samples': len(self.metrics_history),
        }
        
        # Add drift analysis
        if self.drift_scores:
            # Get recent drift scores
            recent_drift = list(self.drift_scores.items())[-10:]
            report['recent_drift_scores'] = dict(recent_drift)
            
            # Calculate average drift by feature
            avg_drift_by_feature = {}
            for _, metrics in self.drift_scores.items():
                for metric_name, value in metrics.items():
                    if metric_name not in avg_drift_by_feature:
                        avg_drift_by_feature[metric_name] = []
                    avg_drift_by_feature[metric_name].append(value)
            
            report['average_drift_by_feature'] = {
                metric: float(np.mean(values)) 
                for metric, values in avg_drift_by_feature.items()
            }
        
        # Add performance analysis
        if self.performance_history:
            # Get recent performance
            recent_performance = self.performance_history[-5:]
            report['recent_performance'] = recent_performance
            
            # Calculate performance trends
            if len(self.performance_history) >= 2:
                trends = {}
                latest = self.performance_history[-1]['metrics']
                first = self.performance_history[0]['metrics']
                
                for metric in set(latest.keys()).intersection(set(first.keys())):
                    if isinstance(latest[metric], (int, float)) and isinstance(first[metric], (int, float)):
                        trends[metric] = {
                            'first': first[metric],
                            'latest': latest[metric],
                            'change': latest[metric] - first[metric],
                            'percent_change': (latest[metric] - first[metric]) / (abs(first[metric]) + 1e-10) * 100
                        }
                
                report['performance_trends'] = trends
        
        # Save report if path provided
        if output_path:
            try:
                with open(output_path, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                self.logger.info(f"Saved monitoring report to {output_path}")
            except Exception as e:
                self.logger.error(f"Error saving monitoring report: {str(e)}")
        
        return report


class AutomatedRetrainingPipeline:
    def __init__(self, model_path: str, monitor: ModelMonitor, 
                 predictor=None, preprocessor=None):
        """
        Initialize the automated retraining pipeline.
        
        Args:
            model_path: Path to the model file
            monitor: ModelMonitor instance
            predictor: Model predictor instance (optional)
            preprocessor: Data preprocessor instance (optional)
        """
        self.model_path = model_path
        self.monitor = monitor
        self.predictor = predictor
        self.preprocessor = preprocessor
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def check_and_retrain(self, reference_data: Optional[np.ndarray] = None) -> bool:
        """
        Check if retraining is needed and perform retraining if necessary.
        
        Args:
            reference_data: Reference data for drift detection (optional)
            
        Returns:
            Boolean indicating if retraining was performed
        """
        try:
            # Check if retraining is needed
            if not self.monitor.check_retraining_needed():
                self.logger.info("Retraining not needed at this time")
                return False
            
            # Get data for retraining
            X, y = self.monitor.get_retraining_data()
            
            if len(X) < 50:  # Minimum samples for retraining
                self.logger.warning(f"Insufficient data for retraining: {len(X)} samples")
                return False
            
            # Perform retraining
            self.logger.info(f"Starting model retraining with {len(X)} samples")
            
            if self.predictor is None:
                self.logger.error("Predictor not provided, cannot retrain")
                return False
            
            # Train the model
            metrics = self.predictor.train(X, y)
            
            # Save the retrained model
            self.predictor.save_model(self.model_path)
            
            # Record retraining in monitor
            self.monitor.record_retraining(metrics)
            
            self.logger.info(f"Model retraining completed successfully with metrics: {metrics}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in retraining pipeline: {str(e)}")
            return False
    
    def schedule_periodic_check(self, interval_hours: int = 24):
        """
        Schedule periodic checks for retraining.
        
        Args:
            interval_hours: Hours between checks
        """
        import schedule
        import time
        
        def job():
            self.logger.info("Running scheduled retraining check")
            self.check_and_retrain()
        
        schedule.every(interval_hours).hours.do(job)
        
        self.logger.info(f"Scheduled retraining checks every {interval_hours} hours")
        
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Sleep for an hour between checks
    
    def run_on_demand(self, reference_data: Optional[np.ndarray] = None) -> Dict:
        """
        Run the retraining pipeline on demand and generate a report.
        
        Args:
            reference_data: Reference data for drift detection (optional)
            
        Returns:
            Dictionary with pipeline results
        """
        # Check and retrain if needed
        retraining_performed = self.check_and_retrain(reference_data)
        
        # Generate monitoring report
        report_path = os.path.join(
            os.path.dirname(self.model_path), 
            f'monitoring_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        )
        report = self.monitor.generate_monitoring_report(report_path)
        
        # Add retraining status
        report['retraining_performed'] = retraining_performed
        
        return report