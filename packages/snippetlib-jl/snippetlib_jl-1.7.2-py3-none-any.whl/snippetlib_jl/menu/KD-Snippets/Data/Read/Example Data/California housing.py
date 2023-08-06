# Load the california housing dataset
import pandas as pd
from sklearn.datasets.california_housing import fetch_california_housing
cal_housing = fetch_california_housing()

data = pd.DataFrame(cal_housing['data'], columns=cal_housing['feature_names'])
data['Target'] = cal_housing['target']
print(cal_housing['DESCR'])
data.head()