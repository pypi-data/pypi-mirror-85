# Andrews curves plot a parametrized harmonic function for each data record. 
# Similarity in lines indicates a similarity over the data records values. Nice for spotting clusters
from pandas.plotting import andrews_curves

color_by = 'Target'
plt.figure(figsize=(10,7))
curves = andrews_curves(data, color_by, alpha=0.5)
plt.grid(False)