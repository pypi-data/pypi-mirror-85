from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV

parameters = {'n_estimators':[2, 5, 10, 50, 100], 
              'max_depth':[3, 4, 5], 
              'learning_rate':[0.001, 0.01, 0.1]}

model = GradientBoostingClassifier()
clfs = GridSearchCV(model, parameters, cv=3)
clfs.fit(X_train, y_train)
clf = clfs.best_estimator_