from unittest import TestCase
from sklearn import datasets
from randomsubgroups import RandomSubgroupClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

data = datasets.load_wine()
cols = data.feature_names
target = pd.Series(data.target)
data = pd.DataFrame(data.data)
data.columns = cols

Xtr, Xtt, ytr, ytt = train_test_split(data, target, test_size=0.3, random_state=42)


class TestRandomSubgroupClassifier(TestCase):
    def setUp(self):
        self.rsc = RandomSubgroupClassifier(n_estimators=10)
        self.rsc.fit(Xtr, ytr)


class TestMethods(TestRandomSubgroupClassifier):
    def test_estimators(self):
        self.assertEqual(self.rsc.n_estimators, 10)

    def test_estimators(self):
        self.assertEqual(self.rsc.n_estimators, 10)

    def test_estimators(self):
        self.assertEqual(self.rsc.n_estimators, 10)