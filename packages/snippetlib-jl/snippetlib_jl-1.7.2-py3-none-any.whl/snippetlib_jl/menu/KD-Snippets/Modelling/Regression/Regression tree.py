# Model via regression tree
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

parameters = {'criterion':['mse','friedman_mse'], 'max_depth':[2,3,4], 'min_samples_leaf':[10,20,50]}

model = DecisionTreeRegressor()
regs = GridSearchCV(model, parameters, cv=10)
regs.fit(X_train, y_train)
reg = regs.best_estimator_