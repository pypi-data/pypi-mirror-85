# Model via Decision tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

parameters = {'criterion':['gini', 'entropy'], 'max_depth':[1,2,3,4], 'min_samples_leaf':[20]}

model = DecisionTreeClassifier()
clfs = GridSearchCV(model, parameters, cv=10)
clfs.fit(X_train, y_train)
clf = clfs.best_estimator_