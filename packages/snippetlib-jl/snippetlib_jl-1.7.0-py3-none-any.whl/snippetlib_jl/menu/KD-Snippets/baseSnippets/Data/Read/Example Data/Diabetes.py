# Load the legendary diabetes example dataset
import pandas as pd
from sklearn import datasets

rawdata = datasets.load_diabetes()
data = pd.DataFrame(rawdata['data'], columns=rawdata['feature_names'])
data['Target'] = rawdata['target']
data.head()