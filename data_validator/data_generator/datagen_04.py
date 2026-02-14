import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

# Load config
with open("config_02.yaml", "r") as file:
    config = yaml.safe_load(file)

sns.set(style='whitegrid')

distributions = {}
plots = []

# Dynamically generate data
for name, settings in config['distributions'].items():
    dist_name = settings['dist']
    params = settings['params'].copy()
    size = params.pop('size', 1000)
    
    dist_func = getattr(stats, dist_name)
    data = np.array(dist_func.rvs(size=size, **params))
    
    distributions[name] = data
    plots.append((name, data))

# Create subplot grid
fig, axes = plt.subplots(len(plots), 2, figsize=(14, 4 * len(plots)))

if len(plots) == 1:
    axes = [axes]  # Ensure 2D structure for single plot

# Plotting
for i, (name, data) in enumerate(plots):
    sns.histplot(data=data, kde=True, ax=axes[i][0])
    axes[i][0].set_title(f"{name.title()} - Histogram + KDE")

    sns.stripplot(x=data, ax=axes[i][1], color="gray", size=2, alpha=0.3)
    axes[i][1].set_title(f"{name.title()} - Data Points")

plt.tight_layout()
plt.show()