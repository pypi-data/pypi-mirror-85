# Model via support vector machine
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV

parameters = {'kernel':['rbf'], 'C':10.0**np.arange(-4, 4), 'epsilon':[0.1, 0.2]}

model = SVR()
regs = GridSearchCV(model, parameters, cv=10)
regs.fit(X_train, y_train)
reg = regs.best_estimator_