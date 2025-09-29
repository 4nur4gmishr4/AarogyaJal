#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Alert Generator for Water-Borne Disease Prediction System

This module provides utilities for generating alerts based on disease risk predictions.
It includes functions for creating alerts with different severity levels and
formatting them for delivery through various channels (mobile app notifications,
SMS, email, etc.).
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class AlertGenerator:
    """
    Generates alerts based on disease risk predictions.
    
    This class provides methods for creating structured alerts with
    appropriate severity levels, messages, and recommendations based on
    the risk predictions from the disease prediction models.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the AlertGenerator.
        
        Args:
            config: Optional configuration dictionary with alert thresholds and settings
        """
        self.config = config or {
            'risk_thresholds': {
                'critical': 0.7,
                'high': 0.5,
                'medium': 0.3,
                'low': 0.1
            },
            'alert_levels': {
                'critical': 'CRITICAL',
                'high': 'HIGH',
                'medium': 'MEDIUM',
                'low': 'LOW'
            }
        }
    
    def generate_alerts(self, prediction_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate alerts based on prediction results.
        
        Args:
            prediction_results: Dictionary containing disease risk predictions
            
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        # Extract overall risk level
        overall_risk = prediction_results.get('overall_risk', 'LOW')
        
        # Generate overall alert if risk is high or critical
        if overall_risk in ['HIGH', 'CRITICAL']:
            alerts.append(self._create_overall_alert(overall_risk))
        
        # Generate disease-specific alerts
        disease_risks = prediction_results.get('disease_risks', {})
        for disease, risk_data in disease_risks.items():
            risk_level = risk_data.get('risk_level', 'Low')
            risk_score = risk_data.get('risk_score', 0.0)
            
            # Generate alert for high and critical risks
            if risk_level in ['High', 'Critical']:
                alerts.append(self._create_disease_alert(
                    disease, risk_level, risk_score, risk_data.get('recommendations', [])
                ))
        
        return alerts
    
    def _create_overall_alert(self, risk_level: str) -> Dict[str, Any]:
        """
        Create an overall alert for high overall risk.
        
        Args:
            risk_level: Overall risk level ('HIGH' or 'CRITICAL')
            
        Returns:
            Alert dictionary
        """
        severity = 'warning' if risk_level == 'HIGH' else 'danger'
        
        return {
            'id': self._generate_alert_id(),
            'timestamp': self._get_timestamp(),
            'type': 'overall',
            'severity': severity,
            'title': f"{risk_level} Water-Borne Disease Risk Detected",
            'message': self._get_overall_message(risk_level),
            'actions': self._get_overall_actions(risk_level)
        }
    
    def _create_disease_alert(self, disease: str, risk_level: str, 
                             risk_score: float, recommendations: List[str]) -> Dict[str, Any]:
        """
        Create a disease-specific alert.
        
        Args:
            disease: Name of the disease
            risk_level: Risk level ('High' or 'Critical')
            risk_score: Numerical risk score
            recommendations: List of recommendations
            
        Returns:
            Alert dictionary
        """
        severity = 'warning' if risk_level == 'High' else 'danger'
        
        return {
            'id': self._generate_alert_id(),
            'timestamp': self._get_timestamp(),
            'type': 'disease',
            'disease': disease,
            'severity': severity,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'title': f"{risk_level} {self._format_disease_name(disease)} Risk Detected",
            'message': self._get_disease_message(disease, risk_level),
            'recommendations': recommendations,
            'actions': self._get_disease_actions(disease, risk_level)
        }
    
    def _generate_alert_id(self) -> str:
        """
        Generate a unique alert ID.
        
        Returns:
            Unique alert ID string
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        return f"alert-{timestamp}"
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp in ISO format.
        
        Returns:
            ISO formatted timestamp string
        """
        return datetime.now().isoformat()
    
    def _format_disease_name(self, disease: str) -> str:
        """
        Format disease name for display.
        
        Args:
            disease: Raw disease name
            
        Returns:
            Formatted disease name
        """
        # Replace underscores with spaces and capitalize
        return disease.replace('_', ' ').title()
    
    def _get_overall_message(self, risk_level: str) -> str:
        """
        Get message for overall alert.
        
        Args:
            risk_level: Overall risk level
            
        Returns:
            Alert message string
        """
        if risk_level == 'HIGH':
            return "High risk of water-borne diseases detected in your area. Take precautionary measures."
        else:  # CRITICAL
            return "Critical risk of water-borne diseases detected in your area. Immediate action required!"
    
    def _get_disease_message(self, disease: str, risk_level: str) -> str:
        """
        Get message for disease-specific alert.
        
        Args:
            disease: Name of the disease
            risk_level: Risk level
            
        Returns:
            Alert message string
        """
        disease_name = self._format_disease_name(disease)
        
        if risk_level == 'High':
            return f"High risk of {disease_name} detected in your area. Take precautionary measures."
        else:  # Critical
            return f"Critical risk of {disease_name} detected in your area. Immediate action required!"
    
    def _get_overall_actions(self, risk_level: str) -> List[Dict[str, str]]:
        """
        Get actions for overall alert.
        
        Args:
            risk_level: Overall risk level
            
        Returns:
            List of action dictionaries
        """
        actions = [
            {
                'name': 'view_details',
                'label': 'View Details',
                'url': '/risk-details'
            },
            {
                'name': 'safety_guidelines',
                'label': 'Safety Guidelines',
                'url': '/guidelines'
            }
        ]
        
        if risk_level == 'CRITICAL':
            actions.append({
                'name': 'emergency_contacts',
                'label': 'Emergency Contacts',
                'url': '/emergency-contacts'
            })
        
        return actions
    
    def _get_disease_actions(self, disease: str, risk_level: str) -> List[Dict[str, str]]:
        """
        Get actions for disease-specific alert.
        
        Args:
            disease: Name of the disease
            risk_level: Risk level
            
        Returns:
            List of action dictionaries
        """
        actions = [
            {
                'name': 'view_details',
                'label': 'View Details',
                'url': f'/disease/{disease}'
            },
            {
                'name': 'prevention_tips',
                'label': 'Prevention Tips',
                'url': f'/prevention/{disease}'
            }
        ]
        
        if risk_level == 'Critical':
            actions.append({
                'name': 'find_healthcare',
                'label': 'Find Healthcare',
                'url': '/healthcare-facilities'
            })
        
        return actions
    
    def format_for_mobile_notification(self, alert: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format alert for mobile push notification.
        
        Args:
            alert: Alert dictionary
            
        Returns:
            Formatted notification dictionary
        """
        return {
            'title': alert['title'],
            'body': alert['message'],
            'data': {
                'alert_id': alert['id'],
                'type': alert['type'],
                'severity': alert['severity'],
                'timestamp': alert['timestamp']
            }
        }
    
    def format_for_sms(self, alert: Dict[str, Any]) -> str:
        """
        Format alert for SMS delivery.
        
        Args:
            alert: Alert dictionary
            
        Returns:
            Formatted SMS message string
        """
        return f"ALERT: {alert['title']}. {alert['message']}"
    
    def format_for_email(self, alert: Dict[str, Any]) -> Dict[str, str]:
        """
        Format alert for email delivery.
        
        Args:
            alert: Alert dictionary
            
        Returns:
            Dictionary with email subject and body
        """
        # Basic email template
        subject = f"Water Quality Alert: {alert['title']}"
        
        body = f"""
        {alert['title']}
        
        {alert['message']}
        
        Severity: {alert['severity'].upper()}
        Time: {alert['timestamp']}
        """
        
        # Add recommendations if available
        if 'recommendations' in alert and alert['recommendations']:
            body += "\n\nRecommendations:\n"
            for i, rec in enumerate(alert['recommendations'], 1):
                body += f"  {i}. {rec}\n"
        
        return {
            'subject': subject,
            'body': body
        }


# Example usage
if __name__ == "__main__":
    # Create alert generator
    alert_gen = AlertGenerator()
    
    # Example prediction results
    prediction_results = {
        'overall_risk': 'HIGH',
        'disease_risks': {
            'cholera': {
                'risk_score': 0.75,
                'risk_level': 'Critical',
                'recommendations': [
                    "Boil all drinking water for at least one minute.",
                    "Avoid consuming raw or undercooked food.",
                    "Wash hands frequently with soap and clean water."
                ]
            },
            'typhoid': {
                'risk_score': 0.65,
                'risk_level': 'High',
                'recommendations': [
                    "Drink only bottled or treated water.",
                    "Avoid street food and raw vegetables."
                ]
            },
            'diarrhea': {
                'risk_score': 0.45,
                'risk_level': 'Medium',
                'recommendations': [
                    "Maintain good hygiene practices.",
                    "Drink clean water."
                ]
            }
        }
    }
    
    # Generate alerts
    alerts = alert_gen.generate_alerts(prediction_results)
    
    # Print alerts
    print(json.dumps(alerts, indent=2))
    
    # Example of formatting for different channels
    if alerts:
        print("\nMobile Notification:")
        print(json.dumps(alert_gen.format_for_mobile_notification(alerts[0]), indent=2))
        
        print("\nSMS:")
        print(alert_gen.format_for_sms(alerts[0]))
        
        print("\nEmail:")
        print(json.dumps(alert_gen.format_for_email(alerts[0]), indent=2))