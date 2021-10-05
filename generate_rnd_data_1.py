# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 22:24:08 2016

@author: Igor
"""

# Generate a dataset and plot it
from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(0)
X, y = sklearn.datasets.make_moons(200, noise=0.20)
plt.scatter(X[:,0], X[:,1], s=40, c=y, cmap=plt.cm.Spectral)