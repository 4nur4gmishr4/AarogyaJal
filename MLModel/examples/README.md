# Water-Borne Disease Prediction System - Examples

This directory contains example scripts demonstrating how to use the water-borne disease prediction system with different datasets and scenarios.

## Available Examples

### Kaggle Dataset Integration

`kaggle_dataset_example.py` - Demonstrates how to use the Kaggle water pollution and disease dataset with our prediction model.

This example shows the workflow of:
1. Downloading the dataset using kagglehub
2. Processing and mapping the data to our model inputs
3. Running predictions using our ensemble model
4. Visualizing the results with matplotlib and seaborn
5. Saving the prediction results

## Running the Examples

To see the demonstration workflow without executing any commands:

```bash
python examples/kaggle_dataset_example.py
```

To actually run the analysis with the Kaggle dataset:

```bash
python run_kaggle_analysis.py
```

## Kaggle Dataset Information

The "water-pollution-and-disease" dataset from Kaggle contains water quality parameters and associated disease cases, which is ideal for testing our prediction model. The dataset includes:

- Water quality measurements (pH, temperature, turbidity, etc.)
- Bacterial contamination indicators (E.coli, coliforms)
- Disease case counts for various water-borne diseases

## Visualization Outputs

When running the Kaggle dataset analysis, the following visualizations will be generated in the `visualizations/` directory:

1. **Water Quality Parameter Distributions** - Histograms showing the distribution of each water quality parameter
2. **Risk Level Distribution** - Count plot of predicted risk levels
3. **Disease Risk Score Comparisons** - Box plots comparing risk scores across different diseases
4. **Correlation Heatmap** - Correlation between water parameters and disease cases
5. **E.coli vs Disease Cases** - Scatter plots showing the relationship between E.coli counts and disease cases

## Adding New Examples

To add new examples to this directory:

1. Create a new Python script in the `examples/` directory
2. Update this README.md to include information about your example
3. Follow the pattern of existing examples for consistency