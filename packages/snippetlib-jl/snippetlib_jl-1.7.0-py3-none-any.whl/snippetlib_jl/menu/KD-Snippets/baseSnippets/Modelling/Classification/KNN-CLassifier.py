# Model via KNN Classifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

parameters = {'n_neighbors':[1,3,5], 'weights':['uniform', 'distance']}

model = KNeighborsClassifier()
clfs = GridSearchCV(model, parameters, cv=10)
clfs.fit(X_train, y_train)
clf = clfs.best_estimator_