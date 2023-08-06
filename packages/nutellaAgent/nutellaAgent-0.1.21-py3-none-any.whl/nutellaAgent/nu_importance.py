from fanova import fANOVA
import ConfigSpace
from ConfigSpace.hyperparameters import UniformFloatHyperparameter
import numpy as np
import pandas as pd

def __make_datas(trials):
    # x 생성
    hps = trials.vals
    hps_list = list(hps.keys())

    features = []
    for i in range(len(hps[hps_list[0]])):
        tmp =[]
        for j in range(len(hps_list)):
            tmp.append(hps[hps_list[j]][i])
        features.append(tmp)

    columns_list = []
    for i in range(len(hps)):
        columns_list.append(str(i))
    df_x = pd.DataFrame(features, columns=columns_list)

    # y 생성
    res = trials.results
    responses = []
    for i in range(len(res)):
        responses.append(res[i]['loss'])
    responses = np.array(responses)

    # cs 생성
    pcs = list(zip(np.min(df_x, axis=0), np.max(df_x, axis=0)))
    cs = ConfigSpace.ConfigurationSpace()
    for i in range(len(pcs)):
        cs.add_hyperparameter(UniformFloatHyperparameter("%i" %i, pcs[i][0], pcs[i][1]))    

    return df_x, responses, cs

def calculate_importance(trials):
    df_x, responses, cs = __make_datas(trials)

    f = fANOVA(X = df_x, Y = responses, config_space=cs)

    num_of_features = len(df_x.columns)

    # marginal of particular parameter:
    importances = []
    for i in range(num_of_features):
        dims = (i, )
        res = f.quantify_importance(dims)
        importances.append(res)

    # # getting the 10 most important pairwise marginals sorted by importance
    # best_margs = f.get_most_important_pairwise_marginals(n=1)
    # print(best_margs)

    return importances



