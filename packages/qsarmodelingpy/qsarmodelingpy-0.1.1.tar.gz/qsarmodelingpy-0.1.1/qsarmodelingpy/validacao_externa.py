""" **DEPRECATED.**

Throw an error when imported. Use `qsarmodelingpy.external_validation` instead."""
import logging

logging.error(
    "`qsarmodelingpy.validacao_externa` was removed. Use `qsarmodelingpy.external_validation` instead.")

###############################
###############################
###############################
###############################
###############################
###############################
# from sklearn.model_selection import ShuffleSplit
# from sklearn.cross_decomposition import PLSRegression
# from qsarmodelingpy.cross_validation_class import CrossValidation
# from qsarmodelingpy.calculate_parameters import ssy, calcPress, calcR, calcR2, calcMAE, calcRMSE
# import numpy as np
# import pandas as pd
# import math
# import sys
# import json
# import os


# class ExternalValidation(object):
#     def __init__(self, X, y, nLV=None):
#         super(ExternalValidation, self).__init__()
#         self.X = X
#         self.y = y
#         self.nLV = nLV

#     def validateExtVal(self, train, test, nLV=None):
#         X = self.X
#         y = self.y
#         nLV = self.nLV
#         if nLV == None:
#             cv = CrossValidation(X[train, :], y[train])
#             nLV = np.argmax(cv.Q2())+1
#         pls = PLSRegression(n_components=nLV)
#         pls.fit(X[train, :], y[train])
#         yp = pls.predict(X[test])
#         Q2F1 = calcR2(y[test], yp, np.mean(y[train]))
#         Q2F2 = calcR2(y[test], yp)
#         # Q2F3 = 1-((ytest-ypred).T.dot(ytest-ypred)/len(ytest))/((ytrain-ytrain.mean()).T.dot(ytrain-ytrain.mean())/len(ytrain))
#         MAE = calcMAE(y[test], yp)
#         residuals = np.reshape(yp-y[test], len(test))
#         sd = np.std(abs(residuals), ddof=1)
#         higher_residuals = np.argsort(-abs(residuals)
#                                       )[:math.ceil(0.05*len(test))]
#         higher_residuals = [test[i] for i in higher_residuals]
#         new_test = [i for i in test if i not in higher_residuals]
#         yp = pls.predict(X[new_test])
#         Q2F195 = calcR2(y[new_test], yp, np.mean(y[train]))
#         Q2F295 = calcR2(y[new_test], yp)
#         MAE95 = calcMAE(y[new_test], yp)
#         residuals95 = np.reshape(abs(yp-y[new_test]), len(new_test))
#         sd95 = np.std(residuals95, ddof=1)
#         tr = max(y[train]) - min(y[train])
#         NE = [i for i in residuals if i < 0]
#         PE = [i for i in residuals if i > 0]
#         nNE = len(NE)
#         nPE = len(PE)
#         mNE = abs(np.mean(NE))
#         mPE = np.mean(PE)
#         if (nNE == 0) or (nPE == 0) or (nNE/nPE > 5) or (nPE/nNE > 5):
#             return False
#         if (MAE95 <= 0.1*tr) and (MAE95 + 3*sd95 <= 0.2*tr):
#             if Q2F1 > 0.5 and Q2F2 > 0.5:
#                 return True
#             else:
#                 return False
#         else:
#             return False

#     def searchValidExtVal(self, nLV=None, n_test=10, n_splits=100):
#         X = self.X
#         y = self.y
#         nLV = self.nLV
#         if nLV == None:
#             cv = CrossValidation(X, y)
#             nLV = np.argmax(cv.Q2())+1
#         N_SPLITS = n_splits
#         TEST_SIZE = n_test/len(y)
#         ss = ShuffleSplit(n_splits=N_SPLITS, test_size=TEST_SIZE)
#         pls = PLSRegression(n_components=nLV)
#         # yp = np.zeros((self.n_test,N_SPLITS))
#         # R2 = np.zeros(N_SPLITS)
#         R2 = np.zeros(0)
#         Q2 = np.zeros(0)
#         i = 0
#         tests_sets = []
#         for train, test in ss.split(X):
#             # teste com conjunto teste fixo para ver se parametros estão sendo calculados corretamente
#             # test = [23, 47, 6, 25, 40, 13, 48, 30, 43, 19]
#             # train = [i for i in range(len(y)) if i not in test]
#             cv = CrossValidation(X[train, :], y[train])
#             nLV = np.argmax(cv.Q2())+1
#             pls = PLSRegression(n_components=nLV)
#             pls.fit(X[train, :], y[train])
#             yp = pls.predict(X[test])
#             Q2F1 = calcR2(y[test], yp, np.mean(y[train]))
#             Q2F2 = calcR2(y[test], yp)
#             MAE = calcMAE(y[test], yp)
#             # print(Q2F1)
#             # print(Q2F2)
#             # print(MAE)
#             residuals = np.reshape(yp-y[test], len(test))
#             sd = np.std(abs(residuals), ddof=1)
#             # print(sd)
#             higher_residuals = np.argsort(-abs(residuals)
#                                           )[:math.ceil(0.05*n_test)]
#             higher_residuals = [test[i] for i in higher_residuals]
#             new_test = [i for i in test if i not in higher_residuals]
#             yp = pls.predict(X[new_test])
#             Q2F195 = calcR2(y[new_test], yp, np.mean(y[train]))
#             Q2F295 = calcR2(y[new_test], yp)
#             MAE95 = calcMAE(y[new_test], yp)
#             residuals95 = np.reshape(abs(yp-y[new_test]), len(new_test))
#             sd95 = np.std(residuals95, ddof=1)
#             # print(Q2F195)
#             # print(Q2F295)
#             # print(MAE95)
#             # print(sd95)
#             # print(MAE95 + 3*sd95)
#             tr = max(y[train]) - min(y[train])
#             # print(tr)
#             # print(0.1*tr)
#             # print(0.15*tr)
#             # print(0.2*tr)
#             # print(0.25*tr)
#             NE = [i for i in residuals if i < 0]
#             PE = [i for i in residuals if i > 0]
#             nNE = len(NE)
#             nPE = len(PE)
#             mNE = abs(np.mean(NE))
#             mPE = np.mean(PE)
#             # print(nNE/nPE)
#             # print(nPE/nNE)
#             # print(mNE/mPE)
#             # print(mPE/mNE)
#             if (nNE == 0) or (nPE == 0) or (nNE/nPE > 5) or (nPE/nNE > 5):
#                 print("Warning")
#             if (MAE95 <= 0.1*tr) and (MAE95 + 3*sd95 <= 0.2*tr):
#                 print("good")
#                 # print(MAE95)
#                 # print(MAE95 + 3*sd95)
#                 # print(0.1*tr)
#                 # print(0.15*tr)
#                 # print(0.2*tr)
#                 # print(0.25*tr)
#                 # print(test)
#                 tests_sets.append(test)
#                 R2 = np.r_[R2, Q2F2]
#                 Q2 = np.r_[Q2, max(cv.Q2())]
#             else:
#                 if (MAE95 > 0.15*tr) or (MAE95 + 3*sd95 > 0.25*tr):
#                     print("bad")
#                 else:
#                     print("moderate")

#         ind = np.argsort(-R2)
#         self.R2 = R2[ind]
#         self.Q2 = Q2[ind]
#         self.tests_sets = [tests_sets[i] for i in ind]

#     def extVal(self, train, test, nLV=None):
#         Xtest = self.X[test]
#         Xtrain = self.X[train]
#         ytest = self.y[test]
#         ytrain = self.y[train]
#         nLV = self.nLV
#         if nLV == None:
#             cv = CrossValidation(Xtrain, ytrain)
#             nLV = np.argmax(cv.Q2())+1
#         pls = PLSRegression(n_components=nLV)
#         pls.fit(Xtrain, ytrain)
#         ypred = pls.predict(Xtest)
#         self.ypred = ypred
#         Q2F1 = calcR2(ytest, ypred, np.mean(ytrain))
#         Q2F2 = calcR2(ytest, ypred)
#         Q2F3 = 1-((ytest-ypred).T.dot(ytest-ypred)/len(ytest)) / \
#             ((ytrain-ytrain.mean()).T.dot(ytrain-ytrain.mean())/len(ytrain))
#         residuals = np.reshape(ypred-ytest, len(test))
#         higher_residuals = np.argsort(-abs(residuals)
#                                       )[:math.ceil(0.05*len(test))]
#         higher_residuals = [test[i] for i in higher_residuals]
#         new_test = [i for i in test if i not in higher_residuals]
#         yp = pls.predict(self.X[new_test])
#         Q2F195 = calcR2(self.y[new_test], yp, np.mean(ytrain))
#         Q2F295 = calcR2(self.y[new_test], yp)
#         Q2F395 = 1-((self.y[new_test]-yp).T.dot(self.y[new_test]-yp)/len(yp)) / \
#             ((ytrain-ytrain.mean()).T.dot(ytrain-ytrain.mean())/len(ytrain))
#         MAE95 = calcMAE(self.y[new_test], yp)
#         k = sum(ytest*ypred)/sum(ypred**2)
#         k1 = sum(ytest*ypred)/sum(ytest**2)
#         yr0 = k*ypred
#         y1r0 = k1*ytest
#         R02 = calcR2(ytest, yr0)
#         R102 = calcR2(ypred, y1r0)
#         dif = abs(R02-R102)
#         AREpred = sum(abs(ytest-ypred)/ytest)*100/len(ytest)
#         RMSEP = calcRMSE(ytest, ypred)
#         scaledy_test = (ytest-min(ytest))/(max(ytest)-min(ytest))
#         scaledyp = (ypred-min(ytest))/(max(ytest)-min(ytest))
#         scaled_k = sum(scaledy_test*scaledyp)/sum(scaledyp**2)
#         scaled_k1 = sum(scaledy_test*scaledyp)/sum(scaledy_test**2)
#         scaled_yr0 = scaled_k*scaledyp
#         scaled_y1r0 = scaled_k1*scaledy_test
#         scaled_R02 = calcR2(scaledy_test, scaled_yr0)
#         scaled_R102 = calcR2(scaledyp, scaled_y1r0)
#         r2 = (calcR(np.reshape(scaledy_test, len(scaledy_test)),
#                     np.reshape(scaledyp, len(scaledy_test))))**2
#         rm2 = r2*(1-math.sqrt(r2-scaled_R02))
#         rm12 = r2*(1-math.sqrt(r2-scaled_R102))
#         avgrm = (rm2+rm12)/2
#         deltarm = abs(rm2-rm12)
#         MAE = calcMAE(ytest, ypred)
#         test_set = str([i+1 for i in test])
#         # param = [Q2F1,Q2F2,k,k1,R02,R102,dif,AREpred,RMSEP,str(test)]
#         # dfPred = pd.DataFrame(index = ["Q2F1","Q2F2","k","k'","R0","R0'","dif","AREpred","RMSEP","test_set"],
#         #     data=np.array([Q2F1[0],Q2F2[0],k[0],k1[0],R02[0],R102[0],dif[0],AREpred[0],RMSEP,str(test)]))
#         # param = [Q2F1,Q2F2,k,k1,R02,R102,dif,AREpred,RMSEP,avgrm,deltarm,str(test)]
#         dfPred = pd.DataFrame(index=["Q2F1", "Q2F2", "Q2F3", "Q2F195", "Q2F295", "Q2F395",
#                                      "k", "k'", "R0",
#                                      "R0'", "dif", "AREpred", "RMSEP", "avgrm",
#                                      "deltarm", "MAE", "MAE95", "test_set", "nLV"],
#                               data=np.array([Q2F1[0], Q2F2[0], Q2F3[0][0], Q2F195[0], Q2F295[0], Q2F395[0][0],
#                                              k[0], k1[0], R02[0], R102[0], dif[0], AREpred[0], RMSEP, avgrm,
#                                              deltarm, MAE, MAE95, test_set, nLV]))
#         return dfPred

#     def saveExtVal(self, train, test, fileName):
#         dfPred = self.extVal(train, test, self.nLV)
#         dfPred.to_csv(fileName, sep=',', header=False)

#     def runValidExtVal(self, directory, n_models=1):
#         print("Entrou na funcao de testar validacoes")
#         print(len(self.tests_sets))
#         for i in range(min(n_models, len(self.tests_sets))):
#             test = self.tests_sets[i]
#             train = [j for j in range(len(self.y)) if j not in test]
#             dfPred = self.extVal(train, test)
#             dfPred.to_csv(directory+"test"+str(i+1) +
#                           ".csv", sep=',', header=False)

#     def searchValidExtVal2(self, directory, nLV=None, n_test=10, n_splits=100):
#         X = self.X
#         y = self.y
#         nLV = self.nLV
#         if nLV == None:
#             cv = CrossValidation(X, y)
#             nLV = np.argmax(cv.Q2())+1
#         N_SPLITS = n_splits
#         TEST_SIZE = n_test/len(y)
#         ss = ShuffleSplit(n_splits=N_SPLITS, test_size=TEST_SIZE)
#         pls = PLSRegression(n_components=nLV)
#         # yp = np.zeros((self.n_test,N_SPLITS))
#         # R2 = np.zeros(N_SPLITS)
#         # R2 = np.zeros(0)
#         # Q2 = np.zeros(0)
#         i = 0
#         # tests_sets = []
#         dfExt = pd.DataFrame()
#         dfCv = pd.DataFrame()
#         for train, test in ss.split(X):
#             if self.validateExtVal(train, test, nLV):
#                 # print("Achou um conjunto teste valido")
#                 # self.saveExtVal(train,test,os.path.join(directory,"test"+str(i+1)+".csv"))
#                 dfExt[i] = self.extVal(train, test, nLV).iloc[:, 0]
#                 cv = CrossValidation(
#                     X[train, :], y[train], nLVMax=nLV, scale=True)
#                 dfCv[i] = cv.returnParameters(nLV).iloc[:, 0]
#                 # cv.saveParameters(os.path.join(directory,"test_cv"+str(i+1)+".csv"))
#                 i = i + 1
#         return dfExt, dfCv


# # R2 = R2[ind]
# # yp = yp[:,ind]

# # ytosave = np.zeros((test_size,0))
# # R2tosave = np.zeros(0)
# # teststosave = []

# # i = 0
# # count = 0
# # while R2[i] > 0.5:
# #     residue = True
# #     for j in range(test_size):
# #         if abs(yp[j,i] - y[tests_sets[ind[i]][j]][0]) > 0.5:
# #             residue = False
# #     if residue:
# #         count += 1
# #         ytosave = np.c_[ytosave,yp[:,i]]
# #         R2tosave = np.r_[R2tosave,R2[i]]
# #         teststosave.append(tests_sets[ind[i]])
# #         dfPred = pd.DataFrame(data=np.c_[y[tests_sets[ind[i]]],yp[:,i]],columns=["Yreal","Ypred"])
# #         dfPred.to_csv("test"+str(count)+".csv", sep =',', index=False)
# #     i += 1


# # with open(out_directory+"/R2.json", "w") as f:
# #     f.write(json.dumps(R2tosave.tolist()))

# # with open(out_directory+"/yp.json", "w") as f:
# #     f.write(json.dumps(ytosave.tolist()))

# # with open(out_directory+"/tests.json", "w") as f:
# #     f.write(json.dumps(teststosave))

# # df = pd.DataFrame(ytosave)
# # df2 = pd.DataFrame(R2tosave)
# # df2 = df2.transpose()
# # str_tests = [str(teststosave[i]) for i in range(len(teststosave))]
# # df3 = pd.DataFrame(str_tests)
# # df3 = df3.transpose()
# # frames = [df,df2,df3]
# # result = pd.concat(frames)
# # print(result.shape)
# # # df.to_csv('yp.csv', sep =';')
# # # df2.to_csv('R2.csv', sep =';')
# # df3.to_csv('tests.csv', sep =';')
# # result.to_csv('result.csv', sep =';')
