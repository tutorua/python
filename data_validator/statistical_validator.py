import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


class StatisticalValidator:
    """
    Statistical validation system for web scraping data quality control.
    Uses various statistical methods to detect anomalies and outliers.
    """
    
    def __init__(self):
        self.baseline_stats = {}
        self.field_types = {}
        self.validation_methods = {
            'z_score': self._validate_z_score,
            'iqr': self._validate_iqr,
            'range': self._validate_range,
            'categorical': self._validate_categorical,
            'pattern': self._validate_pattern,
            'correlation': self._validate_correlation
        }
    
    def calculate_baseline_stats(self, historical_data: pd.DataFrame) -> None:
        """
        Calculate baseline statistics from historical data.
        
        Args:
            historical_data: DataFrame containing historical records
        """
        print("Calculating baseline statistics...")
        
        # Identify numeric and categorical columns
        numeric_columns = historical_data.select_dtypes(include=[np.number]).columns
        categorical_columns = historical_data.select_dtypes(include=['object']).columns
        
        for column in historical_data.columns:
            if column in numeric_columns:
                self.field_types[column] = 'numeric'
                self._calculate_numeric_stats(historical_data, column)
            elif column in categorical_columns:
                self.field_types[column] = 'categorical'
                self._calculate_categorical_stats(historical_data, column)
        
        # Calculate correlations for numeric fields
        if len(numeric_columns) > 1:
            correlation_matrix = historical_data[numeric_columns].corr()
            self.baseline_stats['correlations'] = correlation_matrix.to_dict()
        
        print(f"Baseline statistics calculated for {len(self.baseline_stats)} fields")
    
    def _calculate_numeric_stats(self, data: pd.DataFrame, column: str) -> None:
        """Calculate statistics for numeric columns"""
        values = data[column].dropna()
        
        if len(values) == 0:
            return
        
        # Basic statistics
        stats_dict = {
            'mean': float(values.mean()),
            'median': float(values.median()),
            'std': float(values.std()),
            'min': float(values.min()),
            'max': float(values.max()),
            'count': len(values),
            'q1': float(values.quantile(0.25)),
            'q3': float(values.quantile(0.75)),
        }
        
        # IQR calculations
        iqr = stats_dict['q3'] - stats_dict['q1']
        stats_dict['iqr'] = iqr
        stats_dict['lower_fence'] = stats_dict['q1'] - 1.5 * iqr
        stats_dict['upper_fence'] = stats_dict['q3'] + 1.5 * iqr
        
        # Distribution analysis
        try:
            # Test for normality
            _, p_value = stats.normaltest(values)
            stats_dict['is_normal'] = p_value > 0.05
            
            # Skewness and kurtosis
            stats_dict['skewness'] = float(stats.skew(values))
            stats_dict['kurtosis'] = float(stats.kurtosis(values))
        except:
            stats_dict['is_normal'] = False
            stats_dict['skewness'] = 0
            stats_dict['kurtosis'] = 0
        
        self.baseline_stats[column] = stats_dict
    
    def _calculate_categorical_stats(self, data: pd.DataFrame, column: str) -> None:
        """Calculate statistics for categorical columns"""
        values = data[column].dropna()
        
        if len(values) == 0:
            return
        
        value_counts = values.value_counts()
        total_count = len(values)
        
        stats_dict = {
            'unique_values': list(value_counts.index),
            'value_counts': value_counts.to_dict(),
            'total_count': total_count,
            'unique_count': len(value_counts),
            'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
            'most_common_freq': float(value_counts.iloc[0] / total_count) if len(value_counts) > 0 else 0,
            'entropy': float(stats.entropy(value_counts.values))
        }
        
        self.baseline_stats[column] = stats_dict
    
    def validate_record(self, record: Dict[str, Any], config) -> Dict[str, Any]:
        """
        Validate a single record against baseline statistics and thresholds.
        
        Args:
            record: Dictionary containing the record to validate
            config: ThresholdConfig object with validation thresholds
            
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'confidence': 1.0,
            'field_scores': {},
            'timestamp': datetime.now().isoformat()
        }
        
        issue_count = 0
        total_checks = 0
        
        # Validate each field
        for field, value in record.items():
            if field not in self.baseline_stats:
                continue
                
            field_result = self._validate_field(field, value, config)
            validation_result['field_scores'][field] = field_result
            
            if not field_result['is_valid']:
                issue_count += 1
                validation_result['issues'].extend(field_result['issues'])
                validation_result['is_valid'] = False
            
            if field_result['warnings']:
                validation_result['warnings'].extend(field_result['warnings'])
            
            total_checks += 1
        
        # Calculate overall confidence
        if total_checks > 0:
            validation_result['confidence'] = max(0.0, 1.0 - (issue_count / total_checks))
        
        return validation_result
    
    def _validate_field(self, field: str, value: Any, config) -> Dict[str, Any]:
        """Validate a single field value"""
        result = {
            'is_valid': True,
            'issues': [],
            'warnings': [],
            'scores': {}
        }
        
        if field not in self.baseline_stats:
            return result
        
        field_stats = self.baseline_stats[field]
        field_type = self.field_types.get(field, 'unknown')
        
        # Get thresholds for this field
        field_thresholds = config.get_field_thresholds(field)
        
        # Apply validation methods based on field type and configured thresholds
        if field_type == 'numeric' and value is not None:
            self._validate_numeric_field(field, value, field_stats, field_thresholds, result)
        elif field_type == 'categorical' and value is not None:
            self._validate_categorical_field(field, value, field_stats, field_thresholds, result)
        
        return result
    
    def _validate_numeric_field(self, field: str, value: float, stats: Dict, 
                              thresholds: Dict, result: Dict) -> None:
        """Validate numeric field using various statistical methods"""
        
        # Z-score validation
        if 'z_score' in thresholds and stats['std'] > 0:
            z_score = abs(value - stats['mean']) / stats['std']
            result['scores']['z_score'] = z_score
            
            if z_score > thresholds['z_score']:
                result['is_valid'] = False
                result['issues'].append(
                    f"{field}: Z-score {z_score:.2f} exceeds threshold {thresholds['z_score']}"
                )
        
        # IQR validation
        if 'iqr_multiplier' in thresholds:
            iqr_multiplier = thresholds['iqr_multiplier']
            lower_bound = stats['q1'] - iqr_multiplier * stats['iqr']
            upper_bound = stats['q3'] + iqr_multiplier * stats['iqr']
            
            if value < lower_bound or value > upper_bound:
                result['is_valid'] = False
                result['issues'].append(
                    f"{field}: Value {value} outside IQR bounds [{lower_bound:.2f}, {upper_bound:.2f}]"
                )
        
        # Range validation
        if 'range' in thresholds:
            min_val, max_val = thresholds['range']
            if value < min_val or value > max_val:
                result['is_valid'] = False
                result['issues'].append(
                    f"{field}: Value {value} outside allowed range [{min_val}, {max_val}]"
                )
        
        # Percentile validation
        if 'percentile_range' in thresholds:
            lower_pct, upper_pct = thresholds['percentile_range']
            # We'd need to store percentiles in baseline stats for this
            pass
        
        # Add warnings for suspicious but not invalid values
        if 'std' in stats and stats['std'] > 0:
            z_score = abs(value - stats['mean']) / stats['std']
            if z_score > 2.0 and z_score <= thresholds.get('z_score', 3.0):
                result['warnings'].append(
                    f"{field}: Moderate deviation (Z-score: {z_score:.2f})"
                )
    
    def _validate_categorical_field(self, field: str, value: str, stats: Dict,
                                  thresholds: Dict, result: Dict) -> None:
        """Validate categorical field"""
        
        # Check if value exists in historical data
        if 'allowed_values' in thresholds:
            if value not in thresholds['allowed_values']:
                result['is_valid'] = False
                result['issues'].append(
                    f"{field}: Value '{value}' not in allowed values"
                )
        elif value not in stats['unique_values']:
            # New categorical value
            if 'allow_new_categories' in thresholds and not thresholds['allow_new_categories']:
                result['is_valid'] = False
                result['issues'].append(
                    f"{field}: New categorical value '{value}' not seen in historical data"
                )
            else:
                result['warnings'].append(
                    f"{field}: New categorical value '{value}'"
                )
        
        # Check frequency if it's a known value
        if value in stats['value_counts']:
            frequency = stats['value_counts'][value] / stats['total_count']
            if 'min_frequency' in thresholds and frequency < thresholds['min_frequency']:
                result['warnings'].append(
                    f"{field}: Low frequency value '{value}' (freq: {frequency:.3f})"
                )
    
    def _validate_z_score(self, value: float, stats: Dict, threshold: float) -> Tuple[bool, str]:
        """Z-score validation method"""
        if stats['std'] == 0:
            return True, ""
        
        z_score = abs(value - stats['mean']) / stats['std']
        if z_score > threshold:
            return False, f"Z-score {z_score:.2f} exceeds threshold {threshold}"
        return True, ""
    
    def _validate_iqr(self, value: float, stats: Dict, multiplier: float) -> Tuple[bool, str]:
        """IQR validation method"""
        lower_bound = stats['q1'] - multiplier * stats['iqr']
        upper_bound = stats['q3'] + multiplier * stats['iqr']
        
        if value < lower_bound or value > upper_bound:
            return False, f"Value {value} outside IQR bounds [{lower_bound:.2f}, {upper_bound:.2f}]"
        return True, ""
    
    def _validate_range(self, value: float, stats: Dict, range_vals: Tuple) -> Tuple[bool, str]:
        """Range validation method"""
        min_val, max_val = range_vals
        if value < min_val or value > max_val:
            return False, f"Value {value} outside range [{min_val}, {max_val}]"
        return True, ""
    
    def _validate_categorical(self, value: str, stats: Dict, config: Dict) -> Tuple[bool, str]:
        """Categorical validation method"""
        if value not in stats['unique_values']:
            return False, f"Unknown categorical value: {value}"
        return True, ""
    
    def _validate_pattern(self, value: str, stats: Dict, pattern: str) -> Tuple[bool, str]:
        """Pattern validation method"""
        import re
        if not re.match(pattern, str(value)):
            return False, f"Value doesn't match pattern: {pattern}"
        return True, ""
    
    def _validate_correlation(self, record: Dict, stats: Dict, threshold: float) -> Tuple[bool, str]:
        """Correlation validation method"""
        # This would check if relationships between fields are maintained
        # Implementation would depend on specific correlation rules
        return True, ""
    
    def generate_validation_report(self, validation_results: List[Dict]) -> Dict:
        """
        Generate a comprehensive validation report.
        
        Args:
            validation_results: List of validation results from validate_record
            
        Returns:
            Dictionary containing the validation report
        """
        total_records = len(validation_results)
        valid_records = sum(1 for r in validation_results if r['is_valid'])
        invalid_records = total_records - valid_records
        
        # Collect all issues by field
        field_issues = {}
        issue_types = {}
        
        for result in validation_results:
            for issue in result['issues']:
                # Extract field name from issue string
                field_name = issue.split(':')[0]
                if field_name not in field_issues:
                    field_issues[field_name] = []
                field_issues[field_name].append(issue)
                
                # Categorize issue types
                if 'Z-score' in issue:
                    issue_types['z_score'] = issue_types.get('z_score', 0) + 1
                elif 'IQR' in issue:
                    issue_types['iqr'] = issue_types.get('iqr', 0) + 1
                elif 'range' in issue:
                    issue_types['range'] = issue_types.get('range', 0) + 1
                elif 'categorical' in issue:
                    issue_types['categorical'] = issue_types.get('categorical', 0) + 1
                else:
                    issue_types['other'] = issue_types.get('other', 0) + 1
        
        # Calculate confidence statistics
        confidences = [r['confidence'] for r in validation_results]
        avg_confidence = np.mean(confidences) if confidences else 0
        
        # Field-level analysis
        field_analysis = {}
        for field, issues in field_issues.items():
            field_analysis[field] = {
                'anomaly_count': len(issues),
                'anomaly_rate': len(issues) / total_records,
                'common_issues': list(set(issues))[:5]  # Top 5 unique issues
            }
        
        report = {
            'generation_time': datetime.now().isoformat(),
            'summary': {
                'total_records': total_records,
                'valid_records': valid_records,
                'invalid_records': invalid_records,
                'validation_rate': (valid_records / total_records * 100) if total_records > 0 else 0,
                'average_confidence': avg_confidence
            },
            'issue_breakdown': issue_types,
            'field_analysis': field_analysis,
            'baseline_stats_summary': {
                field: {
                    'type': self.field_types.get(field, 'unknown'),
                    'mean': stats.get('mean', 'N/A'),
                    'std': stats.get('std', 'N/A'),
                    'unique_count': stats.get('unique_count', 'N/A')
                }
                for field, stats in self.baseline_stats.items()
                if field != 'correlations'
            },
            'recommendations': self._generate_recommendations(field_analysis, issue_types)
        }
        
        return report
    
    def _generate_recommendations(self, field_analysis: Dict, issue_types: Dict) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        # High anomaly rate recommendations
        high_anomaly_fields = [
            field for field, analysis in field_analysis.items()
            if analysis['anomaly_rate'] > 0.1
        ]
        
        if high_anomaly_fields:
            recommendations.append(
                f"High anomaly rates detected in fields: {', '.join(high_anomaly_fields)}. "
                "Consider reviewing data sources or adjusting thresholds."
            )
        
        # Issue type recommendations
        if issue_types.get('z_score', 0) > issue_types.get('iqr', 0):
            recommendations.append(
                "Many Z-score violations detected. Consider using IQR-based validation "
                "for non-normal distributions."
            )
        
        if issue_types.get('categorical', 0) > 0:
            recommendations.append(
                "New categorical values detected. Review if these are legitimate "
                "or indicate data quality issues."
            )
        
        if issue_types.get('range', 0) > 0:
            recommendations.append(
                "Range violations detected. Verify if range constraints are appropriate "
                "for current data patterns."
            )
        
        if not recommendations:
            recommendations.append("Validation results look good. No major issues detected.")
        
        return recommendations
    
    def export_baseline_stats(self, filename: str) -> None:
        """Export baseline statistics to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.baseline_stats, f, indent=2)
        print(f"Baseline statistics exported to {filename}")
    
    def import_baseline_stats(self, filename: str) -> None:
        """Import baseline statistics from JSON file"""
        with open(filename, 'r') as f:
            self.baseline_stats = json.load(f)
        print(f"Baseline statistics imported from {filename}")
        
        # Rebuild field types
        for field, stats in self.baseline_stats.items():
            if field == 'correlations':
                continue
            if 'mean' in stats:
                self.field_types[field] = 'numeric'
            else:
                self.field_types[field] = 'categorical'
                