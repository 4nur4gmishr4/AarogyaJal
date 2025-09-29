#!/usr/bin/env python3
"""
Enhanced Visualizations for Water-borne Disease Prediction System

This script creates detailed visualizations with different parameters
to provide deeper insights into water quality and disease relationships.
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path
from matplotlib.gridspec import GridSpec
from sklearn.preprocessing import StandardScaler

# Set up directories
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'enhanced_visualizations')
os.makedirs(output_dir, exist_ok=True)

# Load existing results if available
results_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results/synthetic_data_predictions.json')

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("viridis")

# Set font sizes for better readability
PLOT_TITLE_SIZE = 16
AXIS_LABEL_SIZE = 12
TICK_SIZE = 10


def load_data():
    """
    Load synthetic data or generate new data if needed.
    """
    try:
        # Try to load existing synthetic data from demo_analysis.py
        from demo_analysis import generate_synthetic_data
        print("Loading synthetic data generator...")
        df = generate_synthetic_data(n_samples=200)  # Generate more samples for better visualization
        print(f"Generated dataset with {len(df)} samples")
        return df
    except ImportError:
        print("Could not import generate_synthetic_data, creating new synthetic data...")
        # Generate our own synthetic data
        np.random.seed(42)
        
        # Generate water quality parameters
        data = {
            'pH': np.random.normal(7.2, 0.8, 200),
            'Temperature': np.random.normal(25, 5, 200),
            'Turbidity': np.random.exponential(5, 200),
            'DO': np.random.normal(8, 2, 200),  # Dissolved Oxygen
            'E.coli': np.random.exponential(50, 200),
            'Total_Coliforms': np.random.exponential(200, 200),
            'Nitrates': np.random.exponential(5, 200),
            'Phosphates': np.random.exponential(0.5, 200),
            'Rainfall': np.random.exponential(20, 200),
            'Humidity': np.random.normal(60, 15, 200),
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
        df['Season'] = np.random.choice(seasons, 200)
        
        return df


def load_predictions():
    """
    Load prediction results if available, otherwise return None.
    """
    if os.path.exists(results_path):
        try:
            with open(results_path, 'r') as f:
                predictions = json.load(f)
            print(f"Loaded {len(predictions)} prediction results from {results_path}")
            return predictions
        except Exception as e:
            print(f"Error loading predictions: {e}")
            return None
    else:
        print(f"No prediction results found at {results_path}")
        return None


def create_water_quality_distribution_plots(df):
    """
    Create enhanced water quality parameter distribution plots.
    """
    print("Creating water quality distribution plots...")
    
    # Create a figure with a grid layout
    fig = plt.figure(figsize=(20, 15))
    gs = GridSpec(3, 3, figure=fig)
    
    # Water quality parameters to plot
    params = [
        ('pH', 'pH Level', gs[0, 0]),
        ('Temperature', 'Temperature (°C)', gs[0, 1]),
        ('Turbidity', 'Turbidity (NTU)', gs[0, 2]),
        ('DO', 'Dissolved Oxygen (mg/L)', gs[1, 0]),
        ('E.coli', 'E.coli (CFU/100mL)', gs[1, 1]),
        ('Total_Coliforms', 'Total Coliforms (CFU/100mL)', gs[1, 2]),
        ('Nitrates', 'Nitrates (mg/L)', gs[2, 0]),
        ('Phosphates', 'Phosphates (mg/L)', gs[2, 1])
    ]
    
    for param, label, position in params:
        if param in df.columns:
            ax = fig.add_subplot(position)
            
            # Create histogram with KDE
            sns.histplot(df[param], kde=True, ax=ax, color='steelblue')
            
            # Add vertical lines for WHO guidelines or typical thresholds
            if param == 'pH':
                ax.axvline(x=6.5, color='r', linestyle='--', alpha=0.7, label='WHO Lower Limit')
                ax.axvline(x=8.5, color='r', linestyle='--', alpha=0.7, label='WHO Upper Limit')
            elif param == 'Turbidity':
                ax.axvline(x=5, color='r', linestyle='--', alpha=0.7, label='WHO Guideline')
            elif param == 'E.coli':
                ax.axvline(x=0, color='r', linestyle='--', alpha=0.7, label='WHO Guideline (0)')
            
            # Add mean and median lines
            mean_val = df[param].mean()
            median_val = df[param].median()
            ax.axvline(x=mean_val, color='g', linestyle='-', alpha=0.7, label=f'Mean: {mean_val:.2f}')
            ax.axvline(x=median_val, color='purple', linestyle='-.', alpha=0.7, label=f'Median: {median_val:.2f}')
            
            # Set titles and labels
            ax.set_title(f'Distribution of {label}', fontsize=PLOT_TITLE_SIZE)
            ax.set_xlabel(label, fontsize=AXIS_LABEL_SIZE)
            ax.set_ylabel('Frequency', fontsize=AXIS_LABEL_SIZE)
            ax.tick_params(labelsize=TICK_SIZE)
            ax.legend(fontsize=TICK_SIZE)
    
    # Add a title for the entire figure
    fig.suptitle('Water Quality Parameters Distribution', fontsize=PLOT_TITLE_SIZE+4, y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(os.path.join(output_dir, 'enhanced_water_quality_distribution.png'), dpi=300)
    plt.close()


def create_disease_correlation_matrix(df):
    """
    Create an enhanced correlation matrix between water parameters and disease cases.
    """
    print("Creating disease correlation matrix...")
    
    # Select relevant columns
    water_params = ['pH', 'Temperature', 'Turbidity', 'DO', 'E.coli', 'Total_Coliforms', 'Nitrates', 'Phosphates']
    disease_cases = ['Cholera_Cases', 'Typhoid_Cases', 'Hepatitis_A_Cases', 'Dysentery_Cases', 'Diarrhea_Cases']
    
    # Filter to only include columns that exist in the dataframe
    water_params = [col for col in water_params if col in df.columns]
    disease_cases = [col for col in disease_cases if col in df.columns]
    
    if not water_params or not disease_cases:
        print("Not enough data for correlation matrix")
        return
    
    # Create a subset dataframe with just the columns we need
    corr_df = df[water_params + disease_cases]
    
    # Calculate the correlation matrix
    corr = corr_df.corr()
    
    # Create a figure
    plt.figure(figsize=(16, 12))
    
    # Create a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=bool)
    mask[np.triu_indices_from(mask, k=1)] = True
    
    # Create the heatmap with annotations
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', 
                annot_kws={"size": 10}, linewidths=0.5)
    
    plt.title('Correlation Between Water Parameters and Disease Cases', fontsize=PLOT_TITLE_SIZE)
    plt.xticks(fontsize=TICK_SIZE, rotation=45, ha='right')
    plt.yticks(fontsize=TICK_SIZE)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'enhanced_correlation_matrix.png'), dpi=300)
    plt.close()


def create_parameter_vs_disease_plots(df):
    """
    Create scatter plots showing relationships between key water parameters and disease cases.
    """
    print("Creating parameter vs disease plots...")
    
    # Key parameters that typically affect disease rates
    key_params = ['E.coli', 'Turbidity', 'DO', 'pH']
    disease_cases = ['Cholera_Cases', 'Typhoid_Cases', 'Hepatitis_A_Cases', 'Dysentery_Cases', 'Diarrhea_Cases']
    
    # Filter to only include columns that exist in the dataframe
    key_params = [col for col in key_params if col in df.columns]
    disease_cases = [col for col in disease_cases if col in df.columns]
    
    if not key_params or not disease_cases:
        print("Not enough data for parameter vs disease plots")
        return
    
    # For each key parameter, create a figure with subplots for each disease
    for param in key_params:
        fig, axes = plt.subplots(len(disease_cases), 1, figsize=(12, 4*len(disease_cases)))
        
        for i, disease in enumerate(disease_cases):
            # Create scatter plot with regression line
            sns.regplot(x=param, y=disease, data=df, ax=axes[i], 
                       scatter_kws={"alpha": 0.6, "s": 50}, 
                       line_kws={"color": "red", "alpha": 0.7})
            
            # Calculate correlation coefficient
            corr = df[[param, disease]].corr().iloc[0, 1]
            
            # Set titles and labels
            axes[i].set_title(f'{param} vs {disease} (Correlation: {corr:.2f})', fontsize=PLOT_TITLE_SIZE)
            axes[i].set_xlabel(param, fontsize=AXIS_LABEL_SIZE)
            axes[i].set_ylabel(disease, fontsize=AXIS_LABEL_SIZE)
            axes[i].tick_params(labelsize=TICK_SIZE)
            
            # Add grid for better readability
            axes[i].grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'enhanced_{param}_vs_diseases.png'), dpi=300)
        plt.close()


def create_seasonal_analysis(df):
    """
    Create visualizations showing seasonal patterns in water quality and disease cases.
    """
    print("Creating seasonal analysis plots...")
    
    if 'Season' not in df.columns:
        print("Season data not available for seasonal analysis")
        return
    
    # Parameters to analyze by season
    water_params = ['pH', 'Temperature', 'Turbidity', 'DO', 'E.coli', 'Total_Coliforms']
    disease_cases = ['Cholera_Cases', 'Typhoid_Cases', 'Hepatitis_A_Cases', 'Dysentery_Cases', 'Diarrhea_Cases']
    
    # Filter to only include columns that exist in the dataframe
    water_params = [col for col in water_params if col in df.columns]
    disease_cases = [col for col in disease_cases if col in df.columns]
    
    if not water_params or not disease_cases:
        print("Not enough data for seasonal analysis")
        return
    
    # 1. Water Parameters by Season
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    for i, param in enumerate(water_params[:6]):  # Limit to 6 parameters for readability
        sns.boxplot(x='Season', y=param, data=df, ax=axes[i])
        axes[i].set_title(f'{param} by Season', fontsize=PLOT_TITLE_SIZE)
        axes[i].set_xlabel('Season', fontsize=AXIS_LABEL_SIZE)
        axes[i].set_ylabel(param, fontsize=AXIS_LABEL_SIZE)
        axes[i].tick_params(labelsize=TICK_SIZE)
        axes[i].set_xticklabels(axes[i].get_xticklabels(), rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'seasonal_water_parameters.png'), dpi=300)
    plt.close()
    
    # 2. Disease Cases by Season
    plt.figure(figsize=(14, 10))
    
    # Melt the dataframe to get it in the right format for a grouped bar chart
    melted_df = pd.melt(df, id_vars=['Season'], value_vars=disease_cases,
                        var_name='Disease', value_name='Cases')
    
    # Create the grouped bar chart
    sns.barplot(x='Season', y='Cases', hue='Disease', data=melted_df)
    
    plt.title('Disease Cases by Season', fontsize=PLOT_TITLE_SIZE)
    plt.xlabel('Season', fontsize=AXIS_LABEL_SIZE)
    plt.ylabel('Average Number of Cases', fontsize=AXIS_LABEL_SIZE)
    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    plt.legend(fontsize=TICK_SIZE)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'seasonal_disease_cases.png'), dpi=300)
    plt.close()


def create_risk_analysis_plots(predictions, df):
    """
    Create visualizations analyzing the risk predictions.
    """
    if not predictions:
        print("No prediction data available for risk analysis")
        return
    
    print("Creating risk analysis plots...")
    
    # Extract risk levels and scores
    overall_risks = [pred['overall_risk'] for pred in predictions]
    
    # 1. Overall Risk Distribution
    plt.figure(figsize=(12, 8))
    risk_counts = pd.Series(overall_risks).value_counts().sort_index()
    
    # Define color map for risk levels
    colors = {'LOW': 'green', 'MEDIUM': 'yellow', 'HIGH': 'orange', 'CRITICAL': 'red'}
    bar_colors = [colors.get(risk, 'blue') for risk in risk_counts.index]
    
    # Create bar chart
    ax = sns.barplot(x=risk_counts.index, y=risk_counts.values, palette=bar_colors)
    
    # Add count labels on top of bars
    for i, count in enumerate(risk_counts.values):
        ax.text(i, count + 0.5, str(count), ha='center', fontsize=TICK_SIZE)
    
    plt.title('Distribution of Overall Risk Levels', fontsize=PLOT_TITLE_SIZE)
    plt.xlabel('Risk Level', fontsize=AXIS_LABEL_SIZE)
    plt.ylabel('Count', fontsize=AXIS_LABEL_SIZE)
    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'enhanced_risk_distribution.png'), dpi=300)
    plt.close()
    
    # 2. Disease-specific Risk Scores
    diseases = ['cholera', 'typhoid', 'hepatitis_a', 'dysentery', 'diarrhea']
    disease_risks = {disease: [] for disease in diseases}
    
    for pred in predictions:
        for disease in diseases:
            if disease in pred['disease_risks']:
                disease_risks[disease].append(pred['disease_risks'][disease]['risk_score'])
            else:
                disease_risks[disease].append(0)
    
    disease_risk_df = pd.DataFrame(disease_risks)
    
    # Create violin plots for risk score distribution
    plt.figure(figsize=(14, 10))
    
    # Use a custom palette for diseases
    disease_palette = sns.color_palette("husl", len(diseases))
    
    # Create violin plot with inner boxplot
    ax = sns.violinplot(data=disease_risk_df, palette=disease_palette, inner="box")
    
    # Add swarm plot for individual data points
    sns.swarmplot(data=disease_risk_df, color="white", edgecolor="gray", size=2, alpha=0.5)
    
    # Add horizontal lines for risk thresholds
    plt.axhline(y=0.3, color='green', linestyle='--', alpha=0.7, label='Low-Medium Threshold')
    plt.axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='Medium-High Threshold')
    plt.axhline(y=0.7, color='red', linestyle='--', alpha=0.7, label='High-Critical Threshold')
    
    plt.title('Disease Risk Score Distribution', fontsize=PLOT_TITLE_SIZE)
    plt.ylabel('Risk Score', fontsize=AXIS_LABEL_SIZE)
    plt.xlabel('Disease', fontsize=AXIS_LABEL_SIZE)
    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    plt.legend(fontsize=TICK_SIZE)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'enhanced_disease_risk_distribution.png'), dpi=300)
    plt.close()
    
    # 3. Risk Level by Water Quality Parameter
    if len(df) == len(predictions):  # Only if we can match predictions to data points
        # Add risk level to the dataframe
        df_with_risk = df.copy()
        df_with_risk['Risk_Level'] = overall_risks
        
        # Key parameters to analyze
        key_params = ['E.coli', 'Turbidity', 'DO', 'pH']
        key_params = [param for param in key_params if param in df_with_risk.columns]
        
        if key_params:
            fig, axes = plt.subplots(len(key_params), 1, figsize=(12, 5*len(key_params)))
            if len(key_params) == 1:
                axes = [axes]  # Make sure axes is always a list
                
            for i, param in enumerate(key_params):
                # Create boxplot
                sns.boxplot(x='Risk_Level', y=param, data=df_with_risk, 
                           order=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                           palette=['green', 'yellow', 'orange', 'red'],
                           ax=axes[i])
                
                # Add individual data points
                sns.stripplot(x='Risk_Level', y=param, data=df_with_risk,
                            order=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
                            color='black', alpha=0.5, jitter=True, size=3,
                            ax=axes[i])
                
                axes[i].set_title(f'{param} by Risk Level', fontsize=PLOT_TITLE_SIZE)
                axes[i].set_xlabel('Risk Level', fontsize=AXIS_LABEL_SIZE)
                axes[i].set_ylabel(param, fontsize=AXIS_LABEL_SIZE)
                axes[i].tick_params(labelsize=TICK_SIZE)
            
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'water_parameters_by_risk.png'), dpi=300)
            plt.close()


def create_alert_analysis(predictions):
    """
    Analyze and visualize the alerts generated by the system.
    """
    if not predictions:
        print("No prediction data available for alert analysis")
        return
    
    print("Creating alert analysis plots...")
    
    # Extract alerts from predictions
    all_alerts = []
    for pred in predictions:
        for alert in pred.get('alerts', []):
            all_alerts.append(alert)
    
    if not all_alerts:
        print("No alerts found in predictions")
        return
    
    # Convert alerts to DataFrame for easier analysis
    alert_df = pd.DataFrame(all_alerts)
    
    # 1. Alert Count by Disease
    plt.figure(figsize=(12, 8))
    disease_counts = alert_df['disease'].value_counts()
    
    # Create bar chart with custom colors
    sns.barplot(x=disease_counts.index, y=disease_counts.values, palette='Reds_r')
    
    # Add count labels on top of bars
    for i, count in enumerate(disease_counts.values):
        plt.text(i, count + 0.1, str(count), ha='center', fontsize=TICK_SIZE)
    
    plt.title('Number of Alerts by Disease', fontsize=PLOT_TITLE_SIZE)
    plt.xlabel('Disease', fontsize=AXIS_LABEL_SIZE)
    plt.ylabel('Number of Alerts', fontsize=AXIS_LABEL_SIZE)
    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'alerts_by_disease.png'), dpi=300)
    plt.close()
    
    # 2. Alert Count by Severity
    plt.figure(figsize=(10, 8))
    severity_counts = alert_df['severity'].value_counts()
    
    # Define color map for severity levels
    severity_colors = {'high': 'orange', 'critical': 'red'}
    bar_colors = [severity_colors.get(severity, 'blue') for severity in severity_counts.index]
    
    # Create bar chart
    ax = sns.barplot(x=severity_counts.index, y=severity_counts.values, palette=bar_colors)
    
    # Add count labels on top of bars
    for i, count in enumerate(severity_counts.values):
        ax.text(i, count + 0.1, str(count), ha='center', fontsize=TICK_SIZE)
    
    plt.title('Number of Alerts by Severity', fontsize=PLOT_TITLE_SIZE)
    plt.xlabel('Severity', fontsize=AXIS_LABEL_SIZE)
    plt.ylabel('Number of Alerts', fontsize=AXIS_LABEL_SIZE)
    plt.xticks(fontsize=TICK_SIZE)
    plt.yticks(fontsize=TICK_SIZE)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'alerts_by_severity.png'), dpi=300)
    plt.close()
    
    # 3. Disease-Severity Heatmap
    if 'disease' in alert_df.columns and 'severity' in alert_df.columns:
        # Create a cross-tabulation of disease and severity
        disease_severity = pd.crosstab(alert_df['disease'], alert_df['severity'])
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(disease_severity, annot=True, fmt='d', cmap='YlOrRd')
        
        plt.title('Disease-Severity Alert Distribution', fontsize=PLOT_TITLE_SIZE)
        plt.xlabel('Severity', fontsize=AXIS_LABEL_SIZE)
        plt.ylabel('Disease', fontsize=AXIS_LABEL_SIZE)
        plt.xticks(fontsize=TICK_SIZE)
        plt.yticks(fontsize=TICK_SIZE)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'disease_severity_heatmap.png'), dpi=300)
        plt.close()


def print_header():
    print("\n" + "=" * 80)
    print("WATER-BORNE DISEASE PREDICTION SYSTEM - ENHANCED VISUALIZATIONS")
    print("=" * 80)
    print("This script will:")
    print("  1. Load or generate synthetic water quality and disease data")
    print("  2. Create detailed visualizations with different parameters")
    print("  3. Analyze relationships between water quality and disease risks")
    print("  4. Generate seasonal analysis of water quality and disease cases")
    print("  5. Create detailed risk and alert analysis visualizations")
    print("\nEnhanced visualizations will be saved to the 'enhanced_visualizations' directory.")
    print("=" * 80 + "\n")


def main():
    print_header()
    
    # Load data
    df = load_data()
    
    # Load predictions if available
    predictions = load_predictions()
    
    # Create enhanced visualizations
    create_water_quality_distribution_plots(df)
    create_disease_correlation_matrix(df)
    create_parameter_vs_disease_plots(df)
    create_seasonal_analysis(df)
    
    # Create risk and alert analysis if predictions are available
    if predictions:
        create_risk_analysis_plots(predictions, df)
        create_alert_analysis(predictions)
    
    print("\nEnhanced visualization generation complete!")
    print(f"All visualizations are available in: {output_dir}")


if __name__ == "__main__":
    main()