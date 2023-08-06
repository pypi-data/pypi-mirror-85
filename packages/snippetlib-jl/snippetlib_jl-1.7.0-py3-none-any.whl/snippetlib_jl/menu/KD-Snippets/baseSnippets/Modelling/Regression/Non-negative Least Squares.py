# Model via non-negative Least Squares
from scipy.optimize import nnls

class NNLS():
    def __init__(self):
        self.coef_ = None
    def get_params(self, deep=False, *args):
        return {}
    def fit(self, X, Y):
        self.coef_ = nnls(X,Y)[0]
    def predict(self, X):
        return self.coef_.dot(np.array(X).T)

reg = NNLS()
reg.fit(X_train, y_train)