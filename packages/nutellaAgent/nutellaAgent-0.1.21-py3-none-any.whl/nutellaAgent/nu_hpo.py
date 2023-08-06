from hyperopt.base import STATUS_STRINGS
from hyperopt.base import STATUS_NEW
from hyperopt.base import STATUS_RUNNING
from hyperopt.base import STATUS_SUSPENDED
from hyperopt.base import STATUS_OK
from hyperopt.base import STATUS_FAIL

from hyperopt.base import JOB_STATES
from hyperopt.base import JOB_STATE_NEW
from hyperopt.base import JOB_STATE_RUNNING
from hyperopt.base import JOB_STATE_DONE
from hyperopt.base import JOB_STATE_ERROR

from hyperopt.base import Ctrl
from hyperopt.base import Trials
from hyperopt.base import trials_from_docs
from hyperopt.base import Domain

# -- syntactic sugar
from hyperopt import hp

# -- exceptions
from hyperopt import exceptions

# -- Import built-in optimization algorithms
from hyperopt import rand
from hyperopt import tpe
from hyperopt import atpe
from hyperopt import mix
from hyperopt import anneal

# -- spark extension
from hyperopt.spark import SparkTrials

from hyperopt.fmin import fmin #as nu_fmin
from hyperopt.fmin import fmin_pass_expr_memo_ctrl
from hyperopt.fmin import FMinIter
from hyperopt.fmin import partial
from hyperopt.fmin import space_eval

from .nu_importance import calculate_importance
import numpy as np
import json
import asyncio
from .nu_requests import Requests

hpo_url = "http://localhost:7000/admin/sdk/hpo"

def nu_fmin(hpo_project_key, objective, space, algo, max_evals, trials, rseed=1337, full_model_string=None, notebook_name=None, verbose=True, stack=3, keep_temp=False, data_args=None):
        
    best = fmin(objective, space, algo=algo, max_evals=max_evals, trials=trials, rstate=np.random.RandomState(rseed), return_argmin=True)
    importances = calculate_importance(trials)

    all_info = dict()
    
    all_info["best_result"] = trials.best_trial['result'] 
    all_info["best_hp"] = best
    all_info["trial_result"] = trials.results
    all_info["trial_hp"] = trials.vals
    # json int64 때문에 작업
    all_info = __to_int(all_info)
    
    all_info["hpo_project_key"] = hpo_project_key

    method, config = __transform_function_to_db(algo, space)
    all_info["method"] = method
    all_info["config"] = config

    tmp_importance = list()
    for i in range(len(importances)):
        for key1, value1 in importances[i].items():
            for key2, value2 in value1.items(): 
                tmp_importance.append(value2)
                break
    all_info["importances"] = tmp_importance

    asyncio.run(Requests().post_action(request_datas = all_info, url = hpo_url))

    return best

# 웹에서 설정한 space, algo로 돌리고 max_evals도 추천으로 돌리기. 오직 objective 만 넘기면 됨
def nu_simple_fmin(hpo_project_key, objective, rseed=1337, full_model_string=None, notebook_name=None, verbose=True, stack=3, keep_temp=False, data_args=None):
    
    # db에서 가져오기
    db_info = asyncio.run(Requests().get_action(parameter1 = hpo_project_key, parameter2 = "null", url = hpo_url))[0]
    hpo_project_id = db_info["hpoProjectId"]
    algo, space = __transform_db_to_function(method = db_info["method"], config = db_info["config"])

    trials = Trials()
    best = fmin(objective, space, algo=algo, max_evals=50, trials=trials, rstate=np.random.RandomState(rseed), return_argmin=True)
    importances = calculate_importance(trials)
 
    # 저장 api
    all_info = dict()
    
    all_info["best_result"] = trials.best_trial['result'] 
    all_info["best_hp"] = best
    all_info["trial_result"] = trials.results
    all_info["trial_hp"] = trials.vals
    # json int64 때문에 작업
    all_info = __to_int(all_info)

    all_info["hpo_project_key"] = hpo_project_key

    tmp_importance = list()
    for i in range(len(importances)):
        for key1, value1 in importances[i].items():
            for key2, value2 in value1.items(): 
                tmp_importance.append(value2)
                break
    all_info["importances"] = tmp_importance

    asyncio.run(Requests().post_action(request_datas = all_info, url = hpo_url))

    return best, trials

# db에서 꺼낸 method랑 config를 nu_fmin에 넣을 수 있는 형식으로 변환하는 함수
def __transform_db_to_function(method, config):
    # 알고리즘 변환
    algo = 2
    if method == 0:
        algo = "random"
    if method == 1:
        algo = "grid"
    if method == 2:
        algo = tpe.suggest

    # search space 변환
    space = dict()

    for key, value in json.loads(config).items():
        for key_in, value_in in value.items():    
            if str(key_in) == "scope":
                space[key] = hp.uniform(key, value_in[0], value_in[1])
            else:
                space[key] = hp.choice(key, value_in)

    return algo, space

# 사용자에게 함수 인자로 받은 algo랑 space를 db에 넣을 형식으로 변환하는 함수
def __transform_function_to_db(algo, space):
    method = 2
    if algo == "random":
        method = 0
    if algo == "grid":
        method = 1
    if algo == "tpe.sugget":
        method = 2

    config = dict()
    for key, value in space.items():
        if str(type(value)) != "<class 'hyperopt.pyll.base.Apply'>":
            continue
        
        tmp_arr = str(value).split('Literal{')
        real_list = list()

        for i in range(len(tmp_arr)-2):
            real_val = tmp_arr[i+2].split('}')[0]
            if key != 'optimizer':
                real_val = float(real_val)
            real_list.append(real_val)

        if value.name == "float":
            config[key] = {"scope": real_list}

        if value.name == "switch":
            config[key] = {"value": real_list[1:]}

    return method, config

# json 변환을 위해 int64를 int로 변환작업
def __to_int(all_info):
    for key1, value1 in all_info.items():
        if str(type(value1)) == "<class 'dict'>":
            for key2, value2 in value1.items():
                if str(type(value2)) == "<class 'list'>":
                    if isinstance(value2[0], np.int64):
                        tmparr = list()
                        for j in range(len(value2)):
                            tmparr.append(int(value2[j]))
                        all_info[key1][key2] = tmparr
                else:
                    if isinstance(value2, np.int64):
                        all_info[key1][key2] = int(value2)
                    # print(value2)
        else:
            for i in range(len(value1)):
                for key2, value2 in value1[i].items():
                    if isinstance(value2, np.int64):
                        all_info[key1][i][key2] = int(value2)
    return all_info
