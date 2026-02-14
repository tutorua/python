from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import scipy.stats as stats
import yaml

app = FastAPI()

# Load YAML config
with open("config_02.yaml", "r") as f:
    config = yaml.safe_load(f)

@app.get("/generate")
def generate_data():
    results = {}
    for name, settings in config['distributions'].items():
        dist_name = settings['dist']
        params = settings['params'].copy()
        size = params.pop('size', 1000)

        dist_func = getattr(stats, dist_name)
        data = dist_func.rvs(size=size, **params)
        results[name] = data.tolist()  # Convert NumPy array to list for JSON serialization

    return {"generated_data": results}