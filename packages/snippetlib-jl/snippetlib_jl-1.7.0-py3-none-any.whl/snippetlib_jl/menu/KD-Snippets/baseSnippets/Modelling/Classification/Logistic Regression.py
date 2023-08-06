from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

parameters = {'penalty':['l1', 'l2', 'elasticnet', 'none'], 
              'C':[0.01, 0.1, 0.0, 1.0, 10.0]}

model = LogisticRegression()
clfs = GridSearchCV(model, parameters, cv=3)
clfs.fit(X_train, y_train)
clf = clfs.best_estimator_