import sys
import numpy as np
import pandas as pd
import json
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.yrandomization import YRandomization
from qsarmodelingpy.lno import LNO
import qsarmodelingpy.lj_cut as lj
from qsarmodelingpy.filter import variance_cut, correlation_cut


def validate(X: np.ndarray, y: np.ndarray, pop: list, Q2: list, Q2_cut=0.5, yr_cut=0.3, lno_cut=0.1) -> list:
    # y-randomization
    lpass = []
    intercepts = []
    for i, var_sel in enumerate(pop):
        if Q2[i] > Q2_cut:
            XSel = X[:, var_sel]
            cv = CrossValidation(XSel, y)
            nLV = np.argmax(cv.Q2()) + 1
            yr = YRandomization(XSel, y, nLV, 50)
            intercepts.append(yr.returnIntercept())
            if yr.returnIntercept() < yr_cut:
                lpass.append(i)
    # leave-N-out
    lpass2 = []
    if lpass != []:
        for i in lpass:
            if Q2[i] > Q2_cut:
                XSel = X[:, pop[i]]
                m, _ = np.shape(X)
                cv = CrossValidation(XSel, y)
                nLV = np.argmax(cv.Q2()) + 1
                lno = LNO(XSel, y, nLV, int(m / 4), 5)
                m = np.mean(lno.Q2, 1)
                std = max([abs(m[j] - m[0]) for j in range(len(m))])
                if std < lno_cut:
                    lpass2.append(i)
        if lpass2 != []:
            i = np.argmax([Q2[i] for i in lpass2])
            var_sel = pop[lpass2[i]]
            return var_sel
        else:
            return []
    else:
        return []


if __name__ == '__main__':
    directory = sys.argv[1]
    df = pd.read_csv(sys.argv[2], sep=';', index_col=0)
    dfX = lj.transform(df)
    y = pd.read_csv(sys.argv[3], sep=';', header=None).values
    indVar = variance_cut(dfX.values, 0.1)
    dfVar = dfX.loc[:, dfX.columns[indVar]]
    print(dfVar.shape)
    indCorr = correlation_cut(dfVar.values, y, 0.3)
    dfCorr = dfVar.loc[:, dfVar.columns[indCorr]]
    print(dfCorr.shape)
    out_directory = sys.argv[4]
    X = dfCorr.values
    with open(directory + "/Popout.json") as pop_file:
        pop = json.load(pop_file)
    with open(directory + "/Q2out.json") as Q2_file:
        Q2 = json.load(Q2_file)
    var_sel = validate(X, y, pop, Q2, yr_cut=0.25, lno_cut=0.1)
    if var_sel != []:
        dfSel = dfCorr.loc[:, dfCorr.columns[var_sel]]
        dfSel.to_csv(out_directory + "/XSel.csv", sep=';')
        cv = CrossValidation(dfSel.values, y)
        cv.saveParameters(out_directory + "/parameters_cv.csv")
    else:
        print("y-randomization or LNO failed!")
