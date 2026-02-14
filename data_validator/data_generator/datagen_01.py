import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Set the aesthetic style of the plots
sns.set(style='whitegrid')

# Number of samples
n = 1000

# 🎯 Generate random samples from three distributions
normal_data = np.array(stats.norm.rvs(loc=0, scale=1, size=n))
beta_data   = np.array(stats.beta.rvs(a=2, b=5, size=n))
gamma_data  = np.array(stats.gamma.rvs(a=2, scale=2, size=n))


# 📊 Plotting
plt.figure(figsize=(15, 5))

# Normal Distribution
plt.subplot(1, 3, 1)
sns.histplot(normal_data, kde=True, color="skyblue")
plt.title("Normal Distribution (μ=0, σ=1)")

# Beta Distribution
plt.subplot(1, 3, 2)
sns.histplot(beta_data, kde=True, color="lightgreen")
plt.title("Beta Distribution (α=2, β=5)")

# Gamma Distribution
plt.subplot(1, 3, 3)
sns.histplot(gamma_data, kde=True, color="salmon")
plt.title("Gamma Distribution (α=2, θ=2)")

plt.tight_layout()
plt.show()
