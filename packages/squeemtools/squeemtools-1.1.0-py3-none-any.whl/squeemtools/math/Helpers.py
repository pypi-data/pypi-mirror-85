import numpy as np
def Augment(X):
    '''Takes in n-dimensional X and returns n+1-dimensional (augmented) X'''
    return np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)