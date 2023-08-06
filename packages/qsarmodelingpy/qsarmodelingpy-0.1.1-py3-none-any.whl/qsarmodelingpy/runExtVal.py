# Importing libraries
import numpy as np
import pandas as pd
from qsarmodelingpy.external_validation import ExternalValidation
from qsarmodelingpy.cross_validation_class import CrossValidation
from qsarmodelingpy.kennardstonealgorithm import kennardstonealgorithm
import qsarmodelingpy.lj_cut as lj
import os
import argparse
import logging


def run(config) -> None:
    """Run External Validation with configuration given by `config`.

    `config` is (usually) a CSV containing all needed information for this function. Please, [see this template](https://github.com/hellmrf/QSARModelingPyCore/blob/master/examples/confExtVal.csv) and edit for your needs.
    Probably, in future, `config` will also accept a Dictionary that follows rules defined in `qsarmodelingpy.Interfaces`.

    Args:
        config (str, path, file-like, `io`): The configuration file (usually a CSV). [See this template](https://github.com/hellmrf/QSARModelingPyCore/blob/master/examples/confExtVal.csv).
    """
    # Open configuration file in order to look for the matrices and the parameters to run
    # external validation
    dfConf = pd.read_csv(config, header=None)
    directory = dfConf[1][0]
    Xfile = dfConf[1][1]
    yfile = dfConf[1][2]
    nLV = None if dfConf.isnull()[1][4] else int(dfConf[1][4])
    out_directory = dfConf[1][5]
    ext_val_file = dfConf[1][6]
    cv_file = dfConf[1][7]
    Xtrain_file = dfConf[1][8]
    ytrain_file = dfConf[1][9]
    Xtest_file = dfConf[1][10]
    ytest_file = dfConf[1][11]
    autoscale = dfConf[1][12].upper() == "YES"
    y = pd.read_csv(os.path.join(directory, yfile),
                    sep=';', header=None).values
    dfX = pd.read_csv(os.path.join(directory, Xfile), sep=';', index_col=0)
    dfX = lj.transform(dfX) if dfConf[1][13].upper() == "YES" else dfX
    X = dfX.values
    type_ext_val = int(dfConf[1][14])
    if type_ext_val == 1:  # manual selection
        test_set = dfConf[1][3]
        test = [int(i) - 1 for i in test_set.split(',')]
        train = [j for j in range(len(y)) if j not in test]
    elif type_ext_val == 2:  # Kennard-Stone
        size_test_set = int(dfConf[1][3])
        # parameter is the size of training set
        train, test = kennardstonealgorithm(dfX, len(dfX) - size_test_set)
    else:  # Random selection
        pass
    ext = ExternalValidation(X, y, nLV)
    ext.extVal(train, test, nLV)
    if ext.validateExtVal(train, test):
        logging.info("Passed")
    else:
        logging.info("Failed")
    ext.saveExtVal(train, test, out_directory + "/" + ext_val_file)
    cv = CrossValidation(X[train, :], y[train], nLVMax=nLV, scale=True)
    cv.saveParameters(os.path.join(out_directory, cv_file))
    dfXtrain = dfX.loc[dfX.index[train], dfX.columns]
    dfXtrain.to_csv(os.path.join(out_directory, Xtrain_file), sep=';')
    dfytrain = pd.DataFrame(y[train])
    dfytrain.to_csv(os.path.join(out_directory, ytrain_file),
                    sep=',', header=False)
    dfXtest = dfX.loc[dfX.index[test], dfX.columns]
    dfXtest.to_csv(os.path.join(out_directory, Xtest_file), sep=';')
    dfytest = pd.DataFrame(y[test])
    dfytest.to_csv(os.path.join(out_directory, ytest_file),
                   sep=',', header=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--filename', '-f', required=True,
                        metavar='<filename>',
                        help='Config External Validation file.')
    args = parser.parse_args()
    filename = args.filename
    run(filename)
