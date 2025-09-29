#!/usr/bin/env python3
"""
Water-borne Disease Prediction System - Demonstration Analysis

This script demonstrates the water-borne disease prediction system using
synthetic data without requiring external dependencies.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path

# Set up directories
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visualizations')
os.makedirs(output_dir, exist_ok=True)

results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
os.makedirs(results_dir, exist_ok=True)


def generate_synthetic_data(n_samples=100):
    """
    Generate synthetic water quality and disease data for demonstration.
    """
    np.random.seed(42)
    
    # Generate water quality parameters
    data = {
        'pH': np.random.normal(7.2, 0.8, n_samples),
        'Temperature': np.random.normal(25, 5, n_samples),
        'Turbidity': np.random.exponential(5, n_samples),
        'DO': np.random.normal(8, 2, n_samples),  # Dissolved Oxygen
        'E.coli': np.random.exponential(50, n_samples),
        'Total_Coliforms': np.random.exponential(200, n_samples),
        'Nitrates': np.random.exponential(5, n_samples),
        'Phosphates': np.random.exponential(0.5, n_samples),
        'Rainfall': np.random.exponential(20, n_samples),
        'Humidity': np.random.normal(60, 15, n_samples),
    }
    
    # Add some correlations between parameters
    # Higher E.coli tends to occur with higher turbidity
    turbidity_factor = data['Turbidity'] / np.mean(data['Turbidity'])
    data['E.coli'] = data['E.coli'] * turbidity_factor
    
    # Lower DO tends to have higher bacterial counts
    do_factor = np.max(data['DO']) / data['DO']
    data['Total_Coliforms'] = data['Total_Coliforms'] * do_factor
    
    # Generate disease cases (correlated with water quality)
    # Higher E.coli -> more disease cases
    ecoli_normalized = data['E.coli'] / np.max(data['E.coli'])
    
    data['Cholera_Cases'] = np.random.poisson(ecoli_normalized * 5)
    data['Typhoid_Cases'] = np.random.poisson(ecoli_normalized * 3)
    data['Hepatitis_A_Cases'] = np.random.poisson(ecoli_normalized * 2)
    data['Dysentery_Cases'] = np.random.poisson(ecoli_normalized * 4)
    data['Diarrhea_Cases'] = np.random.poisson(ecoli_normalized * 8)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add categorical season data
    seasons = ['winter', 'spring', 'summer', 'monsoon', 'autumn']
    df['Season'] = np.random.choice(seasons, n_samples)
    
    return df


def map_columns_to_model_inputs(df):
    """
    Map the dataset columns to the expected model inputs.
    """
    # Print available columns for reference
    print("Available columns:")
    print(df.columns.tolist())
    
    # This mapping should match the actual dataset columns
    column_mapping = {
        # Water quality parameters
        'ph': 'pH',
        'temperature': 'Temperature',
        'turbidity': 'Turbidity',
        'dissolved_oxygen': 'DO',  # Dissolved Oxygen
        'ecoli_count': 'E.coli',
        'total_coliforms': 'Total_Coliforms',
        'nitrates': 'Nitrates',
        'phosphates': 'Phosphates',
        
        # Environmental factors
        'rainfall_last_7_days': 'Rainfall',
        'humidity': 'Humidity',
        'season': 'Season',
        
        # Disease data
        'cholera_cases_last_30_days': 'Cholera_Cases',
        'typhoid_cases_last_30_days': 'Typhoid_Cases',
        'hepatitis_a_cases_last_30_days': 'Hepatitis_A_Cases',
        'dysentery_cases_last_30_days': 'Dysentery_Cases',
        'diarrhea_cases_last_30_days': 'Diarrhea_Cases'
    }
    
    # Create a new dataframe with the mapped columns
    mapped_df = pd.DataFrame()
    
    # For each expected model input, try to find a corresponding column
    for model_col, dataset_col in column_mapping.items():
        if dataset_col in df.columns:
            mapped_df[model_col] = df[dataset_col]
        else:
            print(f"Warning: Could not find column {dataset_col} for {model_col}")
            # Use a default value or leave as NaN
            mapped_df[model_col] = np.nan
    
    # Fill missing values with reasonable defaults
    defaults = {
        'ph': 7.0,
        'temperature': 25.0,
        'turbidity': 5.0,
        'dissolved_oxygen': 8.0,
        'ecoli_count': 0.0,
        'total_coliforms': 0.0,
        'nitrates': 0.0,
        'phosphates': 0.0,
        'rainfall_last_7_days': 0.0,
        'humidity': 50.0,
        'season': 'summer',
        'cholera_cases_last_30_days': 0,
        'typhoid_cases_last_30_days': 0,
        'hepatitis_a_cases_last_30_days': 0,
        'dysentery_cases_last_30_days': 0,
        'diarrhea_cases_last_30_days': 0
    }
    
    for col, default in defaults.items():
        if col in mapped_df.columns and mapped_df[col].isna().any():
            mapped_df[col].fillna(default, inplace=True)
    
    return mapped_df


def run_predictions(df):
    """
    Run a simplified Random Forest model for water-borne disease prediction.
    """
    from sklearn.ensemble import RandomForestClassifier
    
    # Create a simplified model for demonstration
    print("Using simplified Random Forest model for predictions...")
    
    # Generate synthetic target values for training
    np.random.seed(42)
    X = df.select_dtypes(include=[np.number]).fillna(0).values  # Simple imputation for demo
    
    # Create synthetic target values (0=low risk, 1=high risk)
    # This is just for demonstration - in reality we'd use real disease data
    y = np.random.choice([0, 1], size=len(X), p=[0.7, 0.3])  # 30% high risk samples
    
    # Train a simple model
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    
    # Make predictions
    risk_scores = model.predict_proba(X)[:, 1]  # Probability of high risk
    
    # Generate results in the same format as the original model would
    results = []
    diseases = ['cholera', 'typhoid', 'hepatitis_a', 'dysentery', 'diarrhea']
    
    for i, row in enumerate(df.iterrows()):
        # Base risk on the model prediction
        base_risk = risk_scores[i]
        
        # Create disease-specific risks with some variation
        disease_risks = {}
        for disease in diseases:
            # Add some random variation to make each disease different
            variation = np.random.uniform(-0.2, 0.2)
            risk = max(0, min(1, base_risk + variation))
            
            # Determine risk level
            if risk < 0.3:
                risk_level = "Low"
            elif risk < 0.5:
                risk_level = "Medium"
            elif risk < 0.7:
                risk_level = "High"
            else:
                risk_level = "Critical"
                
            disease_risks[disease] = {
                "risk_score": float(round(risk, 2)),
                "risk_level": risk_level
            }
        
        # Determine overall risk based on maximum disease risk
        max_risk = max(d["risk_score"] for d in disease_risks.values())
        if max_risk < 0.3:
            overall_risk = "LOW"
        elif max_risk < 0.5:
            overall_risk = "MEDIUM"
        elif max_risk < 0.7:
            overall_risk = "HIGH"
        else:
            overall_risk = "CRITICAL"
        
        # Create the prediction result
        result = {
            "overall_risk": overall_risk,
            "disease_risks": disease_risks,
            "alerts": []
        }
        
        # Add alerts for high and critical risks
        for disease, risk_data in disease_risks.items():
            if risk_data["risk_level"] in ["High", "Critical"]:
                result["alerts"].append({
                    "severity": risk_data["risk_level"].lower(),
                    "disease": disease,
                    "message": f"{risk_data['risk_level']} risk of {disease} detected",
                    "recommended_actions": [
                        "Increase water quality monitoring",
                        "Consider public health advisory"
                    ]
                })
        
        results.append(result)
    
    return results


def visualize_results(df, predictions):
    """
    Create visualizations of the water quality data and prediction results.
    """
    # Set up the plotting style
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("viridis")
    
    # 1. Water Quality Parameters Distribution
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    axes = axes.flatten()
    
    water_params = ['ph', 'temperature', 'turbidity', 'dissolved_oxygen', 
                   'ecoli_count', 'total_coliforms', 'nitrates', 'phosphates']
    
    for i, param in enumerate(water_params):
        if param in df.columns:
            sns.histplot(df[param], kde=True, ax=axes[i])
            axes[i].set_title(f'Distribution of {param}')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'water_quality_distribution.png'))
    plt.close()
    
    # 2. Risk Level Distribution
    risk_levels = [pred['overall_risk'] for pred in predictions]
    plt.figure(figsize=(10, 6))
    sns.countplot(x=risk_levels)
    plt.title('Distribution of Overall Risk Levels')
    plt.xlabel('Risk Level')
    plt.ylabel('Count')
    plt.savefig(os.path.join(output_dir, 'risk_level_distribution.png'))
    plt.close()
    
    # 3. Disease Risk Scores
    diseases = ['cholera', 'typhoid', 'hepatitis_a', 'dysentery', 'diarrhea']
    disease_risks = {disease: [] for disease in diseases}
    
    for pred in predictions:
        for disease in diseases:
            if disease in pred['disease_risks']:
                disease_risks[disease].append(pred['disease_risks'][disease]['risk_score'])
            else:
                disease_risks[disease].append(0)
    
    disease_risk_df = pd.DataFrame(disease_risks)
    
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=disease_risk_df)
    plt.title('Disease Risk Score Distribution')
    plt.ylabel('Risk Score')
    plt.savefig(os.path.join(output_dir, 'disease_risk_boxplot.png'))
    plt.close()
    
    # 4. Correlation Heatmap
    corr_cols = ['ph', 'temperature', 'turbidity', 'dissolved_oxygen', 
                'ecoli_count', 'total_coliforms', 'nitrates', 'phosphates',
                'cholera_cases_last_30_days', 'typhoid_cases_last_30_days', 
                'hepatitis_a_cases_last_30_days', 'dysentery_cases_last_30_days', 
                'diarrhea_cases_last_30_days']
    
    # Filter to only include columns that exist in the dataframe
    corr_cols = [col for col in corr_cols if col in df.columns]
    
    if corr_cols:  # Only create heatmap if we have columns to correlate
        plt.figure(figsize=(14, 10))
        corr = df[corr_cols].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Correlation Between Water Parameters and Disease Cases')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'correlation_heatmap.png'))
        plt.close()
    
    # 5. E.coli vs Disease Cases Scatter Plots
    if 'ecoli_count' in df.columns:
        fig, axes = plt.subplots(len(diseases), 1, figsize=(12, 15))
        
        for i, disease in enumerate(diseases):
            case_col = f'{disease}_cases_last_30_days'
            if case_col in df.columns:
                sns.scatterplot(x='ecoli_count', y=case_col, data=df, ax=axes[i])
                axes[i].set_title(f'E.coli Count vs {disease.capitalize()} Cases')
                axes[i].set_xlabel('E.coli Count')
                axes[i].set_ylabel('Cases (Last 30 Days)')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'ecoli_vs_disease_cases.png'))
        plt.close()
    
    print(f"Visualizations saved to {output_dir}")


def save_results(predictions, output_path):
    """
    Save prediction results to a JSON file.
    """
    with open(output_path, 'w') as f:
        json.dump(predictions, f, indent=2)
    print(f"Results saved to {output_path}")


def print_header():
    print("\n" + "=" * 80)
    print("WATER-BORNE DISEASE PREDICTION SYSTEM - DEMONSTRATION ANALYSIS")
    print("=" * 80)
    print("This script will:")
    print("  1. Generate synthetic water quality and disease data")
    print("  2. Process the data and map it to our model inputs")
    print("  3. Run predictions using a simplified Random Forest model")
    print("  4. Generate visualizations of water quality and disease risks")
    print("  5. Save results to the 'results' directory")
    print("\nVisualizations will be saved to the 'visualizations' directory.")
    print("=" * 80 + "\n")


def main():
    print_header()
    
    # Generate synthetic data
    print("Generating synthetic water quality and disease data...")
    df = generate_synthetic_data(n_samples=100)
    print(f"Generated dataset with {len(df)} samples")
    
    # Map columns to model inputs
    print("\nMapping columns to model inputs...")
    mapped_df = map_columns_to_model_inputs(df)
    
    # Run predictions
    print("\nRunning disease risk predictions...")
    predictions = run_predictions(mapped_df)
    print(f"Generated {len(predictions)} prediction results")
    
    # Visualize results
    print("\nCreating visualizations...")
    visualize_results(mapped_df, predictions)
    
    # Save results
    output_path = os.path.join(results_dir, "synthetic_data_predictions.json")
    save_results(predictions, output_path)
    
    print("\nAnalysis complete!")
    print(f"Visualizations are available in: {output_dir}")
    print(f"Prediction results are available in: {results_dir}")


if __name__ == "__main__":
    main()