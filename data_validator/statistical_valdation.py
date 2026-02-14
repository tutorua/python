import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from typing import Dict, List, Any, Optional, Tuple
import json
import yaml
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

class AnomalyType(Enum):
    DISTRIBUTION_SHIFT = "distribution_shift"
    OUTLIER = "outlier"
    TREND_BREAK = "trend_break"
    SEASONAL_ANOMALY = "seasonal_anomaly"

@dataclass
class StatisticalAnomaly:
    field: str
    anomaly_type: AnomalyType
    value: Any
    score: float
    confidence: float
    message: str
    reference_period: str

class StatisticalValidator:
    def __init__(self, config_path: str):
        """Initialize statistical validator with configuration"""
        self.config = self._load_config(config_path)
        self.historical_data = {}
        self.baseline_stats = {}
        self.anomalies: List[StatisticalAnomaly] = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load statistical validation configuration"""
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def set_historical_data(self, historical_data: List[Dict[str, Any]]):
        """Set historical data for baseline calculations"""
        self.historical_df = pd.DataFrame(historical_data)
        self._calculate_baseline_stats()
        
    def _calculate_baseline_stats(self):
        """Calculate baseline statistics from historical data"""
        numeric_columns = self.historical_df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in self.config.get('statistical_fields', {}):
                self.baseline_stats[col] = {
                    'mean': self.historical_df[col].mean(),
                    'std': self.historical_df[col].std(),
                    'median': self.historical_df[col].median(),
                    'q1': self.historical_df[col].quantile(0.25),
                    'q3': self.historical_df[col].quantile(0.75),
                    'min': self.historical_df[col].min(),
                    'max': self.historical_df[col].max(),
                    'distribution': self._fit_distribution(self.historical_df[col])
                }
    
    def _fit_distribution(self, data: pd.Series) -> Dict[str, Any]:
        """Fit statistical distribution to data"""
        # Test for normal distribution
        _, p_value_normal = stats.normaltest(data.dropna())
        
        # Test for exponential distribution
        try:
            exp_params = stats.expon.fit(data.dropna())
            _, p_value_exp = stats.kstest(data.dropna(), 'expon', args=exp_params)
        except:
            p_value_exp = 0
        
        # Test for log-normal distribution
        try:
            log_data = np.log(data.dropna() + 1)  # Add 1 to handle zeros
            lognorm_params = stats.lognorm.fit(log_data)
            _, p_value_lognorm = stats.kstest(log_data, 'lognorm', args=lognorm_params)
        except:
            p_value_lognorm = 0
        
        # Choose best fitting distribution
        distributions = {
            'normal': p_value_normal,
            'exponential': p_value_exp,
            'lognormal': p_value_lognorm
        }
        
        best_dist = max(distributions, key=distributions.get)
        
        return {
            'type': best_dist,
            'p_value': distributions[best_dist],
            'params': self._get_distribution_params(data, best_dist)
        }
    
    def _get_distribution_params(self, data: pd.Series, dist_type: str) -> Dict:
        """Get parameters for the specified distribution"""
        if dist_type == 'normal':
            return {'loc': data.mean(), 'scale': data.std()}
        elif dist_type == 'exponential':
            return {'scale': 1/data.mean()}
        elif dist_type == 'lognormal':
            log_data = np.log(data + 1)
            return {'s': log_data.std(), 'scale': np.exp(log_data.mean())}
        return {}
    
    def validate_distribution_shift(self, new_data: List[Dict[str, Any]]) -> List[StatisticalAnomaly]:
        """Detect distribution shifts using statistical tests"""
        anomalies = []
        new_df = pd.DataFrame(new_data)
        
        for field in self.config.get('statistical_fields', {}):
            if field not in new_df.columns or field not in self.baseline_stats:
                continue
                
            field_config = self.config['statistical_fields'][field]
            historical_values = self.historical_df[field].dropna()
            new_values = new_df[field].dropna()
            
            if len(new_values) < field_config.get('min_samples', 10):
                continue
            
            # Kolmogorov-Smirnov test for distribution comparison
            ks_stat, ks_p_value = stats.ks_2samp(historical_values, new_values)
            ks_threshold = field_config.get('ks_threshold', 0.05)
            
            if ks_p_value < ks_threshold:
                anomalies.append(StatisticalAnomaly(
                    field=field,
                    anomaly_type=AnomalyType.DISTRIBUTION_SHIFT,
                    value=f"KS-statistic: {ks_stat:.4f}",
                    score=ks_stat,
                    confidence=1 - ks_p_value,
                    message=f"Distribution shift detected in {field} (p-value: {ks_p_value:.4f})",
                    reference_period="baseline"
                ))
            
            # Mann-Whitney U test for median comparison
            u_stat, u_p_value = stats.mannwhitneyu(historical_values, new_values, alternative='two-sided')
            u_threshold = field_config.get('mannwhitney_threshold', 0.05)
            
            if u_p_value < u_threshold:
                anomalies.append(StatisticalAnomaly(
                    field=field,
                    anomaly_type=AnomalyType.DISTRIBUTION_SHIFT,
                    value=f"U-statistic: {u_stat}",
                    score=u_stat,
                    confidence=1 - u_p_value,
                    message=f"Median shift detected in {field} (p-value: {u_p_value:.4f})",
                    reference_period="baseline"
                ))
        
        return anomalies
    
    def detect_outliers(self, data: List[Dict[str, Any]]) -> List[StatisticalAnomaly]:
        """Detect outliers using multiple methods"""
        anomalies = []
        df = pd.DataFrame(data)
        
        for field in self.config.get('statistical_fields', {}):
            if field not in df.columns:
                continue
                
            field_config = self.config['statistical_fields'][field]
            values = df[field].dropna()
            
            if len(values) < field_config.get('min_samples', 10):
                continue
            
            # Z-score based outlier detection
            if field_config.get('z_score_detection', True):
                z_scores = np.abs(stats.zscore(values))
                z_threshold = field_config.get('z_threshold', 3.0)
                z_outliers = np.where(z_scores > z_threshold)[0]
                
                for idx in z_outliers:
                    anomalies.append(StatisticalAnomaly(
                        field=field,
                        anomaly_type=AnomalyType.OUTLIER,
                        value=values.iloc[idx],
                        score=z_scores[idx],
                        confidence=min(z_scores[idx] / z_threshold, 1.0),
                        message=f"Z-score outlier in {field}: {values.iloc[idx]} (z-score: {z_scores[idx]:.2f})",
                        reference_period="current_batch"
                    ))
            
            # IQR-based outlier detection
            if field_config.get('iqr_detection', True):
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1
                iqr_multiplier = field_config.get('iqr_multiplier', 1.5)
                
                lower_bound = Q1 - iqr_multiplier * IQR
                upper_bound = Q3 + iqr_multiplier * IQR
                
                iqr_outliers = values[(values < lower_bound) | (values > upper_bound)]
                
                for idx, value in iqr_outliers.items():
                    distance = min(abs(value - lower_bound), abs(value - upper_bound))
                    anomalies.append(StatisticalAnomaly(
                        field=field,
                        anomaly_type=AnomalyType.OUTLIER,
                        value=value,
                        score=distance / IQR,
                        confidence=min(distance / (IQR * iqr_multiplier), 1.0),
                        message=f"IQR outlier in {field}: {value} (bounds: {lower_bound:.2f}, {upper_bound:.2f})",
                        reference_period="current_batch"
                    ))
            
            # Isolation Forest for multivariate outlier detection
            if field_config.get('isolation_forest', False) and len(values) > 50:
                iso_forest = IsolationForest(
                    contamination=field_config.get('contamination', 0.1),
                    random_state=42
                )
                outlier_labels = iso_forest.fit_predict(values.values.reshape(-1, 1))
                outlier_scores = iso_forest.decision_function(values.values.reshape(-1, 1))
                
                for idx, (label, score) in enumerate(zip(outlier_labels, outlier_scores)):
                    if label == -1:  # Outlier
                        anomalies.append(StatisticalAnomaly(
                            field=field,
                            anomaly_type=AnomalyType.OUTLIER,
                            value=values.iloc[idx],
                            score=abs(score),
                            confidence=min(abs(score) * 2, 1.0),
                            message=f"Isolation Forest outlier in {field}: {values.iloc[idx]} (score: {score:.3f})",
                            reference_period="current_batch"
                        ))
        
        return anomalies
    
    def detect_trend_breaks(self, data: List[Dict[str, Any]]) -> List[StatisticalAnomaly]:
        """Detect trend breaks and sudden changes"""
        anomalies = []
        df = pd.DataFrame(data)
        
        # Add timestamp if not present
        if 'timestamp' not in df.columns:
            df['timestamp'] = pd.date_range(start='2024-01-01', periods=len(df), freq='D')
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        for field in self.config.get('statistical_fields', {}):
            if field not in df.columns:
                continue
                
            field_config = self.config['statistical_fields'][field]
            
            if not field_config.get('trend_detection', False):
                continue
                
            values = df[field].dropna()
            
            if len(values) < field_config.get('min_trend_samples', 20):
                continue
            
            # Calculate rolling statistics
            window = field_config.get('trend_window', 7)
            rolling_mean = values.rolling(window=window).mean()
            rolling_std = values.rolling(window=window).std()
            
            # Detect sudden changes using CUSUM
            cusum_threshold = field_config.get('cusum_threshold', 2.0)
            cusum_pos = 0
            cusum_neg = 0
            
            for i in range(window, len(values)):
                current_val = values.iloc[i]
                expected_val = rolling_mean.iloc[i-1]
                std_val = rolling_std.iloc[i-1]
                
                if pd.isna(expected_val) or pd.isna(std_val) or std_val == 0:
                    continue
                
                # Standardized residual
                residual = (current_val - expected_val) / std_val
                
                # CUSUM calculation
                cusum_pos = max(0, cusum_pos + residual - 0.5)
                cusum_neg = max(0, cusum_neg - residual - 0.5)
                
                if cusum_pos > cusum_threshold or cusum_neg > cusum_threshold:
                    anomalies.append(StatisticalAnomaly(
                        field=field,
                        anomaly_type=AnomalyType.TREND_BREAK,
                        value=current_val,
                        score=max(cusum_pos, cusum_neg),
                        confidence=min(max(cusum_pos, cusum_neg) / cusum_threshold, 1.0),
                        message=f"Trend break detected in {field} at index {i}: {current_val} (CUSUM: {max(cusum_pos, cusum_neg):.2f})",
                        reference_period=f"rolling_{window}_days"
                    ))
                    
                    # Reset CUSUM after detection
                    cusum_pos = 0
                    cusum_neg = 0
        
        return anomalies
    
    def detect_seasonal_anomalies(self, data: List[Dict[str, Any]]) -> List[StatisticalAnomaly]:
        """Detect seasonal anomalies using historical patterns"""
        anomalies = []
        df = pd.DataFrame(data)
        
        if 'timestamp' not in df.columns:
            df['timestamp'] = pd.date_range(start='2024-01-01', periods=len(df), freq='D')
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['month'] = df['timestamp'].dt.month
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['hour'] = df['timestamp'].dt.hour
        
        for field in self.config.get('statistical_fields', {}):
            if field not in df.columns:
                continue
                
            field_config = self.config['statistical_fields'][field]
            
            if not field_config.get('seasonal_detection', False):
                continue
            
            # Monthly seasonal pattern detection
            if field_config.get('monthly_seasonality', True):
                monthly_stats = self.historical_df.groupby('month')[field].agg(['mean', 'std'])
                
                for _, row in df.iterrows():
                    month = row['month']
                    value = row[field]
                    
                    if pd.isna(value):
                        continue
                        
                    expected_mean = monthly_stats.loc[month, 'mean']
                    expected_std = monthly_stats.loc[month, 'std']
                    
                    if expected_std > 0:
                        z_score = abs(value - expected_mean) / expected_std
                        seasonal_threshold = field_config.get('seasonal_z_threshold', 2.5)
                        
                        if z_score > seasonal_threshold:
                            anomalies.append(StatisticalAnomaly(
                                field=field,
                                anomaly_type=AnomalyType.SEASONAL_ANOMALY,
                                value=value,
                                score=z_score,
                                confidence=min(z_score / seasonal_threshold, 1.0),
                                message=f"Seasonal anomaly in {field} for month {month}: {value} (expected: {expected_mean:.2f}±{expected_std:.2f})",
                                reference_period=f"month_{month}_historical"
                            ))
        
        return anomalies
    
    def validate_data_quality(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive data quality assessment"""
        df = pd.DataFrame(data)
        quality_metrics = {}
        
        for field in self.config.get('statistical_fields', {}):
            if field not in df.columns:
                continue
                
            values = df[field]
            
            quality_metrics[field] = {
                'completeness': 1 - values.isna().sum() / len(values),
                'uniqueness': values.nunique() / len(values),
                'consistency': self._calculate_consistency_score(values),
                'validity': self._calculate_validity_score(values, field),
                'accuracy': self._calculate_accuracy_score(values, field)
            }
        
        return quality_metrics
    
    def _calculate_consistency_score(self, values: pd.Series) -> float:
        """Calculate consistency score based on data patterns"""
        if values.dtype == 'object':
            # For categorical data, check format consistency
            formats = values.dropna().apply(lambda x: self._detect_format(str(x)))
            most_common_format = formats.mode().iloc[0] if not formats.empty else None
            consistency = (formats == most_common_format).sum() / len(formats) if most_common_format else 0
        else:
            # For numeric data, check for reasonable variance
            cv = values.std() / values.mean() if values.mean() != 0 else 0
            consistency = max(0, 1 - cv)  # Lower coefficient of variation = higher consistency
        
        return min(consistency, 1.0)
    
    def _calculate_validity_score(self, values: pd.Series, field: str) -> float:
        """Calculate validity score based on field-specific rules"""
        field_config = self.config.get('statistical_fields', {}).get(field, {})
        
        if 'valid_range' in field_config:
            min_val, max_val = field_config['valid_range']
            valid_count = ((values >= min_val) & (values <= max_val)).sum()
            return valid_count / len(values)
        
        return 1.0  # Default to valid if no rules specified
    
    def _calculate_accuracy_score(self, values: pd.Series, field: str) -> float:
        """Calculate accuracy score against baseline if available"""
        if field in self.baseline_stats:
            baseline_mean = self.baseline_stats[field]['mean']
            baseline_std = self.baseline_stats[field]['std']
            
            # Calculate how many values fall within reasonable range of baseline
            reasonable_range = 2 * baseline_std
            within_range = abs(values - baseline_mean) <= reasonable_range
            return within_range.sum() / len(values)
        
        return 1.0  # Default to accurate if no baseline
    
    def _detect_format(self, value: str) -> str:
        """Detect format pattern of a string value"""
        if value.replace('.', '').replace('-', '').isdigit():
            return 'numeric'
        elif '@' in value:
            return 'email'
        elif value.startswith('http'):
            return 'url'
        elif len(value) == 10 and value.isdigit():
            return 'phone'
        else:
            return 'text'
    
    def run_all_statistical_validations(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run all statistical validation methods"""
        all_anomalies = []
        
        # Distribution shift detection
        if hasattr(self, 'historical_df') and len(self.historical_df) > 0:
            all_anomalies.extend(self.validate_distribution_shift(data))
        
        # Outlier detection
        all_anomalies.extend(self.detect_outliers(data))
        
        # Trend break detection
        all_anomalies.extend(self.detect_trend_breaks(data))
        
        # Seasonal anomaly detection
        if hasattr(self, 'historical_df') and len(self.historical_df) > 0:
            all_anomalies.extend(self.detect_seasonal_anomalies(data))
        
        # Data quality assessment
        quality_metrics = self.validate_data_quality(data)
        
        return {
            'anomalies': all_anomalies,
            'quality_metrics': quality_metrics,
            'total_anomalies': len(all_anomalies),
            'anomaly_types': {atype.value: len([a for a in all_anomalies if a.anomaly_type == atype]) 
                             for atype in AnomalyType}
        }

# Example usage
if __name__ == "__main__":
    # Sample configuration would be loaded from file
    sample_config = {
        'statistical_fields': {
            'price': {
                'min_samples': 10,
                'z_score_detection': True,
                'z_threshold': 3.0,
                'iqr_detection': True,
                'iqr_multiplier': 1.5,
                'trend_detection': True,
                'seasonal_detection': True,
                'valid_range': [0, 10000]
            },
            'stock_quantity': {
                'min_samples': 5,
                'z_score_detection': True,
                'z_threshold': 2.5,
                'trend_detection': True,
                'valid_range': [0, 1000]
            }
        }
    }
    
    print("Statistical validation system ready.")
    print("Use set_historical_data() to provide baseline data, then run validations.")
    