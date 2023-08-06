# Model via a Random Forest
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

parameters = {'max_depth':[2,3,4]}

model = RandomForestRegressor()
regs = GridSearchCV(model, parameters, cv=10)
regs.fit(X_train, y_train)
reg = regs.best_estimator_