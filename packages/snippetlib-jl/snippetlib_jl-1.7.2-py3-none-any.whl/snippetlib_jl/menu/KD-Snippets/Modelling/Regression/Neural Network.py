# Model via a simple Feed Foreward Neural Network
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV

parameters = {'activation':['tanh', 'relu'], 
              'hidden_layer_sizes':[(10, 10, 10,), (50, 10,), (100,)], 
              'solver':['lbfgs', 'adam', 'sgd'], 
              'alpha':[0.001, 0.01, 0.1]}

model = MLPRegressor()
regs = GridSearchCV(model, parameters, cv=10)
regs.fit(X_train, y_train)
reg = regs.best_estimator_