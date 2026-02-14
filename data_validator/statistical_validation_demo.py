import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

# Demo script for statistical validation system
class StatisticalValidationDemo:
    def __init__(self):
        self.historical_data = self.generate_historical_data()
        self.current_data = self.generate_current_data()
        
    def generate_historical_data(self) -> List[Dict[str, Any]]:
        """Generate realistic historical e-commerce data"""
        np.random.seed(42)  # For reproducibility
        
        # Generate 1000 historical records over 90 days
        historical_data = []
        base_date = datetime.now() - timedelta(days=90)
        
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
        brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
        
        for i in range(1000):
            # Create realistic price distributions
            if random.choice(categories) == 'Electronics':
                base_price = np.random.lognormal(5.5, 0.8)  # Higher prices for electronics
            elif random.choice(categories) == 'Books':
                base_price = np.random.lognormal(2.5, 0.5)  # Lower prices for books
            else:
                base_price = np.random.lognormal(3.5, 0.7)  # Medium prices for others
            
            # Add some seasonality and trends
            days_ago = random.randint(0, 89)
            date = base_date + timedelta(days=days_ago)
            seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * days_ago / 365)
            
            record = {
                'id': f'prod_{i+1}',
                'name': f'Product {i+1}',
                'category': random.choice(categories),
                'brand': random.choice(brands),
                'price': round(base_price * seasonal_factor, 2),
                'rating': round(random.uniform(3.0, 5.0), 1),
                'review_count': random.randint(5, 500),
                'availability': random.choice(['In Stock', 'Out of Stock', 'Limited']),
                'discount_percent': random.randint(0, 50),
                'shipping_cost': round(random.uniform(0, 25), 2),
                'scraped_at': date.isoformat(),
                'source': random.choice(['site_a', 'site_b', 'site_c'])
            }
            historical_data.append(record)
        
        return historical_data
    
    def generate_current_data(self) -> List[Dict[str, Any]]:
        """Generate current data with some anomalies for testing"""
        np.random.seed(123)  # Different seed for current data
        
        current_data = []
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports']
        brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
        
        for i in range(100):
            # Most data should be normal
            if i < 80:
                # Normal data similar to historical
                if random.choice(categories) == 'Electronics':
                    base_price = np.random.lognormal(5.5, 0.8)
                elif random.choice(categories) == 'Books':
                    base_price = np.random.lognormal(2.5, 0.5)
                else:
                    base_price = np.random.lognormal(3.5, 0.7)
                
                rating = round(random.uniform(3.0, 5.0), 1)
                review_count = random.randint(5, 500)
                discount = random.randint(0, 50)
                
            else:
                # Introduce anomalies in last 20 records
                if i < 85:
                    # Price anomalies
                    base_price = np.random.lognormal(8.0, 1.2)  # Much higher prices
                elif i < 90:
                    # Rating anomalies
                    base_price = np.random.lognormal(3.5, 0.7)
                    rating = round(random.uniform(1.0, 2.0), 1)  # Very low ratings
                    review_count = random.randint(5, 500)
                    discount = random.randint(0, 50)
                elif i < 95:
                    # Review count anomalies
                    base_price = np.random.lognormal(3.5, 0.7)
                    rating = round(random.uniform(3.0, 5.0), 1)
                    review_count = random.randint(1000, 5000)  # Very high review counts
                    discount = random.randint(0, 50)
                else:
                    # Discount anomalies
                    base_price = np.random.lognormal(3.5, 0.7)
                    rating = round(random.uniform(3.0, 5.0), 1)
                    review_count = random.randint(5, 500)
                    discount = random.randint(80, 99)  # Unrealistic discounts
            
            record = {
                'id': f'current_prod_{i+1}',
                'name': f'Current Product {i+1}',
                'category': random.choice(categories),
                'brand': random.choice(brands),
                'price': round(base_price, 2),
                'rating': rating,
                'review_count': review_count,
                'availability': random.choice(['In Stock', 'Out of Stock', 'Limited']),
                'discount_percent': discount,
                'shipping_cost': round(random.uniform(0, 25), 2),
                'scraped_at': datetime.now().isoformat(),
                'source': random.choice(['site_a', 'site_b', 'site_c'])
            }
            current_data.append(record)
        
        return current_data
    
    def save_data_to_files(self):
        """Save generated data to JSON files"""
        with open('historical_data.json', 'w') as f:
            json.dump(self.historical_data, f, indent=2)
        
        with open('current_data.json', 'w') as f:
            json.dump(self.current_data, f, indent=2)
        
        print("Data saved to historical_data.json and current_data.json")
    
    def display_data_summary(self):
        """Display summary statistics of the generated data"""
        hist_df = pd.DataFrame(self.historical_data)
        curr_df = pd.DataFrame(self.current_data)
        
        print("=== HISTORICAL DATA SUMMARY ===")
        print(f"Total records: {len(hist_df)}")
        print(f"Date range: {hist_df['scraped_at'].min()} to {hist_df['scraped_at'].max()}")
        print(f"Categories: {hist_df['category'].unique()}")
        print(f"Price range: ${hist_df['price'].min():.2f} - ${hist_df['price'].max():.2f}")
        print(f"Average price: ${hist_df['price'].mean():.2f}")
        print(f"Rating range: {hist_df['rating'].min()} - {hist_df['rating'].max()}")
        print(f"Review count range: {hist_df['review_count'].min()} - {hist_df['review_count'].max()}")
        print()
        
        print("=== CURRENT DATA SUMMARY ===")
        print(f"Total records: {len(curr_df)}")
        print(f"Categories: {curr_df['category'].unique()}")
        print(f"Price range: ${curr_df['price'].min():.2f} - ${curr_df['price'].max():.2f}")
        print(f"Average price: ${curr_df['price'].mean():.2f}")
        print(f"Rating range: {curr_df['rating'].min()} - {curr_df['rating'].max()}")
        print(f"Review count range: {curr_df['review_count'].min()} - {curr_df['review_count'].max()}")
        print()


# Demo usage of the validation system
def run_validation_demo():
    """Run the complete validation demo"""
    print("=== STATISTICAL VALIDATION SYSTEM DEMO ===")
    print()
    
    # Generate demo data
    demo = StatisticalValidationDemo()
    demo.save_data_to_files()
    demo.display_data_summary()
    
    # Import the validation system (assuming the files exist)
    try:
        from statistical_validator import StatisticalValidator
        from threshold_config import ThresholdConfig
        
        # Initialize the validation system
        print("=== INITIALIZING VALIDATION SYSTEM ===")
        validator = StatisticalValidator()
        
        # Load historical data for baseline calculation
        print("Loading historical data...")
        historical_df = pd.DataFrame(demo.historical_data)
        validator.calculate_baseline_stats(historical_df)
        
        # Configure thresholds
        print("Configuring validation thresholds...")
        config = ThresholdConfig()
        
        # Set custom thresholds for our demo
        config.set_threshold('price', 'z_score', 3.0)
        config.set_threshold('price', 'iqr_multiplier', 2.5)
        config.set_threshold('rating', 'z_score', 2.5)
        config.set_threshold('review_count', 'z_score', 3.0)
        config.set_threshold('discount_percent', 'range', (0, 70))  # Max 70% discount
        
        # Validate current data
        print("\n=== VALIDATING CURRENT DATA ===")
        current_df = pd.DataFrame(demo.current_data)
        
        validation_results = []
        anomaly_count = 0
        
        for idx, record in current_df.iterrows():
            result = validator.validate_record(record.to_dict(), config)
            validation_results.append(result)
            
            if not result['is_valid']:
                anomaly_count += 1
                print(f"\n🚨 ANOMALY DETECTED - Record {idx + 1}:")
                print(f"   Product: {record['name']}")
                print(f"   Category: {record['category']}")
                print(f"   Issues found:")
                for issue in result['issues']:
                    print(f"     - {issue}")
                print(f"   Confidence: {result['confidence']:.2f}")
        
        # Summary statistics
        print(f"\n=== VALIDATION SUMMARY ===")
        print(f"Total records validated: {len(validation_results)}")
        print(f"Valid records: {len(validation_results) - anomaly_count}")
        print(f"Anomalies detected: {anomaly_count}")
        print(f"Anomaly rate: {(anomaly_count/len(validation_results)*100):.1f}%")
        
        # Show some examples of valid records
        print(f"\n=== SAMPLE VALID RECORDS ===")
        valid_count = 0
        for idx, result in enumerate(validation_results):
            if result['is_valid'] and valid_count < 3:
                record = current_df.iloc[idx]
                print(f"✅ Record {idx + 1}: {record['name']}")
                print(f"   Price: ${record['price']:.2f}, Rating: {record['rating']}, Reviews: {record['review_count']}")
                valid_count += 1
        
        # Generate validation report
        print(f"\n=== GENERATING VALIDATION REPORT ===")
        report = validator.generate_validation_report(validation_results)
        
        # Save report to file
        with open('validation_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print("Validation report saved to validation_report.json")
        
        # Display key metrics from report
        print(f"\nKey Metrics:")
        print(f"- Total records: {report['summary']['total_records']}")
        print(f"- Valid records: {report['summary']['valid_records']}")
        print(f"- Invalid records: {report['summary']['invalid_records']}")
        print(f"- Validation rate: {report['summary']['validation_rate']:.1f}%")
        
        if report['field_analysis']:
            print(f"\nField Analysis:")
            for field, analysis in report['field_analysis'].items():
                if analysis['anomaly_count'] > 0:
                    print(f"- {field}: {analysis['anomaly_count']} anomalies detected")
    
    except ImportError as e:
        print(f"⚠️  Could not import validation modules: {e}")
        print("Please ensure statistical_validator.py and threshold_config.py are in the same directory")
        print("Demo data has been generated and saved to files for manual testing")


if __name__ == "__main__":
    run_validation_demo()
    