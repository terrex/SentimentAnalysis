__author__ = 'terrex'

from sklearn.datasets.base import Bunch
import numpy as np

__all__ = ('VectorizerI', 'SkLearnVectorizer')


class VectorizerI(object):
    def vectorize(self, train_samples: list):
        raise NotImplementedError()


class SkLearnVectorizer(VectorizerI):
    def vectorize(self, train_samples: list):
        count = len(train_samples)
        data = np.empty((count, train_samples[0].feats['vec'].shape[0]))
        target = np.empty((count,))
        bunch = Bunch(data=data, target=target)
        """
            return Bunch(data=data, target=target,
                 target_names=target_names,
                 DESCR=fdescr,
                 feature_names=['sepal length (cm)', 'sepal width (cm)',
                                'petal length (cm)', 'petal width (cm)'])
"""
        return bunch

