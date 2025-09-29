#!/usr/bin/env python3
"""
Explainable AI Module for Water-Borne Disease Prediction System

This module implements explainable AI features using SHAP (SHapley Additive exPlanations)
to provide interpretable insights into model predictions and feature importance.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap
import os
import logging
from typing import Dict, List, Tuple, Union, Optional, Any

class ExplainableAI:
    def __init__(self, model=None, feature_names=None):
        """
        Initialize the ExplainableAI module.
        
        Args:
            model: The trained model to explain (must be compatible with SHAP)
            feature_names: List of feature names for better visualization
        """
        self.model = model
        self.feature_names = feature_names
        self.explainer = None
        self.shap_values = None
        self.background_data = None
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def set_model(self, model):
        """
        Set or update the model to explain.
        
        Args:
            model: The trained model to explain
        """
        self.model = model
        self.explainer = None  # Reset explainer when model changes
        self.shap_values = None
    
    def set_feature_names(self, feature_names):
        """
        Set or update feature names.
        
        Args:
            feature_names: List of feature names
        """
        self.feature_names = feature_names
    
    def create_explainer(self, background_data, model_type='tree'):
        """
        Create a SHAP explainer for the model.
        
        Args:
            background_data: Representative dataset for SHAP explainer
            model_type: Type of model ('tree', 'linear', 'kernel', etc.)
            
        Returns:
            The created explainer object
        """
        if self.model is None:
            raise ValueError("Model must be set before creating an explainer")
        
        self.background_data = background_data
        
        try:
            if model_type == 'tree':
                self.explainer = shap.TreeExplainer(self.model)
            elif model_type == 'linear':
                self.explainer = shap.LinearExplainer(self.model, background_data)
            elif model_type == 'kernel':
                self.explainer = shap.KernelExplainer(self.model.predict, background_data)
            elif model_type == 'deep':
                self.explainer = shap.DeepExplainer(self.model, background_data)
            else:
                self.explainer = shap.Explainer(self.model)
            
            self.logger.info(f"Created {model_type} SHAP explainer")
            return self.explainer
            
        except Exception as e:
            self.logger.error(f"Error creating explainer: {str(e)}")
            raise
    
    def explain_prediction(self, X, output_names=None):
        """
        Generate SHAP values to explain predictions.
        
        Args:
            X: Input data to explain
            output_names: Names for output classes (for classification)
            
        Returns:
            Dictionary with SHAP values and related information
        """
        if self.explainer is None:
            raise ValueError("Explainer must be created before explaining predictions")
        
        try:
            # Calculate SHAP values
            self.shap_values = self.explainer.shap_values(X)
            
            # Prepare results
            result = {
                'shap_values': self.shap_values,
                'expected_value': self.explainer.expected_value if hasattr(self.explainer, 'expected_value') else None,
                'feature_names': self.feature_names
            }
            
            if output_names:
                result['output_names'] = output_names
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error calculating SHAP values: {str(e)}")
            raise
    
    def get_feature_importance(self, global_importance=True):
        """
        Get feature importance based on SHAP values.
        
        Args:
            global_importance: If True, return global feature importance,
                              otherwise return per-sample importance
            
        Returns:
            DataFrame with feature importance values
        """
        if self.shap_values is None:
            raise ValueError("SHAP values must be calculated before getting feature importance")
        
        try:
            # Handle different SHAP value formats
            if isinstance(self.shap_values, list):
                # Multi-class case
                if global_importance:
                    # Average absolute SHAP values across all classes and samples
                    importance_values = np.mean([np.abs(sv).mean(0) for sv in self.shap_values], axis=0)
                else:
                    # Per-sample importance for the predicted class
                    importance_values = np.mean([np.abs(sv) for sv in self.shap_values], axis=0)
            else:
                # Binary/regression case
                if global_importance:
                    importance_values = np.abs(self.shap_values).mean(0)
                else:
                    importance_values = np.abs(self.shap_values)
            
            # Create DataFrame
            if global_importance:
                feature_names = self.feature_names if self.feature_names else [f"Feature {i}" for i in range(len(importance_values))]
                return pd.DataFrame({
                    'Feature': feature_names,
                    'Importance': importance_values
                }).sort_values('Importance', ascending=False)
            else:
                feature_names = self.feature_names if self.feature_names else [f"Feature {i}" for i in range(importance_values.shape[1])]
                return pd.DataFrame(
                    importance_values,
                    columns=feature_names
                )
                
        except Exception as e:
            self.logger.error(f"Error calculating feature importance: {str(e)}")
            raise
    
    def plot_summary(self, max_display=10, plot_type='bar', save_path=None):
        """
        Create a summary plot of SHAP values.
        
        Args:
            max_display: Maximum number of features to display
            plot_type: Type of plot ('bar', 'dot', 'violin')
            save_path: Path to save the plot image
            
        Returns:
            The matplotlib figure
        """
        if self.shap_values is None:
            raise ValueError("SHAP values must be calculated before plotting")
        
        try:
            plt.figure(figsize=(10, 6))
            
            if plot_type == 'bar':
                shap.summary_plot(
                    self.shap_values, 
                    features=self.background_data,
                    feature_names=self.feature_names,
                    max_display=max_display,
                    plot_type='bar',
                    show=False
                )
            elif plot_type == 'violin':
                shap.summary_plot(
                    self.shap_values, 
                    features=self.background_data,
                    feature_names=self.feature_names,
                    max_display=max_display,
                    plot_type='violin',
                    show=False
                )
            else:  # Default to dot plot
                shap.summary_plot(
                    self.shap_values, 
                    features=self.background_data,
                    feature_names=self.feature_names,
                    max_display=max_display,
                    show=False
                )
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Saved SHAP summary plot to {save_path}")
            
            return plt.gcf()
            
        except Exception as e:
            self.logger.error(f"Error creating SHAP summary plot: {str(e)}")
            raise
    
    def plot_dependence(self, feature_idx, interaction_idx=None, save_path=None):
        """
        Create a dependence plot to show how a feature affects predictions.
        
        Args:
            feature_idx: Index or name of the feature to plot
            interaction_idx: Index or name of the feature to use for coloring
            save_path: Path to save the plot image
            
        Returns:
            The matplotlib figure
        """
        if self.shap_values is None:
            raise ValueError("SHAP values must be calculated before plotting")
        
        try:
            # Convert feature name to index if needed
            if isinstance(feature_idx, str) and self.feature_names:
                feature_idx = self.feature_names.index(feature_idx)
            
            # Convert interaction feature name to index if needed
            if isinstance(interaction_idx, str) and self.feature_names:
                interaction_idx = self.feature_names.index(interaction_idx)
            
            plt.figure(figsize=(10, 6))
            
            # Handle different SHAP value formats
            if isinstance(self.shap_values, list):
                # For multi-class, use the first class for visualization
                shap.dependence_plot(
                    feature_idx, 
                    self.shap_values[0], 
                    self.background_data,
                    feature_names=self.feature_names,
                    interaction_index=interaction_idx,
                    show=False
                )
            else:
                shap.dependence_plot(
                    feature_idx, 
                    self.shap_values, 
                    self.background_data,
                    feature_names=self.feature_names,
                    interaction_index=interaction_idx,
                    show=False
                )
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Saved SHAP dependence plot to {save_path}")
            
            return plt.gcf()
            
        except Exception as e:
            self.logger.error(f"Error creating SHAP dependence plot: {str(e)}")
            raise
    
    def plot_force(self, sample_idx=0, save_path=None):
        """
        Create a force plot to visualize the prediction for a single sample.
        
        Args:
            sample_idx: Index of the sample to explain
            save_path: Path to save the plot image
            
        Returns:
            The matplotlib figure
        """
        if self.shap_values is None:
            raise ValueError("SHAP values must be calculated before plotting")
        
        try:
            plt.figure(figsize=(20, 3))
            
            # Handle different SHAP value formats
            if isinstance(self.shap_values, list):
                # For multi-class, use the predicted class
                # Assuming sample_idx is for both X and shap_values
                if isinstance(sample_idx, int):
                    shap_value = self.shap_values[0][sample_idx] if len(self.shap_values[0].shape) > 1 else self.shap_values[0]
                    expected_value = self.explainer.expected_value[0] if isinstance(self.explainer.expected_value, list) else self.explainer.expected_value
                    sample_data = self.background_data[sample_idx] if len(self.background_data.shape) > 1 else self.background_data
                else:  # Assume it's already the data to explain
                    shap_value = self.shap_values[0]
                    expected_value = self.explainer.expected_value[0] if isinstance(self.explainer.expected_value, list) else self.explainer.expected_value
                    sample_data = self.background_data
            else:
                # Binary/regression case
                if isinstance(sample_idx, int):
                    shap_value = self.shap_values[sample_idx] if len(self.shap_values.shape) > 1 else self.shap_values
                    expected_value = self.explainer.expected_value
                    sample_data = self.background_data[sample_idx] if len(self.background_data.shape) > 1 else self.background_data
                else:  # Assume it's already the data to explain
                    shap_value = self.shap_values
                    expected_value = self.explainer.expected_value
                    sample_data = self.background_data
            
            # Create force plot
            shap.force_plot(
                expected_value, 
                shap_value, 
                sample_data,
                feature_names=self.feature_names,
                matplotlib=True,
                show=False
            )
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Saved SHAP force plot to {save_path}")
            
            return plt.gcf()
            
        except Exception as e:
            self.logger.error(f"Error creating SHAP force plot: {str(e)}")
            raise
    
    def generate_explanation_report(self, X, y_pred, output_dir='./explanations'):
        """
        Generate a comprehensive explanation report with multiple visualizations.
        
        Args:
            X: Input data to explain
            y_pred: Predicted values or classes
            output_dir: Directory to save explanation files
            
        Returns:
            Dictionary with paths to generated files
        """
        if self.explainer is None:
            raise ValueError("Explainer must be created before generating reports")
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Calculate SHAP values if not already done
            if self.shap_values is None:
                self.explain_prediction(X)
            
            # Generate and save plots
            plots = {}
            
            # Summary plot
            summary_path = os.path.join(output_dir, 'shap_summary.png')
            self.plot_summary(save_path=summary_path)
            plots['summary'] = summary_path
            
            # Feature importance
            importance = self.get_feature_importance()
            importance_path = os.path.join(output_dir, 'feature_importance.csv')
            importance.to_csv(importance_path, index=False)
            plots['importance'] = importance_path
            
            # Top 3 feature dependence plots
            top_features = importance['Feature'].values[:3]
            for i, feature in enumerate(top_features):
                if isinstance(feature, str) and self.feature_names:
                    feature_idx = self.feature_names.index(feature)
                else:
                    feature_idx = feature
                
                dep_path = os.path.join(output_dir, f'dependence_plot_{i}.png')
                self.plot_dependence(feature_idx, save_path=dep_path)
                plots[f'dependence_{i}'] = dep_path
            
            # Sample force plots (first 3 samples)
            for i in range(min(3, len(X))):
                force_path = os.path.join(output_dir, f'force_plot_{i}.png')
                self.plot_force(sample_idx=i, save_path=force_path)
                plots[f'force_{i}'] = force_path
            
            # Generate HTML report
            html_path = os.path.join(output_dir, 'explanation_report.html')
            with open(html_path, 'w') as f:
                f.write('<html><head><title>Model Explanation Report</title>')
                f.write('<style>body{font-family:Arial;margin:20px;} h1{color:#2c3e50;} ')
                f.write('img{max-width:100%;} .section{margin-bottom:30px;} ')
                f.write('table{border-collapse:collapse;width:100%;} ')
                f.write('th,td{text-align:left;padding:8px;border:1px solid #ddd;} ')
                f.write('tr:nth-child(even){background-color:#f2f2f2;} ')
                f.write('th{background-color:#4CAF50;color:white;}</style></head><body>')
                
                f.write('<h1>Model Explanation Report</h1>')
                
                # Summary section
                f.write('<div class="section"><h2>Feature Importance</h2>')
                f.write(f'<img src="{os.path.basename(plots["summary"])}" alt="SHAP Summary Plot">')
                f.write('<p>This plot shows the most important features for the model\'s predictions.</p></div>')
                
                # Feature importance table
                f.write('<div class="section"><h2>Feature Importance Table</h2><table>')
                f.write('<tr><th>Feature</th><th>Importance Score</th></tr>')
                for _, row in importance.iterrows():
                    f.write(f'<tr><td>{row["Feature"]}</td><td>{row["Importance"]:.4f}</td></tr>')
                f.write('</table></div>')
                
                # Dependence plots
                f.write('<div class="section"><h2>Feature Dependence Plots</h2>')
                f.write('<p>These plots show how specific features affect the model\'s predictions.</p>')
                for i in range(len(top_features)):
                    f.write(f'<h3>{top_features[i]}</h3>')
                    f.write(f'<img src="{os.path.basename(plots[f"dependence_{i}"])}" alt="Dependence Plot {i}">')
                f.write('</div>')
                
                # Force plots
                f.write('<div class="section"><h2>Individual Prediction Explanations</h2>')
                f.write('<p>These plots explain individual predictions by showing how each feature contributes.</p>')
                for i in range(min(3, len(X))):
                    f.write(f'<h3>Sample {i+1}</h3>')
                    f.write(f'<img src="{os.path.basename(plots[f"force_{i}"])}" alt="Force Plot {i}">')
                f.write('</div>')
                
                f.write('</body></html>')
            
            plots['html_report'] = html_path
            self.logger.info(f"Generated explanation report at {html_path}")
            
            return plots
            
        except Exception as e:
            self.logger.error(f"Error generating explanation report: {str(e)}")
            raise