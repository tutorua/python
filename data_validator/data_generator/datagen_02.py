import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='whitegrid')
n = 1000

# Generate data
normal_data = np.array(stats.norm.rvs(loc=0, scale=1, size=n))
beta_data   = np.array(stats.beta.rvs(a=2, b=5, size=n))
gamma_data  = np.array(stats.gamma.rvs(a=2, scale=2, size=n))

# Create subplots
fig, axes = plt.subplots(3, 2, figsize=(14, 12))  # 3 rows, 2 columns

# 🔵 Normal
sns.histplot(data=normal_data, kde=True, ax=axes[0, 0], color="skyblue")
axes[0, 0].set_title("Normal Distribution - Histogram + KDE")
sns.stripplot(x=normal_data, ax=axes[0, 1], color="dodgerblue", size=2, alpha=0.3)
axes[0, 1].set_title("Normal Distribution - Data Points")

# 🟢 Beta
sns.histplot(data=beta_data, kde=True, ax=axes[1, 0], color="lightgreen")
axes[1, 0].set_title("Beta Distribution - Histogram + KDE")
sns.stripplot(x=beta_data, ax=axes[1, 1], color="green", size=2, alpha=0.3)
axes[1, 1].set_title("Beta Distribution - Data Points")

# 🔴 Gamma
sns.histplot(data=gamma_data, kde=True, ax=axes[2, 0], color="salmon")
axes[2, 0].set_title("Gamma Distribution - Histogram + KDE")
sns.stripplot(x=gamma_data, ax=axes[2, 1], color="red", size=2, alpha=0.3)
axes[2, 1].set_title("Gamma Distribution - Data Points")

plt.tight_layout()
plt.show()
