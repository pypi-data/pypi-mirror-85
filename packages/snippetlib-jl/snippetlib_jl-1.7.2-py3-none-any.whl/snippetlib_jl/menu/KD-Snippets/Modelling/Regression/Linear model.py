# Model via linear regression

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV

parameters = {'normalize':[True,False]}


model = LinearRegression()
regs = GridSearchCV(model, parameters, cv=10)
regs.fit(X_train, y_train)
reg = regs.best_estimator_