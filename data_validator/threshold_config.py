import json
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime


class ThresholdConfig:
    """
    Configuration management for statistical validation thresholds.
    Handles field-specific thresholds and validation rules.
    """
    
    def __init__(self):
        self.thresholds = {}
        self.global_config = {
            'default_z_score': 3.0,
            'default_iqr_multiplier': 1.5,
            'default_confidence_threshold': 0.8,
            'allow_new_categories': True,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Initialize with some sensible defaults
        self._set_default_thresholds()
    
    def _set_default_thresholds(self):
        """Set default thresholds for common field types"""
        
        # Common e-commerce field defaults
        default_configs = {
            'price': {
                'z_score': 3.0,
                'iqr_multiplier': 2.0,
                'range': (0, 10000),  # $0 to $10,000
                'percentile_range': (0.01, 0.99)
            },
            'rating': {
                'z_score': 2.5,
                'range': (0, 5),
                'iqr_multiplier': 1.5
            },
            'review_count': {
                'z_score': 3.0,
                'iqr_multiplier': 2.5,
                'range': (0, 10000)
            },
            'discount_percent': {
                'z_score': 2.0,
                'range': (0, 90),  # 0% to 90% discount
                'iqr_multiplier': 1.5
            },
            'shipping_cost': {
                'z_score': 2.5,
                'range': (0, 100),  # $0 to $100
                'iqr_multiplier': 2.0
            },
            'availability': {
                'allowed_values': ['In Stock', 'Out of Stock', 'Limited', 'Backordered'],
                'allow_new_categories': False
            },
            'category': {
                'allow_new_categories': True,
                'min_frequency': 0.001  # At least 0.1% frequency
            },
            'brand': {
                'allow_new_categories': True,
                'min_frequency': 0.001
            },
            'source': {
                'allowed_values': ['site_a', 'site_b', 'site_c'],
                'allow_new_categories': False
            }
        }
        
        for field, config in default_configs.items():
            self.thresholds[field] = config
    
    def set_threshold(self, field: str, threshold_type: str, value: Any) -> None:
        """
        Set a specific threshold for a field.
        
        Args:
            field: Name of the field
            threshold_type: Type of threshold (z_score, iqr_multiplier, range, etc.)
            value: Threshold value
        """
        if field not in self.thresholds:
            self.thresholds[field] = {}
        
        self.thresholds[field][threshold_type] = value
        self.global_config['updated_at'] = datetime.now().isoformat()
        
        print(f"Set {threshold_type} threshold for {field}: {value}")
    
    def get_threshold(self, field: str, threshold_type: str) -> Optional[Any]:
        """
        Get a specific threshold for a field.
        
        Args:
            field: Name of the field
            threshold_type: Type of threshold
            
        Returns:
            Threshold value or None if not found
        """
        if field in self.thresholds:
            return self.thresholds[field].get(threshold_type)
        return None
    
    def get_field_thresholds(self, field: str) -> Dict[str, Any]:
        """
        Get all thresholds for a specific field.
        
        Args:
            field: Name of the field
            
        Returns:
            Dictionary of all thresholds for the field
        """
        return self.thresholds.get(field, {})
    
    def remove_threshold(self, field: str, threshold_type: str) -> bool:
        """
        Remove a specific threshold for a field.
        
        Args:
            field: Name of the field
            threshold_type: Type of threshold to remove
            
        Returns:
            True if removed, False if not found
        """
        if field in self.thresholds and threshold_type in self.thresholds[field]:
            del self.thresholds[field][threshold_type]
            self.global_config['updated_at'] = datetime.now().isoformat()
            print(f"Removed {threshold_type} threshold for {field}")
            return True
        return False
    
    def set_field_config(self, field: str, config: Dict[str, Any]) -> None:
        """
        Set complete configuration for a field.
        
        Args:
            field: Name of the field
            config: Dictionary containing all thresholds for the field
        """
        self.thresholds[field] = config.copy()
        self.global_config['updated_at'] = datetime.now().isoformat()
        print(f"Set complete configuration for {field}")
    
    def get_all_thresholds(self) -> Dict[str, Dict[str, Any]]:
        """Get all configured thresholds"""
        return self.thresholds.copy()
    
    def set_global_config(self, key: str, value: Any) -> None:
        """Set a global configuration parameter"""
        self.global_config[key] = value
        self.global_config['updated_at'] = datetime.now().isoformat()
        print(f"Set global config {key}: {value}")
    
    def get_global_config(self, key: str) -> Optional[Any]:
        """Get a global configuration parameter"""
        return self.global_config.get(key)
    
    def create_field_profile(self, field: str, field_type: str, 
                           sensitivity: str = 'medium') -> Dict[str, Any]:
        """
        Create a threshold profile for a field based on its type and sensitivity.
        
        Args:
            field: Name of the field
            field_type: Type of field (price, rating, count, categorical, etc.)
            sensitivity: Sensitivity level (strict, medium, relaxed)
            
        Returns:
            Dictionary containing the threshold configuration
        """
        sensitivity_multipliers = {
            'strict': 0.7,
            'medium': 1.0,
            'relaxed': 1.3
        }
        
        multiplier = sensitivity_multipliers.get(sensitivity, 1.0)
        
        profiles = {
            'price': {
                'z_score': 3.0 * multiplier,
                'iqr_multiplier': 2.0 * multiplier,
                'range': (0, 50000),
                'percentile_range': (0.01, 0.99)
            },
            'rating': {
                'z_score': 2.5 * multiplier,
                'range': (0, 5),
                'iqr_multiplier': 1.5 * multiplier
            },
            'count': {
                'z_score': 3.0 * multiplier,
                'iqr_multiplier': 2.5 * multiplier,
                'range': (0, 100000)
            },
            'percentage': {
                'z_score': 2.0 * multiplier,
                'range': (0, 100),
                'iqr_multiplier': 1.5 * multiplier
            },
            'categorical': {
                'allow_new_categories': sensitivity == 'relaxed',
                'min_frequency': 0.001 if sensitivity == 'relaxed' else 0.01
            },
            'text': {
                'pattern': r'^.{1,500}$',  # 1-500 characters
                'allow_empty': sensitivity == 'relaxed'
            }
        }
        
        if field_type in profiles:
            profile = profiles[field_type].copy()
            self.set_field_config(field, profile)
            return profile
        else:
            print(f"Unknown field type: {field_type}")
            return {}
    
    def validate_config(self) -> List[str]:
        """
        Validate the current configuration for consistency and correctness.
        
        Returns:
            List of validation warnings/errors
        """
        warnings = []
        
        for field, config in self.thresholds.items():
            # Check for conflicting thresholds
            if 'range' in config and 'z_score' in config:
                range_min, range_max = config['range']
                if range_min < 0 and 'price' in field.lower():
                    warnings.append(f"{field}: Negative values allowed in range but field appears to be price")
            
            # Check for unrealistic z_score thresholds
            if 'z_score' in config:
                if config['z_score'] < 1.0:
                    warnings.append(f"{field}: Z-score threshold {config['z_score']} is very strict")
                elif config['z_score'] > 5.0:
                    warnings.append(f"{field}: Z-score threshold {config['z_score']} is very lenient")
            
            # Check for unrealistic IQR multipliers
            if 'iqr_multiplier' in config:
                if config['iqr_multiplier'] < 1.0:
                    warnings.append(f"{field}: IQR multiplier {config['iqr_multiplier']} is very strict")
                elif config['iqr_multiplier'] > 3.0:
                    warnings.append(f"{field}: IQR multiplier {config['iqr_multiplier']} is very lenient")
            
            # Check categorical configurations
            if 'allowed_values' in config:
                if not isinstance(config['allowed_values'], list):
                    warnings.append(f"{field}: allowed_values should be a list")
                elif len(config['allowed_values']) == 0:
                    warnings.append(f"{field}: allowed_values list is empty")
        
        return warnings
    
    def optimize_thresholds(self, validation_results: List[Dict[str, Any]], 
                          target_anomaly_rate: float = 0.05) -> Dict[str, Any]:
        """
        Optimize thresholds based on validation results to achieve target anomaly rate.
        
        Args:
            validation_results: List of validation results
            target_anomaly_rate: Desired anomaly detection rate (0.05 = 5%)
            
        Returns:
            Dictionary containing optimization results
        """
        current_anomaly_rate = sum(1 for r in validation_results if not r['is_valid']) / len(validation_results)
        
        optimization_results = {
            'current_anomaly_rate': current_anomaly_rate,
            'target_anomaly_rate': target_anomaly_rate,
            'adjustments_made': [],
            'recommendations': []
        }
        
        # Collect field-specific anomaly rates
        field_anomalies = {}
        for result in validation_results:
            for field, field_result in result.get('field_scores', {}).items():
                if field not in field_anomalies:
                    field_anomalies[field] = {'total': 0, 'anomalies': 0}
                field_anomalies[field]['total'] += 1
                if not field_result['is_valid']:
                    field_anomalies[field]['anomalies'] += 1
        
        # Calculate field-specific anomaly rates
        field_rates = {}
        for field, counts in field_anomalies.items():
            field_rates[field] = counts['anomalies'] / counts['total'] if counts['total'] > 0

        # Claoude excedded the lenght of the output here, so we will not be able to complete the code.
        # the below code is Copilot fantasy :)     
        optimization_results['field_anomaly_rates'] = field_rates
        optimization_results['field_adjustments'] = {}
        for field, rate in field_rates.items():
            if rate > target_anomaly_rate:
                # Adjust thresholds to reduce anomalies
                if 'z_score' in self.thresholds[field]:
                    new_z_score = self.thresholds[field]['z_score'] * 0.9
                    self.set_threshold(field, 'z_score', new_z_score)
                    optimization_results['field_adjustments'][field] = {
                        'z_score': new_z_score,
                        'action': 'decreased'
                    }
                elif 'iqr_multiplier' in self.thresholds[field]:
                    new_iqr = self.thresholds[field]['iqr_multiplier'] * 0.9
                    self.set_threshold(field, 'iqr_multiplier', new_iqr)
                    optimization_results['field_adjustments'][field] = {
                        'iqr_multiplier': new_iqr,
                        'action': 'decreased'
                    }
        else:
            optimization_results['recommendations'].append(
                f"Field '{field}' anomaly rate {rate:.2%} exceeds target {target_anomaly_rate:.2%}. "
                "Consider adjusting thresholds."
            )
        optimization_results['global_config'] = self.global_config.copy()
        return optimization_results
    def save_config(self, file_path: str) -> None:
        """
        Save the current configuration to a JSON file.
        Args:
            file_path: Path to the JSON file
        """
        config_data = {
            'thresholds': self.thresholds,
            'global_config': self.global_config
        }
        with open(file_path, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"Configuration saved to {file_path}")
        self.save_config("threshold_config.json")
    def load_config(self, file_path: str) -> None:
        """
        Load configuration from a JSON file.
        Args:
            file_path: Path to the JSON file
        """
        try:
            with open(file_path, 'r') as f:
                config_data = json.load(f)
            self.thresholds = config_data.get('thresholds', {})
            self.global_config = config_data.get('global_config', self.global_config)
            print(f"Configuration loaded from {file_path}")
        except FileNotFoundError:
            print(f"Configuration file {file_path} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}.")
        except Exception as e:
            print(f"Unexpected error loading configuration: {e}")
        self.save_config("threshold_config.json")
        self.save_config("threshold_config.json")
        self.save_config("threshold_config.json")
        self.save_config("threshold_config.json")
        except Exception as e:
            print(f"Unexpected error loading configuration: {e}")
        self.save_config("threshold_config.json")
        self.save_config("threshold_config.json")
        self.save_config("threshold_config.json")
        self.save_config("threshold_config.json")
        self.save_config("threshold_config.json")
        self.save_config("threshold_config.json")
