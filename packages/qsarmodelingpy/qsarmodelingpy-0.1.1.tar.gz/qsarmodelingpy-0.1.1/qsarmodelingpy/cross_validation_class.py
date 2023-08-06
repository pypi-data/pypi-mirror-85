""" Cross-Validation routines.

From [Wikipedia](https://en.wikipedia.org/wiki/Cross-validation_(statistics)):

> Cross-validation is any of various similar model validation techniques for assessing how the results of a statistical analysis will generalize to an independent data set.
It is mainly used in settings where the goal is prediction, and one wants to estimate how accurately a predictive model will perform in practice.
In a prediction problem, a model is usually given a dataset of known data on which training is run (training dataset), and a dataset of unknown data (or first seen data) against which the model is tested (called the validation dataset or testing set).
The goal of cross-validation is to test the model's ability to predict new data that was not used in estimating it, in order to flag problems like overfitting or selection bias and to give an insight on how the model will generalize to an independent dataset (i.e., an unknown dataset, for instance from a real problem). 
"""
from sklearn.model_selection import LeaveOneOut
from sklearn.cross_decomposition import PLSRegression
import numpy as np
import pandas as pd
from math import sqrt
from sklearn.preprocessing import scale
from qsarmodelingpy.calculate_parameters import calcPress, calcR2, calcRMSE, calcR
from qsarmodelingpy.plsbdg import PLSBidiag


class CrossValidation(object):

    def __init__(self, X: pd.DataFrame, y, nLVMax: int = None, scale: bool = True) -> None:
        """ Perform the Cross Validation *via* Leave-One-Out.

        Args:
            X (DataFrame): The matrix with descriptors.
            y (DataFrame, list, array): The dependent variable vector.
            nLVMax (int, optional): Maximum number of Latent Variables. Defaults to None.
            scale (bool, optional): Defaults to True.

        ## See also:
        * `qsarmodelingpy.leaveNout`
        """
        self.X = X
        self.y = y
        if nLVMax == None:
            self.nLVMax = int(len(y)/5)
        else:
            self.nLVMax = nLVMax
        nLVMax = self.nLVMax
        # Cross validation
        ycv = np.zeros((len(y), nLVMax))
        loo = LeaveOneOut()
        for train, test in loo.split(X):
            pls = PLSBidiag(n_components=nLVMax)
            pls.fit(X[train, :], y[train])
            ycv[test, :] = pls.predict(X[test])

        # Calibration
        ycal = np.zeros((len(y), nLVMax))
        pls = PLSBidiag(n_components=nLVMax)
        pls.fit(X, y)
        ycal = pls.predict(X)

        self.ycv = ycv
        self.ycal = ycal

    def press(self):
        return [calcPress(self.y[:, 0], self.ycal[:, i]) for i in range(self.nLVMax)]

    def R2(self):
        return [calcR2(self.y[:, 0], self.ycal[:, i]) for i in range(self.nLVMax)]

    def RMSEC(self):
        return [calcRMSE(self.y[:, 0], self.ycal[:, i]) for i in range(self.nLVMax)]

    def rcal(self):
        return [calcR(self.y[:, 0], self.ycal[:, i]) for i in range(self.nLVMax)]

    def presscv(self):
        return [calcPress(self.y[:, 0], self.ycv[:, i]) for i in range(self.nLVMax)]

    def Q2(self):
        return [calcR2(self.y[:, 0], self.ycv[:, i]) for i in range(self.nLVMax)]

    def RMSECV(self):
        return [calcRMSE(self.y[:, 0], self.ycv[:, i]) for i in range(self.nLVMax)]

    def rcv(self):
        return [calcR(self.y[:, 0], self.ycv[:, i]) for i in range(self.nLVMax)]

    def returnParameters(self, nLV=None):
        if nLV == None:
            nLV = np.argmax(self.Q2())+1
        press_value = calcPress(self.y[:, 0], self.ycal[:, nLV-1])
        R2_value = calcR2(self.y[:, 0], self.ycal[:, nLV-1])
        RMSEC_value = calcRMSE(self.y[:, 0], self.ycal[:, nLV-1])
        rcal_value = calcR(self.y[:, 0], self.ycal[:, nLV-1])
        presscv_value = calcPress(self.y[:, 0], self.ycv[:, nLV-1])
        Q2_value = calcR2(self.y[:, 0], self.ycv[:, nLV-1])
        RMSECV_value = calcRMSE(self.y[:, 0], self.ycv[:, nLV-1])
        rcv_value = calcR(self.y[:, 0], self.ycv[:, nLV-1])
        scaledy = (self.y[:, 0]-min(self.y[:, 0])) / \
            (max(self.y[:, 0])-min(self.y[:, 0]))
        scaledycal = (self.ycal[:, nLV-1]-min(self.y[:, 0])) / \
            (max(self.y[:, 0])-min(self.y[:, 0]))
        scaled_k = sum(scaledy*scaledycal)/sum(scaledycal**2)
        scaled_k1 = sum(scaledy*scaledycal)/sum(scaledy**2)
        scaled_yr0 = scaled_k*scaledycal
        scaled_y1r0 = scaled_k1*scaledy
        scaled_R02 = calcR2(scaledy, scaled_yr0)
        scaled_R102 = calcR2(scaledycal, scaled_y1r0)
        r2cal = (calcR(np.reshape(scaledy, len(scaledy)),
                       np.reshape(scaledycal, len(scaledy))))**2
        rm2 = r2cal*(1-sqrt(abs(r2cal-scaled_R02)))
        rm12 = r2cal*(1-sqrt(abs(r2cal-scaled_R102)))
        avgrmcal = (rm2+rm12)/2
        deltarmcal = abs(rm2-rm12)
        scaledycv = (self.ycv[:, nLV-1]-min(self.y[:, 0])) / \
            (max(self.y[:, 0])-min(self.y[:, 0]))
        scaled_k = sum(scaledy*scaledycv)/sum(scaledycv**2)
        scaled_k1 = sum(scaledy*scaledycv)/sum(scaledy**2)
        scaled_yr0 = scaled_k*scaledycv
        scaled_y1r0 = scaled_k1*scaledy
        scaled_R02 = calcR2(scaledy, scaled_yr0)
        scaled_R102 = calcR2(scaledycv, scaled_y1r0)
        r2cv = (calcR(np.reshape(scaledy, len(scaledy)),
                      np.reshape(scaledycv, len(scaledy))))**2
        rm2 = r2cv*(1-sqrt(abs(r2cv-scaled_R02)))
        rm12 = r2cv*(1-sqrt(abs(r2cv-scaled_R102)))
        avgrmcv = (rm2+rm12)/2
        deltarmcv = abs(rm2-rm12)
        F = (np.shape(self.X)[0]-nLV-1)*R2_value/(nLV*(1-R2_value))
        param = [press_value, R2_value, RMSEC_value, rcal_value, avgrmcal, deltarmcal, presscv_value, Q2_value,
                 RMSECV_value, rcv_value, avgrmcv, deltarmcv, F, nLV]
        dfcv = pd.DataFrame(index=["PRESS", "R2", "RMSEC", "rcal", "avgRmcal", "deltaRmcal", "PRESSCV", "Q2",
                                   "RMSECV", "rcv", "avgRmcv", "deltaRmcv", "F", "nLV"],
                            data=np.array(param))
        return dfcv

    def saveParameters(self, fileName, nLV=None) -> None:
        """Save `filename` containing the calculated parameters for CrossValidation.

        Args:
            fileName (str, path, file-like, `io`): The filename to be saved.
            nLV (int, optional): Number of Latent Variables. Defaults to None.
        """
        df = self.returnParameters(nLV)
        df.to_csv(fileName, sep=',', header=False)
