# read the parameters for a distribution from yaml settings file
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

# 🎛 Load settings from YAML
with open("config_01.yaml", "r") as file:
    config = yaml.safe_load(file)

sns.set_theme(style='whitegrid')

# 🧪 Generate data from YAML parameters
normal_data = np.array(stats.norm.rvs(
    loc=config['normal']['loc'],
    scale=config['normal']['scale'],
    size=config['normal']['size']
))

beta_data = np.array(stats.beta.rvs(
    a=config['beta']['a'],
    b=config['beta']['b'],
    size=config['beta']['size']
))

gamma_data = np.array(stats.gamma.rvs(
    a=config['gamma']['a'],
    scale=config['gamma']['scale'],
    size=config['gamma']['size']
))

# 📊 Plotting
fig, axes = plt.subplots(3, 2, figsize=(14, 12))

# Normal
sns.histplot(data=normal_data, kde=True, ax=axes[0, 0], color="skyblue")
axes[0, 0].set_title("Normal Distribution - Histogram")
sns.stripplot(x=normal_data, ax=axes[0, 1], color="dodgerblue", size=2, alpha=0.3)
axes[0, 1].set_title("Normal Distribution - Data Points")

# Beta
sns.histplot(data=beta_data, kde=True, ax=axes[1, 0], color="lightgreen")
axes[1, 0].set_title("Beta Distribution - Histogram")
sns.stripplot(x=beta_data, ax=axes[1, 1], color="green", size=2, alpha=0.3)
axes[1, 1].set_title("Beta Distribution - Data Points")

# Gamma
sns.histplot(data=gamma_data, kde=True, ax=axes[2, 0], color="salmon")
axes[2, 0].set_title("Gamma Distribution - Histogram")
sns.stripplot(x=gamma_data, ax=axes[2, 1], color="red", size=2, alpha=0.3)
axes[2, 1].set_title("Gamma Distribution - Data Points")

plt.tight_layout()
plt.show()
