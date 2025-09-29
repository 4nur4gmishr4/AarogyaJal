#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Synthetic Data Generator for Water-Borne Disease Prediction System

This module generates synthetic data for training and testing the
Water-Borne Disease Prediction System. It creates realistic water quality,
environmental, and disease occurrence data based on domain knowledge.
"""

import numpy as np
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import random
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SyntheticDataGenerator:
    """
    A class for generating synthetic data for water-borne disease prediction.
    """
    
    def __init__(self, seed=42):
        """
        Initialize the SyntheticDataGenerator with default parameters.
        
        Args:
            seed: Random seed for reproducibility
        """
        # Set random seed for reproducibility
        np.random.seed(seed)
        random.seed(seed)
        
        # Define disease thresholds and parameters
        self.disease_params = {
            'cholera': {
                'ecoli_threshold': 50,
                'ph_range': (6.0, 9.0),
                'temp_range': (25, 35),
                'season_weights': {'winter': 0.2, 'spring': 0.3, 'summer': 0.6, 'monsoon': 0.9, 'autumn': 0.4}
            },
            'typhoid': {
                'coliforms_threshold': 100,
                'turbidity_threshold': 10,
                'season_weights': {'winter': 0.3, 'spring': 0.4, 'summer': 0.7, 'monsoon': 0.8, 'autumn': 0.5}
            },
            'hepatitis_a': {
                'ecoli_threshold': 30,
                'phosphates_threshold': 0.5,
                'season_weights': {'winter': 0.4, 'spring': 0.5, 'summer': 0.6, 'monsoon': 0.7, 'autumn': 0.5}
            },
            'dysentery': {
                'ecoli_threshold': 40,
                'turbidity_threshold': 15,
                'season_weights': {'winter': 0.3, 'spring': 0.4, 'summer': 0.7, 'monsoon': 0.8, 'autumn': 0.5}
            },
            'diarrhea': {
                'ecoli_threshold': 20,
                'coliforms_threshold': 50,
                'season_weights': {'winter': 0.4, 'spring': 0.5, 'summer': 0.7, 'monsoon': 0.9, 'autumn': 0.6}
            }
        }
        
        # Define parameter ranges
        self.param_ranges = {
            'pH': (5.5, 9.5),
            'temperature': (15, 40),
            'turbidity': (0, 100),
            'dissolved_oxygen': (0, 15),
            'ecoli_count': (0, 500),
            'total_coliforms': (0, 1000),
            'nitrates': (0, 50),
            'phosphates': (0, 10),
            'rainfall_last_7_days': (0, 200),
            'humidity': (20, 100),
            'population_density': (100, 10000)
        }
        
        # Define seasons
        self.seasons = ['winter', 'spring', 'summer', 'monsoon', 'autumn']
        
        # Define districts and states for location data
        self.districts = [
            'Kamrup', 'Dibrugarh', 'Jorhat', 'Sivasagar', 'Tinsukia',
            'Darrang', 'Nagaon', 'Sonitpur', 'Cachar', 'Karimganj'
        ]
        
        self.states = ['Assam']
        
        # Define risk level thresholds
        self.risk_thresholds = {
            'Low': 0.3,
            'Medium': 0.5,
            'High': 0.7,
            'Critical': 1.0
        }
    
    def generate_single_sample(self, season=None, high_risk=False):
        """
        Generate a single sample of water quality and environmental data.
        
        Args:
            season: Optional season to use (if None, a random season is chosen)
            high_risk: Whether to generate a high-risk sample
            
        Returns:
            Dictionary containing a single data sample
        """
        # Choose a random season if not specified
        if season is None:
            season = random.choice(self.seasons)
        
        # Generate water quality parameters
        if high_risk:
            # Generate parameters that are likely to indicate high risk
            ecoli_count = np.random.uniform(100, 500)
            total_coliforms = np.random.uniform(300, 1000)
            turbidity = np.random.uniform(30, 100)
            dissolved_oxygen = np.random.uniform(0, 5)
            nitrates = np.random.uniform(20, 50)
            phosphates = np.random.uniform(3, 10)
        else:
            # Generate normal parameters
            ecoli_count = np.random.uniform(0, 100)
            total_coliforms = np.random.uniform(0, 300)
            turbidity = np.random.uniform(0, 30)
            dissolved_oxygen = np.random.uniform(5, 15)
            nitrates = np.random.uniform(0, 20)
            phosphates = np.random.uniform(0, 3)
        
        # Generate other parameters
        pH = np.random.uniform(*self.param_ranges['pH'])
        temperature = np.random.uniform(*self.param_ranges['temperature'])
        
        # Adjust parameters based on season
        if season == 'monsoon':
            rainfall_last_7_days = np.random.uniform(50, 200)
            humidity = np.random.uniform(70, 100)
            # Increase turbidity during monsoon
            turbidity *= 1.5
        elif season == 'summer':
            rainfall_last_7_days = np.random.uniform(0, 50)
            humidity = np.random.uniform(30, 70)
            # Increase temperature during summer
            temperature = np.random.uniform(30, 40)
        elif season == 'winter':
            rainfall_last_7_days = np.random.uniform(0, 20)
            humidity = np.random.uniform(20, 50)
            # Decrease temperature during winter
            temperature = np.random.uniform(15, 25)
        else:  # spring or autumn
            rainfall_last_7_days = np.random.uniform(10, 100)
            humidity = np.random.uniform(40, 80)
        
        # Generate population density
        population_density = np.random.uniform(*self.param_ranges['population_density'])
        
        # Generate historical disease cases
        if high_risk:
            cholera_cases = np.random.randint(5, 20)
            typhoid_cases = np.random.randint(5, 15)
            diarrhea_cases = np.random.randint(20, 50)
        else:
            cholera_cases = np.random.randint(0, 5)
            typhoid_cases = np.random.randint(0, 5)
            diarrhea_cases = np.random.randint(0, 20)
        
        # Generate location data
        district = random.choice(self.districts)
        state = random.choice(self.states)
        latitude = 26.0 + np.random.uniform(-0.5, 0.5)  # Approximate latitude for Assam
        longitude = 92.0 + np.random.uniform(-1.0, 1.0)  # Approximate longitude for Assam
        
        # Create sample
        sample = {
            'water_quality': {
                'pH': round(pH, 2),
                'temperature': round(temperature, 2),
                'turbidity': round(turbidity, 2),
                'dissolved_oxygen': round(dissolved_oxygen, 2),
                'ecoli_count': round(ecoli_count, 2),
                'total_coliforms': round(total_coliforms, 2),
                'nitrates': round(nitrates, 2),
                'phosphates': round(phosphates, 2)
            },
            'environmental': {
                'rainfall_last_7_days': round(rainfall_last_7_days, 2),
                'humidity': round(humidity, 2),
                'season': season,
                'population_density': round(population_density, 2)
            },
            'historical': {
                'cholera_cases_last_30_days': cholera_cases,
                'typhoid_cases_last_30_days': typhoid_cases,
                'diarrhea_cases_last_30_days': diarrhea_cases
            },
            'location': {
                'latitude': round(latitude, 4),
                'longitude': round(longitude, 4),
                'district': district,
                'state': state
            }
        }
        
        return sample
    
    def calculate_disease_risks(self, sample):
        """
        Calculate disease risks based on water quality and environmental parameters.
        
        Args:
            sample: Dictionary containing water quality and environmental data
            
        Returns:
            Dictionary containing disease risks
        """
        # Extract parameters
        water_quality = sample['water_quality']
        environmental = sample['environmental']
        historical = sample['historical']
        
        # Calculate risk for each disease
        disease_risks = {}
        
        # Cholera risk
        cholera_risk = self._calculate_cholera_risk(
            water_quality['ecoli_count'],
            water_quality['pH'],
            water_quality['temperature'],
            environmental['season'],
            historical['cholera_cases_last_30_days']
        )
        disease_risks['cholera'] = {
            'risk_score': round(cholera_risk, 4),
            'risk_level': self._get_risk_level(cholera_risk)
        }
        
        # Typhoid risk
        typhoid_risk = self._calculate_typhoid_risk(
            water_quality['total_coliforms'],
            water_quality['turbidity'],
            environmental['season'],
            historical['typhoid_cases_last_30_days']
        )
        disease_risks['typhoid'] = {
            'risk_score': round(typhoid_risk, 4),
            'risk_level': self._get_risk_level(typhoid_risk)
        }
        
        # Hepatitis A risk
        hepatitis_risk = self._calculate_hepatitis_risk(
            water_quality['ecoli_count'],
            water_quality['phosphates'],
            environmental['season']
        )
        disease_risks['hepatitis_a'] = {
            'risk_score': round(hepatitis_risk, 4),
            'risk_level': self._get_risk_level(hepatitis_risk)
        }
        
        # Dysentery risk
        dysentery_risk = self._calculate_dysentery_risk(
            water_quality['ecoli_count'],
            water_quality['turbidity'],
            environmental['season']
        )
        disease_risks['dysentery'] = {
            'risk_score': round(dysentery_risk, 4),
            'risk_level': self._get_risk_level(dysentery_risk)
        }
        
        # Diarrhea risk
        diarrhea_risk = self._calculate_diarrhea_risk(
            water_quality['ecoli_count'],
            water_quality['total_coliforms'],
            environmental['season'],
            historical['diarrhea_cases_last_30_days']
        )
        disease_risks['diarrhea'] = {
            'risk_score': round(diarrhea_risk, 4),
            'risk_level': self._get_risk_level(diarrhea_risk)
        }
        
        # Calculate overall risk
        risk_scores = [risk['risk_score'] for risk in disease_risks.values()]
        max_risk = max(risk_scores)
        overall_risk = self._get_risk_level(max_risk).upper()
        
        return {
            'overall_risk': overall_risk,
            'disease_risks': disease_risks
        }
    
    def _calculate_cholera_risk(self, ecoli_count, pH, temperature, season, historical_cases):
        """
        Calculate cholera risk based on parameters.
        """
        # Base risk from E. coli count
        base_risk = min(1.0, ecoli_count / self.disease_params['cholera']['ecoli_threshold'])
        
        # Adjust for pH (cholera thrives in alkaline conditions)
        if 7.0 <= pH <= 9.0:
            ph_factor = 1.2
        else:
            ph_factor = 0.8
        
        # Adjust for temperature (cholera thrives in warm water)
        if 25 <= temperature <= 35:
            temp_factor = 1.3
        else:
            temp_factor = 0.7
        
        # Adjust for season
        season_factor = self.disease_params['cholera']['season_weights'].get(season.lower(), 0.5)
        
        # Adjust for historical cases
        history_factor = min(1.5, 1.0 + (historical_cases / 20))
        
        # Calculate final risk
        risk = base_risk * ph_factor * temp_factor * season_factor * history_factor
        
        # Cap at 1.0
        return min(1.0, risk)
    
    def _calculate_typhoid_risk(self, total_coliforms, turbidity, season, historical_cases):
        """
        Calculate typhoid risk based on parameters.
        """
        # Base risk from total coliforms
        base_risk = min(1.0, total_coliforms / self.disease_params['typhoid']['coliforms_threshold'])
        
        # Adjust for turbidity
        turbidity_factor = min(1.5, turbidity / self.disease_params['typhoid']['turbidity_threshold'])
        
        # Adjust for season
        season_factor = self.disease_params['typhoid']['season_weights'].get(season.lower(), 0.5)
        
        # Adjust for historical cases
        history_factor = min(1.5, 1.0 + (historical_cases / 15))
        
        # Calculate final risk
        risk = base_risk * turbidity_factor * season_factor * history_factor
        
        # Cap at 1.0
        return min(1.0, risk)
    
    def _calculate_hepatitis_risk(self, ecoli_count, phosphates, season):
        """
        Calculate hepatitis A risk based on parameters.
        """
        # Base risk from E. coli count
        base_risk = min(1.0, ecoli_count / self.disease_params['hepatitis_a']['ecoli_threshold'])
        
        # Adjust for phosphates
        phosphate_factor = min(1.5, phosphates / self.disease_params['hepatitis_a']['phosphates_threshold'])
        
        # Adjust for season
        season_factor = self.disease_params['hepatitis_a']['season_weights'].get(season.lower(), 0.5)
        
        # Calculate final risk
        risk = base_risk * phosphate_factor * season_factor
        
        # Cap at 1.0
        return min(1.0, risk)
    
    def _calculate_dysentery_risk(self, ecoli_count, turbidity, season):
        """
        Calculate dysentery risk based on parameters.
        """
        # Base risk from E. coli count
        base_risk = min(1.0, ecoli_count / self.disease_params['dysentery']['ecoli_threshold'])
        
        # Adjust for turbidity
        turbidity_factor = min(1.5, turbidity / self.disease_params['dysentery']['turbidity_threshold'])
        
        # Adjust for season
        season_factor = self.disease_params['dysentery']['season_weights'].get(season.lower(), 0.5)
        
        # Calculate final risk
        risk = base_risk * turbidity_factor * season_factor
        
        # Cap at 1.0
        return min(1.0, risk)
    
    def _calculate_diarrhea_risk(self, ecoli_count, total_coliforms, season, historical_cases):
        """
        Calculate diarrhea risk based on parameters.
        """
        # Base risk from E. coli count
        base_risk = min(1.0, ecoli_count / self.disease_params['diarrhea']['ecoli_threshold'])
        
        # Adjust for total coliforms
        coliform_factor = min(1.5, total_coliforms / self.disease_params['diarrhea']['coliforms_threshold'])
        
        # Adjust for season
        season_factor = self.disease_params['diarrhea']['season_weights'].get(season.lower(), 0.5)
        
        # Adjust for historical cases
        history_factor = min(1.5, 1.0 + (historical_cases / 30))
        
        # Calculate final risk
        risk = base_risk * coliform_factor * season_factor * history_factor
        
        # Cap at 1.0
        return min(1.0, risk)
    
    def _get_risk_level(self, risk_score):
        """
        Convert risk score to risk level.
        
        Args:
            risk_score: Risk score between 0 and 1
            
        Returns:
            Risk level string
        """
        if risk_score < self.risk_thresholds['Low']:
            return 'Low'
        elif risk_score < self.risk_thresholds['Medium']:
            return 'Medium'
        elif risk_score < self.risk_thresholds['High']:
            return 'High'
        else:
            return 'Critical'
    
    def generate_dataset(self, num_samples=1000, high_risk_ratio=0.2):
        """
        Generate a dataset of water quality and disease risk samples.
        
        Args:
            num_samples: Number of samples to generate
            high_risk_ratio: Ratio of high-risk samples to generate
            
        Returns:
            DataFrame containing the generated dataset
        """
        # Calculate number of high-risk samples
        num_high_risk = int(num_samples * high_risk_ratio)
        num_normal = num_samples - num_high_risk
        
        # Generate samples
        samples = []
        
        # Generate normal samples
        for _ in range(num_normal):
            sample = self.generate_single_sample(high_risk=False)
            risk_data = self.calculate_disease_risks(sample)
            
            # Flatten the sample and add risk data
            flat_sample = self._flatten_sample(sample)
            flat_sample.update(self._flatten_risk_data(risk_data))
            
            samples.append(flat_sample)
        
        # Generate high-risk samples
        for _ in range(num_high_risk):
            sample = self.generate_single_sample(high_risk=True)
            risk_data = self.calculate_disease_risks(sample)
            
            # Flatten the sample and add risk data
            flat_sample = self._flatten_sample(sample)
            flat_sample.update(self._flatten_risk_data(risk_data))
            
            samples.append(flat_sample)
        
        # Convert to DataFrame
        df = pd.DataFrame(samples)
        
        # Shuffle the dataset
        df = df.sample(frac=1).reset_index(drop=True)
        
        return df
    
    def _flatten_sample(self, sample):
        """
        Flatten a nested sample dictionary into a single-level dictionary.
        
        Args:
            sample: Nested dictionary containing sample data
            
        Returns:
            Flattened dictionary
        """
        flat_dict = {}
        
        # Flatten water quality parameters
        for key, value in sample['water_quality'].items():
            flat_dict[key] = value
        
        # Flatten environmental parameters
        for key, value in sample['environmental'].items():
            flat_dict[key] = value
        
        # Flatten historical data
        for key, value in sample['historical'].items():
            flat_dict[key] = value
        
        # Flatten location data
        for key, value in sample['location'].items():
            flat_dict[f'location_{key}'] = value
        
        return flat_dict
    
    def _flatten_risk_data(self, risk_data):
        """
        Flatten nested risk data into a single-level dictionary.
        
        Args:
            risk_data: Nested dictionary containing risk data
            
        Returns:
            Flattened dictionary
        """
        flat_dict = {
            'overall_risk': risk_data['overall_risk']
        }
        
        # Flatten disease risks
        for disease, risk_info in risk_data['disease_risks'].items():
            flat_dict[f'{disease}_risk_score'] = risk_info['risk_score']
            flat_dict[f'{disease}_risk_level'] = risk_info['risk_level']
        
        return flat_dict
    
    def generate_time_series_data(self, num_days=365, location=None):
        """
        Generate time series data for a specific location.
        
        Args:
            num_days: Number of days to generate data for
            location: Optional location dictionary (if None, a random location is chosen)
            
        Returns:
            DataFrame containing time series data
        """
        # Choose a random location if not specified
        if location is None:
            location = {
                'district': random.choice(self.districts),
                'state': random.choice(self.states),
                'latitude': 26.0 + np.random.uniform(-0.5, 0.5),
                'longitude': 92.0 + np.random.uniform(-1.0, 1.0)
            }
        
        # Generate start date (1 year ago)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=num_days)
        
        # Generate dates
        dates = [start_date + timedelta(days=i) for i in range(num_days)]
        
        # Determine seasons for each date
        seasons = []
        for date in dates:
            month = date.month
            if 12 <= month <= 2:  # December to February
                seasons.append('winter')
            elif 3 <= month <= 5:  # March to May
                seasons.append('summer')
            elif 6 <= month <= 9:  # June to September
                seasons.append('monsoon')
            else:  # October to November
                seasons.append('autumn')
        
        # Generate base parameters
        base_params = {}
        for param in self.param_ranges.keys():
            base_value = np.random.uniform(*self.param_ranges[param])
            base_params[param] = base_value
        
        # Generate time series data
        time_series_data = []
        
        # Initialize disease cases
        disease_cases = {
            'cholera': 0,
            'typhoid': 0,
            'hepatitis_a': 0,
            'dysentery': 0,
            'diarrhea': 0
        }
        
        for i, date in enumerate(dates):
            # Get season for this date
            season = seasons[i]
            
            # Generate sample for this date
            sample = self.generate_single_sample(season=season)
            
            # Calculate disease risks
            risk_data = self.calculate_disease_risks(sample)
            
            # Update disease cases based on risks
            for disease, risk_info in risk_data['disease_risks'].items():
                risk_score = risk_info['risk_score']
                
                # Simulate new cases based on risk
                if risk_score < 0.3:  # Low risk
                    new_cases = np.random.poisson(0.1)
                elif risk_score < 0.5:  # Medium risk
                    new_cases = np.random.poisson(0.5)
                elif risk_score < 0.7:  # High risk
                    new_cases = np.random.poisson(2)
                else:  # Critical risk
                    new_cases = np.random.poisson(5)
                
                # Update disease cases
                disease_cases[disease] = new_cases
            
            # Flatten the sample
            flat_sample = self._flatten_sample(sample)
            
            # Add date and disease cases
            flat_sample['date'] = date.strftime('%Y-%m-%d')
            for disease, cases in disease_cases.items():
                flat_sample[f'{disease}_cases'] = cases
            
            time_series_data.append(flat_sample)
        
        # Convert to DataFrame
        df = pd.DataFrame(time_series_data)
        
        return df
    
    def save_dataset(self, df, filename):
        """
        Save dataset to CSV file.
        
        Args:
            df: DataFrame containing the dataset
            filename: Name of the file to save
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save to CSV
        df.to_csv(filename, index=False)
        logger.info(f"Dataset saved to {filename}")
    
    def save_json_samples(self, num_samples=10, filename=None):
        """
        Generate and save JSON samples for API testing.
        
        Args:
            num_samples: Number of samples to generate
            filename: Name of the file to save (if None, samples are returned but not saved)
            
        Returns:
            List of JSON samples
        """
        # Generate samples
        samples = []
        for i in range(num_samples):
            # Alternate between normal and high-risk samples
            high_risk = (i % 2 == 0)
            
            # Generate sample
            sample = self.generate_single_sample(high_risk=high_risk)
            samples.append(sample)
        
        # Save to file if filename is provided
        if filename is not None:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            # Save to JSON
            with open(filename, 'w') as f:
                json.dump(samples, f, indent=2)
            logger.info(f"JSON samples saved to {filename}")
        
        return samples


# Example usage
if __name__ == '__main__':
    # Create generator
    generator = SyntheticDataGenerator()
    
    # Generate a dataset
    dataset = generator.generate_dataset(num_samples=1000, high_risk_ratio=0.2)
    
    # Save dataset
    generator.save_dataset(dataset, 'synthetic_data.csv')
    
    # Generate JSON samples
    json_samples = generator.save_json_samples(num_samples=10, filename='api_test_samples.json')
    
    # Generate time series data
    time_series = generator.generate_time_series_data(num_days=365)
    
    # Save time series data
    generator.save_dataset(time_series, 'time_series_data.csv')