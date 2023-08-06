# Get x-validation performance of a trained classifier clf
from sklearn.model_selection import cross_val_score

scores = cross_val_score(clf, X_train, y_train, scoring='f1', cv=10)
print(scores.mean(), "+/-", scores.std())