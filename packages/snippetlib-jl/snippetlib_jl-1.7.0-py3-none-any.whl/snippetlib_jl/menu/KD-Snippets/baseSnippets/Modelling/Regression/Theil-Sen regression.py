# Model via linear regression
from sklearn.linear_model import TheilSenRegressor

reg = TheilSenRegressor()
reg.fit(X_train, y_train)