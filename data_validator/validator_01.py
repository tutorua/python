import json
import yaml
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import statistics
import math

class ValidationResult(Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"

@dataclass
class ValidationError:
    field: str
    rule: str
    value: Any
    message: str
    severity: ValidationResult

class EcommerceValidator:
    def __init__(self, config_path: str):
        """Initialize validator with configuration file (JSON or YAML)"""
        self.config = self._load_config(config_path)
        self.validation_errors: List[ValidationError] = []
        
    def _load_config(self, config_path: str) -> Dict:
        """Load validation configuration from JSON or YAML file"""
        with open(config_path, 'r') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def validate_product(self, product_data: Dict[str, Any]) -> List[ValidationError]:
        """Validate a single product record"""
        self.validation_errors = []
        
        # Static threshold validation
        self._validate_static_thresholds(product_data)
        
        # Dynamic threshold validation (requires historical data)
        self._validate_dynamic_thresholds(product_data)
        
        # Contextual validation
        self._validate_contextual_rules(product_data)
        
        return self.validation_errors
    
    def _validate_static_thresholds(self, product: Dict[str, Any]) -> None:
        """Apply static threshold validation rules"""
        static_rules = self.config.get('static_thresholds', {})
        
        # Price validation
        if 'price' in product and 'price' in static_rules:
            price = product['price']
            price_rules = static_rules['price']
            
            if price < price_rules.get('min', 0):
                self._add_error('price', 'min_price', price, 
                              f"Price {price} below minimum {price_rules['min']}")
            
            if price > price_rules.get('max', float('inf')):
                self._add_error('price', 'max_price', price,
                              f"Price {price} above maximum {price_rules['max']}")
            
            # Check decimal places
            if 'max_decimals' in price_rules:
                decimal_places = len(str(price).split('.')[-1]) if '.' in str(price) else 0
                if decimal_places > price_rules['max_decimals']:
                    self._add_error('price', 'price_precision', price,
                                  f"Price has {decimal_places} decimal places, max allowed: {price_rules['max_decimals']}")
        
        # Title validation
        if 'title' in product and 'title' in static_rules:
            title = product['title']
            title_rules = static_rules['title']
            
            if len(title) < title_rules.get('min_length', 0):
                self._add_error('title', 'min_length', title,
                              f"Title too short: {len(title)} chars, minimum: {title_rules['min_length']}")
            
            if len(title) > title_rules.get('max_length', float('inf')):
                self._add_error('title', 'max_length', title,
                              f"Title too long: {len(title)} chars, maximum: {title_rules['max_length']}")
            
            # Check for HTML tags
            if title_rules.get('no_html', False) and re.search(r'<[^>]+>', title):
                self._add_error('title', 'html_tags', title,
                              "Title contains HTML tags")
            
            # Check character restrictions
            if 'forbidden_chars' in title_rules:
                forbidden = title_rules['forbidden_chars']
                found_chars = [char for char in forbidden if char in title]
                if found_chars:
                    self._add_error('title', 'forbidden_chars', title,
                                  f"Title contains forbidden characters: {found_chars}")
        
        # Date validation
        if 'date' in product and 'date' in static_rules:
            date_str = product['date']
            date_rules = static_rules['date']
            
            try:
                product_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                now = datetime.now()
                
                if 'max_future_days' in date_rules:
                    max_future = now + timedelta(days=date_rules['max_future_days'])
                    if product_date > max_future:
                        self._add_error('date', 'future_date', date_str,
                                      f"Date too far in future: {date_str}")
                
                if 'max_past_days' in date_rules:
                    max_past = now - timedelta(days=date_rules['max_past_days'])
                    if product_date < max_past:
                        self._add_error('date', 'past_date', date_str,
                                      f"Date too far in past: {date_str}")
                        
            except ValueError:
                self._add_error('date', 'invalid_format', date_str,
                              f"Invalid date format: {date_str}")
        
        # Availability validation
        if 'availability' in product and 'availability' in static_rules:
            availability = product['availability']
            avail_rules = static_rules['availability']
            
            if 'allowed_values' in avail_rules:
                if availability not in avail_rules['allowed_values']:
                    self._add_error('availability', 'invalid_value', availability,
                                  f"Invalid availability: {availability}")
            
            # Stock quantity validation
            if 'stock_quantity' in product:
                stock = product['stock_quantity']
                if stock < 0:
                    self._add_error('stock_quantity', 'negative_stock', stock,
                                  f"Negative stock quantity: {stock}")
                
                if not isinstance(stock, int):
                    self._add_error('stock_quantity', 'non_integer', stock,
                                  f"Stock quantity must be integer: {stock}")
    
    def _validate_dynamic_thresholds(self, product: Dict[str, Any]) -> None:
        """Apply dynamic threshold validation (requires historical data)"""
        dynamic_rules = self.config.get('dynamic_thresholds', {})
        
        # This would typically require historical data storage
        # For now, we'll implement the structure
        
        if 'price' in product and 'price' in dynamic_rules:
            price = product['price']
            price_rules = dynamic_rules['price']
            category = product.get('category', 'default')
            
            # Check if we have historical stats for this category
            historical_stats = self._get_historical_stats(category, 'price')
            
            if historical_stats:
                mean_price = historical_stats['mean']
                std_price = historical_stats['std']
                multiplier = price_rules.get('std_multiplier', 3)
                
                upper_bound = mean_price + (multiplier * std_price)
                lower_bound = mean_price - (multiplier * std_price)
                
                if price > upper_bound:
                    self._add_error('price', 'price_outlier_high', price,
                                  f"Price {price} exceeds dynamic upper bound {upper_bound:.2f}",
                                  ValidationResult.WARNING)
                
                if price < lower_bound:
                    self._add_error('price', 'price_outlier_low', price,
                                  f"Price {price} below dynamic lower bound {lower_bound:.2f}",
                                  ValidationResult.WARNING)
    
    def _validate_contextual_rules(self, product: Dict[str, Any]) -> None:
        """Apply contextual validation rules"""
        contextual_rules = self.config.get('contextual_rules', {})
        
        # Seasonal adjustments
        if 'seasonal' in contextual_rules:
            current_month = datetime.now().month
            seasonal_rules = contextual_rules['seasonal']
            
            # Check if current month has special rules
            month_rules = seasonal_rules.get(str(current_month), {})
            
            if 'price_adjustment_factor' in month_rules and 'price' in product:
                category = product.get('category', 'default')
                if category in month_rules.get('categories', []):
                    # Apply seasonal price validation
                    factor = month_rules['price_adjustment_factor']
                    # This would compare against baseline prices
                    pass
        
        # Category-specific rules
        if 'category_rules' in contextual_rules and 'category' in product:
            category = product['category']
            category_rules = contextual_rules['category_rules'].get(category, {})
            
            if 'price_change_limit' in category_rules:
                # Would need previous price to validate change
                pass
    
    def _get_historical_stats(self, category: str, field: str) -> Optional[Dict[str, float]]:
        """Get historical statistics for a category and field"""
        # This would typically query a database or cache
        # For demonstration, return mock data
        mock_stats = {
            'electronics': {'price': {'mean': 299.99, 'std': 150.0}},
            'books': {'price': {'mean': 19.99, 'std': 8.0}},
            'clothing': {'price': {'mean': 49.99, 'std': 25.0}}
        }
        
        return mock_stats.get(category, {}).get(field)
    
    def _add_error(self, field: str, rule: str, value: Any, message: str, 
                   severity: ValidationResult = ValidationResult.FAIL) -> None:
        """Add a validation error"""
        error = ValidationError(
            field=field,
            rule=rule,
            value=value,
            message=message,
            severity=severity
        )
        self.validation_errors.append(error)
    
    def validate_batch(self, products: List[Dict[str, Any]]) -> Dict[str, List[ValidationError]]:
        """Validate a batch of products"""
        results = {}
        
        for i, product in enumerate(products):
            product_id = product.get('id', f'product_{i}')
            results[product_id] = self.validate_product(product)
        
        return results
    
    def get_validation_summary(self, results: Dict[str, List[ValidationError]]) -> Dict[str, Any]:
        """Get summary statistics of validation results"""
        total_products = len(results)
        total_errors = sum(len(errors) for errors in results.values())
        failed_products = sum(1 for errors in results.values() if errors)
        
        error_by_field = {}
        error_by_rule = {}
        
        for errors in results.values():
            for error in errors:
                error_by_field[error.field] = error_by_field.get(error.field, 0) + 1
                error_by_rule[error.rule] = error_by_rule.get(error.rule, 0) + 1
        
        return {
            'total_products': total_products,
            'total_errors': total_errors,
            'failed_products': failed_products,
            'success_rate': (total_products - failed_products) / total_products * 100,
            'errors_by_field': error_by_field,
            'errors_by_rule': error_by_rule
        }

# Example usage
if __name__ == "__main__":
    # Sample product data
    sample_products = [
        {
            'id': 'prod_001',
            'title': 'Wireless Headphones',
            'price': 79.99,
            'category': 'electronics',
            'availability': 'in_stock',
            'stock_quantity': 15,
            'date': '2024-07-03T10:30:00Z'
        },
        {
            'id': 'prod_002',
            'title': 'Python Programming Book',
            'price': 39.99,
            'category': 'books',
            'availability': 'in_stock',
            'stock_quantity': 8,
            'date': '2024-07-03T09:15:00Z'
        },
        {
            'id': 'prod_003',
            'title': '<script>alert("hack")</script>Summer Dress',  # Contains HTML
            'price': -5.99,  # Negative price
            'category': 'clothing',
            'availability': 'unknown_status',  # Invalid availability
            'stock_quantity': -2,  # Negative stock
            'date': '2024-12-25T00:00:00Z'  # Future date
        }
    ]
    
    # Create validator (assumes config file exists)
    # validator = EcommerceValidator('validation_config.yaml')
    # results = validator.validate_batch(sample_products)
    # summary = validator.get_validation_summary(results)
    
    print("Validation system ready. Create a configuration file to run validation.")
    