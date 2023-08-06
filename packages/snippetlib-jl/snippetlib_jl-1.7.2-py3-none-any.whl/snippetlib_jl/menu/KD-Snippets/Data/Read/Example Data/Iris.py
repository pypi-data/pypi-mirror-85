# Load the legendary iris example dataset
import pandas as pd
from sklearn import datasets

iris = datasets.load_iris()
data = pd.DataFrame(iris['data'], columns=[name.replace(' (cm)', '').replace(' ', '_') for name in iris['feature_names']])
data['Species'] = [iris['target_names'][i] for i in iris['target']]
data['Species_numeric'] = iris['target']
data.head()