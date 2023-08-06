# Model via support vector machine
from sklearn import svm
from sklearn.model_selection import GridSearchCV

#parameters = [
#              {'C': [1, 10, 100, 1000], 'kernel': ['linear']}, # takes forever on this dataset
#              {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']},
#             ]

parameters = {'kernel':['rbf'], 'C':10.0**np.arange(-5, 5), 'gamma':10.0**np.arange(-5,5)}

model = svm.SVC()
clfs = GridSearchCV(model, parameters, cv=10)
clfs.fit(X_train, y_train)
clf = clfs.best_estimator_