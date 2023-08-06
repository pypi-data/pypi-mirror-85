# Model via KNN Regressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV

parameters = {'n_neighbors':[1,3,5], 'weights':['uniform', 'distance']}


model = KNeighborsRegressor()
regs = GridSearchCV(model, parameters, cv=10)
regs.fit(X_train, y_train)
reg = regs.best_estimator_