#!/usr/bin/env python3
"""
Automated Model Performance Reporter

This module generates comprehensive performance reports for the waterborne disease prediction model,
including metrics visualization, confusion matrices, ROC curves, and prediction analysis.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Union, Optional, Any
from sklearn.metrics import (confusion_matrix, classification_report, 
                             roc_curve, auc, precision_recall_curve, 
                             average_precision_score)

class PerformanceReporter:
    def __init__(self, output_dir: str, model_name: str = "waterborne_disease_model"):
        """
        Initialize the performance reporter.
        
        Args:
            output_dir: Directory to save reports
            model_name: Name of the model for report titles
        """
        self.output_dir = output_dir
        self.model_name = model_name
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Store performance data
        self.performance_data = []
    
    def add_performance_data(self, y_true: np.ndarray, y_pred: np.ndarray, 
                            y_prob: np.ndarray, feature_names: List[str],
                            feature_importance: Optional[np.ndarray] = None,
                            metadata: Optional[Dict] = None):
        """
        Add performance data for reporting.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_prob: Prediction probabilities
            feature_names: Names of features used
            feature_importance: Feature importance scores (optional)
            metadata: Additional metadata about the prediction run (optional)
        """
        timestamp = datetime.now().isoformat()
        
        data = {
            'timestamp': timestamp,
            'y_true': y_true.tolist() if isinstance(y_true, np.ndarray) else y_true,
            'y_pred': y_pred.tolist() if isinstance(y_pred, np.ndarray) else y_pred,
            'y_prob': y_prob.tolist() if isinstance(y_prob, np.ndarray) else y_prob,
            'feature_names': feature_names,
        }
        
        if feature_importance is not None:
            data['feature_importance'] = feature_importance.tolist() if isinstance(feature_importance, np.ndarray) else feature_importance
        
        if metadata is not None:
            data['metadata'] = metadata
        
        self.performance_data.append(data)
        self.logger.info(f"Added performance data from {timestamp}")
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray, 
                          y_prob: np.ndarray) -> Dict:
        """
        Calculate performance metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_prob: Prediction probabilities
            
        Returns:
            Dictionary of performance metrics
        """
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
        
        metrics = {}
        
        # Basic classification metrics
        metrics['accuracy'] = float(accuracy_score(y_true, y_pred))
        
        # Handle binary and multi-class cases
        if len(np.unique(y_true)) == 2:  # Binary classification
            metrics['precision'] = float(precision_score(y_true, y_pred))
            metrics['recall'] = float(recall_score(y_true, y_pred))
            metrics['f1_score'] = float(f1_score(y_true, y_pred))
            
            # ROC AUC
            if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                # Multi-class probabilities, take the positive class
                metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob[:, 1]))
            else:
                metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob))
        else:  # Multi-class classification
            metrics['precision'] = float(precision_score(y_true, y_pred, average='weighted'))
            metrics['recall'] = float(recall_score(y_true, y_pred, average='weighted'))
            metrics['f1_score'] = float(f1_score(y_true, y_pred, average='weighted'))
            
            # Multi-class ROC AUC
            try:
                metrics['roc_auc'] = float(roc_auc_score(y_true, y_prob, multi_class='ovr', average='weighted'))
            except ValueError:
                metrics['roc_auc'] = None
                self.logger.warning("Could not calculate ROC AUC for multi-class")
        
        return metrics
    
    def _plot_confusion_matrix(self, y_true: np.ndarray, y_pred: np.ndarray, 
                             class_names: Optional[List[str]] = None) -> plt.Figure:
        """
        Plot confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            class_names: Names of classes (optional)
            
        Returns:
            Matplotlib figure with confusion matrix
        """
        cm = confusion_matrix(y_true, y_pred)
        
        if class_names is None:
            class_names = [str(i) for i in range(len(np.unique(np.concatenate([y_true, y_pred]))))]
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names)
        plt.xlabel('Predicted')
        plt.ylabel('True')
        plt.title('Confusion Matrix')
        
        return plt.gcf()
    
    def _plot_roc_curve(self, y_true: np.ndarray, y_prob: np.ndarray, 
                      class_names: Optional[List[str]] = None) -> plt.Figure:
        """
        Plot ROC curve.
        
        Args:
            y_true: True labels
            y_prob: Prediction probabilities
            class_names: Names of classes (optional)
            
        Returns:
            Matplotlib figure with ROC curve
        """
        plt.figure(figsize=(10, 8))
        
        # Handle binary and multi-class cases
        if len(np.unique(y_true)) == 2:  # Binary classification
            # Get probabilities for positive class
            if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                y_prob_pos = y_prob[:, 1]
            else:
                y_prob_pos = y_prob
            
            fpr, tpr, _ = roc_curve(y_true, y_prob_pos)
            roc_auc = auc(fpr, tpr)
            
            plt.plot(fpr, tpr, lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
            plt.plot([0, 1], [0, 1], 'k--', lw=2)
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Receiver Operating Characteristic')
            plt.legend(loc="lower right")
            
        else:  # Multi-class classification
            from sklearn.preprocessing import label_binarize
            
            # Binarize the labels for multi-class ROC
            classes = np.unique(y_true)
            y_true_bin = label_binarize(y_true, classes=classes)
            
            if class_names is None:
                class_names = [str(i) for i in classes]
            
            # Compute ROC curve and ROC area for each class
            for i, class_name in enumerate(class_names):
                fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_prob[:, i])
                roc_auc = auc(fpr, tpr)
                plt.plot(fpr, tpr, lw=2, label=f'{class_name} (area = {roc_auc:.2f})')
            
            plt.plot([0, 1], [0, 1], 'k--', lw=2)
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('Multi-class Receiver Operating Characteristic')
            plt.legend(loc="lower right")
        
        return plt.gcf()
    
    def _plot_precision_recall_curve(self, y_true: np.ndarray, y_prob: np.ndarray, 
                                   class_names: Optional[List[str]] = None) -> plt.Figure:
        """
        Plot precision-recall curve.
        
        Args:
            y_true: True labels
            y_prob: Prediction probabilities
            class_names: Names of classes (optional)
            
        Returns:
            Matplotlib figure with precision-recall curve
        """
        plt.figure(figsize=(10, 8))
        
        # Handle binary and multi-class cases
        if len(np.unique(y_true)) == 2:  # Binary classification
            # Get probabilities for positive class
            if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                y_prob_pos = y_prob[:, 1]
            else:
                y_prob_pos = y_prob
            
            precision, recall, _ = precision_recall_curve(y_true, y_prob_pos)
            avg_precision = average_precision_score(y_true, y_prob_pos)
            
            plt.plot(recall, precision, lw=2, label=f'Precision-Recall curve (AP = {avg_precision:.2f})')
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Precision-Recall Curve')
            plt.legend(loc="lower left")
            
        else:  # Multi-class classification
            from sklearn.preprocessing import label_binarize
            
            # Binarize the labels for multi-class PR curve
            classes = np.unique(y_true)
            y_true_bin = label_binarize(y_true, classes=classes)
            
            if class_names is None:
                class_names = [str(i) for i in classes]
            
            # Compute PR curve and average precision for each class
            for i, class_name in enumerate(class_names):
                precision, recall, _ = precision_recall_curve(y_true_bin[:, i], y_prob[:, i])
                avg_precision = average_precision_score(y_true_bin[:, i], y_prob[:, i])
                plt.plot(recall, precision, lw=2, label=f'{class_name} (AP = {avg_precision:.2f})')
            
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Multi-class Precision-Recall Curve')
            plt.legend(loc="lower left")
        
        return plt.gcf()
    
    def _plot_feature_importance(self, feature_names: List[str], 
                               feature_importance: np.ndarray) -> plt.Figure:
        """
        Plot feature importance.
        
        Args:
            feature_names: Names of features
            feature_importance: Feature importance scores
            
        Returns:
            Matplotlib figure with feature importance
        """
        # Sort features by importance
        indices = np.argsort(feature_importance)
        
        plt.figure(figsize=(12, 8))
        plt.barh(range(len(indices)), feature_importance[indices], align='center')
        plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
        plt.xlabel('Feature Importance')
        plt.title('Feature Importance Ranking')
        
        return plt.gcf()
    
    def _plot_prediction_distribution(self, y_true: np.ndarray, y_prob: np.ndarray) -> plt.Figure:
        """
        Plot distribution of prediction probabilities.
        
        Args:
            y_true: True labels
            y_prob: Prediction probabilities
            
        Returns:
            Matplotlib figure with prediction distribution
        """
        plt.figure(figsize=(10, 8))
        
        # Handle binary and multi-class cases
        if len(np.unique(y_true)) == 2:  # Binary classification
            # Get probabilities for positive class
            if y_prob.ndim > 1 and y_prob.shape[1] > 1:
                y_prob_pos = y_prob[:, 1]
            else:
                y_prob_pos = y_prob
            
            # Plot distribution of probabilities for each class
            sns.histplot(y_prob_pos[y_true == 0], kde=True, label='Class 0 (Negative)', alpha=0.5)
            sns.histplot(y_prob_pos[y_true == 1], kde=True, label='Class 1 (Positive)', alpha=0.5)
            plt.xlabel('Prediction Probability')
            plt.ylabel('Density')
            plt.title('Distribution of Prediction Probabilities')
            plt.legend()
            
        else:  # Multi-class classification
            # For multi-class, plot the max probability for each sample
            max_probs = np.max(y_prob, axis=1)
            correct = (np.argmax(y_prob, axis=1) == y_true)
            
            sns.histplot(max_probs[correct], kde=True, label='Correct Predictions', alpha=0.5)
            sns.histplot(max_probs[~correct], kde=True, label='Incorrect Predictions', alpha=0.5)
            plt.xlabel('Max Prediction Probability')
            plt.ylabel('Density')
            plt.title('Distribution of Max Prediction Probabilities')
            plt.legend()
        
        return plt.gcf()
    
    def generate_report(self, report_id: Optional[str] = None, 
                       class_names: Optional[List[str]] = None) -> str:
        """
        Generate a comprehensive performance report.
        
        Args:
            report_id: Unique identifier for the report (optional)
            class_names: Names of classes (optional)
            
        Returns:
            Path to the generated report
        """
        if not self.performance_data:
            raise ValueError("No performance data available for reporting")
        
        # Use the latest performance data
        data = self.performance_data[-1]
        
        # Extract data
        y_true = np.array(data['y_true'])
        y_pred = np.array(data['y_pred'])
        y_prob = np.array(data['y_prob'])
        feature_names = data['feature_names']
        
        # Generate report ID if not provided
        if report_id is None:
            report_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create report directory
        report_dir = os.path.join(self.output_dir, f"report_{report_id}")
        os.makedirs(report_dir, exist_ok=True)
        
        # Calculate metrics
        metrics = self._calculate_metrics(y_true, y_pred, y_prob)
        
        # Generate plots
        plots = {}
        
        # Confusion matrix
        cm_fig = self._plot_confusion_matrix(y_true, y_pred, class_names)
        cm_path = os.path.join(report_dir, "confusion_matrix.png")
        cm_fig.savefig(cm_path)
        plots['confusion_matrix'] = cm_path
        plt.close(cm_fig)
        
        # ROC curve
        try:
            roc_fig = self._plot_roc_curve(y_true, y_prob, class_names)
            roc_path = os.path.join(report_dir, "roc_curve.png")
            roc_fig.savefig(roc_path)
            plots['roc_curve'] = roc_path
            plt.close(roc_fig)
        except Exception as e:
            self.logger.warning(f"Could not generate ROC curve: {str(e)}")
        
        # Precision-recall curve
        try:
            pr_fig = self._plot_precision_recall_curve(y_true, y_prob, class_names)
            pr_path = os.path.join(report_dir, "precision_recall_curve.png")
            pr_fig.savefig(pr_path)
            plots['precision_recall_curve'] = pr_path
            plt.close(pr_fig)
        except Exception as e:
            self.logger.warning(f"Could not generate precision-recall curve: {str(e)}")
        
        # Feature importance
        if 'feature_importance' in data:
            feature_importance = np.array(data['feature_importance'])
            fi_fig = self._plot_feature_importance(feature_names, feature_importance)
            fi_path = os.path.join(report_dir, "feature_importance.png")
            fi_fig.savefig(fi_path)
            plots['feature_importance'] = fi_path
            plt.close(fi_fig)
        
        # Prediction distribution
        try:
            dist_fig = self._plot_prediction_distribution(y_true, y_prob)
            dist_path = os.path.join(report_dir, "prediction_distribution.png")
            dist_fig.savefig(dist_path)
            plots['prediction_distribution'] = dist_path
            plt.close(dist_fig)
        except Exception as e:
            self.logger.warning(f"Could not generate prediction distribution: {str(e)}")
        
        # Generate classification report
        clf_report = classification_report(y_true, y_pred, output_dict=True)
        
        # Prepare report data
        report_data = {
            'report_id': report_id,
            'timestamp': datetime.now().isoformat(),
            'model_name': self.model_name,
            'metrics': metrics,
            'classification_report': clf_report,
            'plots': plots,
        }
        
        # Add metadata if available
        if 'metadata' in data:
            report_data['metadata'] = data['metadata']
        
        # Save report data
        report_json_path = os.path.join(report_dir, "report_data.json")
        with open(report_json_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        # Generate HTML report
        html_report_path = self._generate_html_report(report_data, report_dir)
        
        self.logger.info(f"Generated performance report at {html_report_path}")
        return html_report_path
    
    def _generate_html_report(self, report_data: Dict, report_dir: str) -> str:
        """
        Generate an HTML report from report data.
        
        Args:
            report_data: Report data dictionary
            report_dir: Directory to save the report
            
        Returns:
            Path to the HTML report
        """
        html_path = os.path.join(report_dir, "report.html")
        
        # Basic HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.model_name} Performance Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .metrics {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px; }}
                .metric-card {{ background-color: #f8f9fa; border-radius: 5px; padding: 15px; flex: 1; min-width: 200px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #3498db; }}
                .plot-container {{ margin-bottom: 30px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{self.model_name} Performance Report</h1>
                <p><strong>Report ID:</strong> {report_data['report_id']}</p>
                <p><strong>Generated:</strong> {report_data['timestamp']}</p>
                
                <h2>Performance Metrics</h2>
                <div class="metrics">
        """
        
        # Add metrics
        for metric_name, metric_value in report_data['metrics'].items():
            if metric_value is not None:
                html += f"""
                    <div class="metric-card">
                        <div class="metric-name">{metric_name.replace('_', ' ').title()}</div>
                        <div class="metric-value">{metric_value:.4f}</div>
                    </div>
                """
        
        html += "</div>\n"
        
        # Add plots
        html += "<h2>Visualizations</h2>\n"
        
        for plot_name, plot_path in report_data['plots'].items():
            plot_title = plot_name.replace('_', ' ').title()
            relative_path = os.path.basename(plot_path)
            
            html += f"""
                <div class="plot-container">
                    <h3>{plot_title}</h3>
                    <img src="{relative_path}" alt="{plot_title}" style="max-width: 100%; height: auto;">
                </div>
            """
        
        # Add classification report
        html += "<h2>Classification Report</h2>\n"
        html += "<table>\n"
        html += "<tr><th>Class</th><th>Precision</th><th>Recall</th><th>F1-Score</th><th>Support</th></tr>\n"
        
        clf_report = report_data['classification_report']
        for class_name, metrics in clf_report.items():
            if isinstance(metrics, dict):  # Skip 'accuracy', etc.
                html += f"<tr><td>{class_name}</td><td>{metrics['precision']:.4f}</td><td>{metrics['recall']:.4f}</td><td>{metrics['f1-score']:.4f}</td><td>{metrics['support']}</td></tr>\n"
        
        html += "</table>\n"
        
        # Add metadata if available
        if 'metadata' in report_data:
            html += "<h2>Additional Information</h2>\n"
            html += "<table>\n"
            html += "<tr><th>Property</th><th>Value</th></tr>\n"
            
            for key, value in report_data['metadata'].items():
                html += f"<tr><td>{key}</td><td>{value}</td></tr>\n"
            
            html += "</table>\n"
        
        # Close HTML
        html += """
            </div>
        </body>
        </html>
        """
        
        # Write HTML to file
        with open(html_path, 'w') as f:
            f.write(html)
        
        return html_path
    
    def compare_models(self, model_names: List[str], report_ids: List[str]) -> str:
        """
        Generate a comparative report between multiple models.
        
        Args:
            model_names: Names of models to compare
            report_ids: IDs of reports to compare
            
        Returns:
            Path to the comparative report
        """
        if len(model_names) != len(report_ids):
            raise ValueError("Number of model names must match number of report IDs")
        
        # Create comparison directory
        comparison_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        comparison_dir = os.path.join(self.output_dir, f"comparison_{comparison_id}")
        os.makedirs(comparison_dir, exist_ok=True)
        
        # Load report data
        reports = []
        for i, report_id in enumerate(report_ids):
            report_path = os.path.join(self.output_dir, f"report_{report_id}", "report_data.json")
            try:
                with open(report_path, 'r') as f:
                    report_data = json.load(f)
                    report_data['model_name'] = model_names[i]  # Override model name
                    reports.append(report_data)
            except Exception as e:
                self.logger.error(f"Could not load report {report_id}: {str(e)}")
        
        if not reports:
            raise ValueError("No valid reports found for comparison")
        
        # Generate comparison plots
        plots = {}
        
        # Compare metrics
        metrics_to_compare = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        metrics_data = {metric: [] for metric in metrics_to_compare}
        
        for report in reports:
            for metric in metrics_to_compare:
                if metric in report['metrics'] and report['metrics'][metric] is not None:
                    metrics_data[metric].append(report['metrics'][metric])
                else:
                    metrics_data[metric].append(0)  # Default value if metric not available
        
        # Plot metrics comparison
        plt.figure(figsize=(12, 8))
        x = np.arange(len(model_names))
        width = 0.15
        multiplier = 0
        
        for metric, values in metrics_data.items():
            offset = width * multiplier
            plt.bar(x + offset, values, width, label=metric.replace('_', ' ').title())
            multiplier += 1
        
        plt.xlabel('Models')
        plt.ylabel('Score')
        plt.title('Performance Metrics Comparison')
        plt.xticks(x + width * (len(metrics_data) - 1) / 2, model_names)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()
        
        metrics_plot_path = os.path.join(comparison_dir, "metrics_comparison.png")
        plt.savefig(metrics_plot_path)
        plots['metrics_comparison'] = metrics_plot_path
        plt.close()
        
        # Generate HTML comparison report
        html_path = os.path.join(comparison_dir, "comparison_report.html")
        
        # Basic HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Model Comparison Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .plot-container {{ margin-bottom: 30px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .best {{ background-color: #d4edda; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Model Comparison Report</h1>
                <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
                
                <h2>Performance Metrics Comparison</h2>
                <div class="plot-container">
                    <img src="{os.path.basename(metrics_plot_path)}" alt="Metrics Comparison" style="max-width: 100%; height: auto;">
                </div>
                
                <h2>Detailed Metrics</h2>
                <table>
                    <tr>
                        <th>Metric</th>
        """
        
        # Add model names as headers
        for model_name in model_names:
            html += f"<th>{model_name}</th>\n"
        
        html += "</tr>\n"
        
        # Add metrics rows
        for metric in metrics_to_compare:
            html += f"<tr><td>{metric.replace('_', ' ').title()}</td>\n"
            
            # Find best value for highlighting
            values = metrics_data[metric]
            best_idx = np.argmax(values) if values else -1
            
            for i, value in enumerate(values):
                if i == best_idx:
                    html += f"<td class='best'>{value:.4f}</td>\n"
                else:
                    html += f"<td>{value:.4f}</td>\n"
            
            html += "</tr>\n"
        
        html += "</table>\n"
        
        # Add links to individual reports
        html += "<h2>Individual Reports</h2>\n"
        html += "<ul>\n"
        
        for i, report in enumerate(reports):
            report_path = os.path.join(self.output_dir, f"report_{report_ids[i]}", "report.html")
            if os.path.exists(report_path):
                relative_path = os.path.relpath(report_path, comparison_dir)
                html += f"<li><a href='{relative_path}' target='_blank'>{model_names[i]} Detailed Report</a></li>\n"
        
        html += "</ul>\n"
        
        # Close HTML
        html += """
            </div>
        </body>
        </html>
        """
        
        # Write HTML to file
        with open(html_path, 'w') as f:
            f.write(html)
        
        self.logger.info(f"Generated model comparison report at {html_path}")
        return html_path
    
    def track_performance_over_time(self, metric_name: str = 'accuracy') -> str:
        """
        Generate a report tracking model performance over time.
        
        Args:
            metric_name: Name of the metric to track
            
        Returns:
            Path to the tracking report
        """
        if len(self.performance_data) < 2:
            raise ValueError("Need at least two performance data points to track over time")
        
        # Create tracking directory
        tracking_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        tracking_dir = os.path.join(self.output_dir, f"tracking_{tracking_id}")
        os.makedirs(tracking_dir, exist_ok=True)
        
        # Extract timestamps and metrics
        timestamps = []
        metrics = []
        
        for data in self.performance_data:
            # Calculate metrics for this data point
            y_true = np.array(data['y_true'])
            y_pred = np.array(data['y_pred'])
            y_prob = np.array(data['y_prob'])
            
            calculated_metrics = self._calculate_metrics(y_true, y_pred, y_prob)
            
            if metric_name in calculated_metrics and calculated_metrics[metric_name] is not None:
                timestamps.append(datetime.fromisoformat(data['timestamp']))
                metrics.append(calculated_metrics[metric_name])
        
        if not timestamps or not metrics:
            raise ValueError(f"No valid {metric_name} metrics found in performance data")
        
        # Plot metric over time
        plt.figure(figsize=(12, 8))
        plt.plot(timestamps, metrics, 'o-', linewidth=2)
        plt.xlabel('Time')
        plt.ylabel(metric_name.replace('_', ' ').title())
        plt.title(f'{self.model_name} {metric_name.replace("_", " ").title()} Over Time')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        tracking_plot_path = os.path.join(tracking_dir, f"{metric_name}_over_time.png")
        plt.savefig(tracking_plot_path)
        plt.close()
        
        # Generate HTML tracking report
        html_path = os.path.join(tracking_dir, "tracking_report.html")
        
        # Basic HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{self.model_name} Performance Tracking</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                .plot-container {{ margin-bottom: 30px; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{self.model_name} Performance Tracking</h1>
                <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>
                
                <h2>{metric_name.replace('_', ' ').title()} Over Time</h2>
                <div class="plot-container">
                    <img src="{os.path.basename(tracking_plot_path)}" alt="{metric_name.replace('_', ' ').title()} Over Time" style="max-width: 100%; height: auto;">
                </div>
                
                <h2>Detailed Metrics</h2>
                <table>
                    <tr>
                        <th>Timestamp</th>
                        <th>{metric_name.replace('_', ' ').title()}</th>
                    </tr>
        """
        
        # Add metrics rows
        for i in range(len(timestamps)):
            html += f"<tr><td>{timestamps[i].isoformat()}</td><td>{metrics[i]:.4f}</td></tr>\n"
        
        html += "</table>\n"
        
        # Add statistics
        html += "<h2>Statistics</h2>\n"
        html += "<table>\n"
        html += "<tr><th>Statistic</th><th>Value</th></tr>\n"
        html += f"<tr><td>Mean</td><td>{np.mean(metrics):.4f}</td></tr>\n"
        html += f"<tr><td>Standard Deviation</td><td>{np.std(metrics):.4f}</td></tr>\n"
        html += f"<tr><td>Minimum</td><td>{np.min(metrics):.4f}</td></tr>\n"
        html += f"<tr><td>Maximum</td><td>{np.max(metrics):.4f}</td></tr>\n"
        
        # Calculate trend
        if len(metrics) >= 2:
            first_half = np.mean(metrics[:len(metrics)//2])
            second_half = np.mean(metrics[len(metrics)//2:])
            trend = second_half - first_half
            trend_percent = (trend / first_half) * 100 if first_half != 0 else 0
            
            trend_direction = "Improving" if trend > 0 else "Declining" if trend < 0 else "Stable"
            html += f"<tr><td>Trend</td><td>{trend_direction} ({trend_percent:.2f}%)</td></tr>\n"
        
        html += "</table>\n"
        
        # Close HTML
        html += """
            </div>
        </body>
        </html>
        """
        
        # Write HTML to file
        with open(html_path, 'w') as f:
            f.write(html)
        
        self.logger.info(f"Generated performance tracking report at {html_path}")
        return html_path