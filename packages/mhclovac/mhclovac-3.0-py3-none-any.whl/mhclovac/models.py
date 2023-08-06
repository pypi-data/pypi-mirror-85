from sklearn.ensemble import RandomForestRegressor, VotingRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, BayesianRidge
from sklearn.ensemble import RandomForestClassifier, VotingClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
import pandas as pd


class BindingPredictor:

    scaler = None
    vote_reg = None
    classifier = None

    def __init__(self, random_state=None, n_jobs=-1, standardize_data=True):
        if standardize_data:
            self.scaler = StandardScaler()
        estimators = [
            ('rf', RandomForestRegressor(random_state=random_state, max_depth=3)),
            ('lr', LinearRegression(normalize=True)),
            ('br', BayesianRidge(normalize=True)),
            ('gb', GradientBoostingRegressor(random_state=random_state, max_depth=4))
        ]
        self.estimators = estimators
        self.vote_reg = VotingRegressor(estimators, n_jobs=n_jobs)

    def fit(self, X, y):
        if self.scaler:
            self.scale_fit(X)
            X = self.scale_transform(X)
        self.vote_reg.fit(X, y)

    def predict(self, X):
        if self.scaler:
            X = self.scale_transform(X)
        return self.vote_reg.predict(X)

    def score(self, X, y):
        if self.scaler:
            X = self.scale_transform(X)
        return self.vote_reg.score(X, y)

    def scale_fit(self, X):
        self.scaler.fit(X)

    def scale_transform(self, X):
        scaled = self.scaler.transform(X)
        scaled = pd.DataFrame(scaled, index=X.index)
        return scaled


class EpitopePredictor:

    scaler = None
    vote_reg = None
    estimators = None

    def __init__(self, random_state=None, n_jobs=-1, standardize_data=True):
        if standardize_data:
            self.scaler = StandardScaler()
        estimators = [
            ('rf', RandomForestClassifier(random_state=random_state, max_depth=3)),
            ('lr', LogisticRegression(max_iter=1000, random_state=random_state, solver='saga')),
            ('nb', GaussianNB()),
            ('gd', GradientBoostingClassifier(random_state=random_state, max_depth=4))
        ]
        self.estimators = estimators
        self.vote_reg = VotingClassifier(estimators, n_jobs=n_jobs, voting='soft')

    def fit(self, X, y):
        if self.scaler:
            self.scale_fit(X)
            X = self.scale_transform(X)
        self.vote_reg.fit(X, y)

    def predict(self, X):
        if self.scaler:
            X = self.scale_transform(X)
        return self.vote_reg.predict(X)

    def predict_proba(self, X):
        if self.scaler:
            X = self.scale_transform(X)
        return [x[1] for x in self.vote_reg.predict_proba(X)]

    def score(self, X, y):
        if self.scaler:
            X = self.scale_transform(X)
        return self.vote_reg.score(X, y)

    def scale_fit(self, X):
        self.scaler.fit(X)

    def scale_transform(self, X):
        scaled = self.scaler.transform(X)
        scaled = pd.DataFrame(scaled, index=X.index)
        return scaled
