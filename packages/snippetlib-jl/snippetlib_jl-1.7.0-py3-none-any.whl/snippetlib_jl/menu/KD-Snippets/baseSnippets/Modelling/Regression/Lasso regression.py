# Model via lasso regression
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV

parameters = {'alpha':10.0**np.arange(-5,6), 'normalize':[True,False]}

model = Lasso()
regs = GridSearchCV(model, parameters, cv=10)
regs.fit(X_train, y_train)
reg = regs.best_estimator_