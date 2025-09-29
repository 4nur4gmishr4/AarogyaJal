#!/usr/bin/env python3
"""
Water-borne Disease Prediction System - Kaggle Dataset Analysis

This script runs the analysis on the Kaggle water pollution and disease dataset,
generating predictions and visualizations using a simplified ML model.
"""

import os
import sys
# Import the main function directly
from data.process_kaggle_data import main as process_kaggle_data


def print_header():
    print("\n" + "=" * 80)
    print("WATER-BORNE DISEASE PREDICTION SYSTEM - KAGGLE DATASET ANALYSIS")
    print("=" * 80)
    print("This script will:")
    print("  1. Download the Kaggle dataset 'water-pollution-and-disease'")
    print("  2. Process the data and map it to our model inputs")
    print("  3. Run predictions using our ensemble model")
    print("  4. Generate visualizations of water quality and disease risks")
    print("  5. Save results to the 'results' directory")
    print("\nVisualizations will be saved to the 'visualizations' directory.")
    print("=" * 80 + "\n")


def check_requirements():
    try:
        import kagglehub
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        return True
    except ImportError as e:
        print(f"Error: Missing required package - {e.name}")
        print("\nPlease install the required packages:")
        print("pip install kagglehub pandas numpy matplotlib seaborn")
        return False


def main():
    print_header()
    
    if not check_requirements():
        return
    
    print("Starting data processing and analysis...\n")
    process_kaggle_data()
    
    # Check if visualizations were created
    vis_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'visualizations')
    if os.path.exists(vis_dir) and os.listdir(vis_dir):
        print(f"\nAnalysis complete! Visualizations are available in: {vis_dir}")
        print("You can view the following visualization files:")
        for file in os.listdir(vis_dir):
            print(f"  - {file}")
    else:
        print("\nAnalysis complete, but no visualizations were generated.")
    
    # Check if results were saved
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
    if os.path.exists(results_dir) and os.listdir(results_dir):
        print(f"\nPrediction results are available in: {results_dir}")
        print("You can view the following result files:")
        for file in os.listdir(results_dir):
            print(f"  - {file}")
    else:
        print("\nAnalysis complete, but no result files were generated.")


if __name__ == "__main__":
    main()