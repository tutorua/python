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
        
        # Generate 1000 historical records over 90