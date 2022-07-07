import redis
import vdx
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def create_algorithm(name, algorithm="no_history", collation="average", error=0.05, scaling=2, bootstrapping=False):
    data = {
        "name": name,
        "algorithm": algorithm,
        "collation": collation,
        "error": error,
        "scaling": scaling,
        "bootstrapping": bootstrapping
    }
    data = json.dumps(data)
    r.set('algo:' + name, data)
    return r.get('algo:' + name)

def create_candidate(name):
    data = {
        "name": name,
        "history": [0,0],
        "weight": 1
    }
    data = json.dumps(data)
    r.set('candidate:' + name, data)
    return r.get('candidate:' + name)

def vote_num(algorithm, cands, values):
    algo = r.get('algo:' + algorithm)
    algo = json.loads(algo)
    input = []
    for value in values:
        input.append(float(value))
    histories = []
    weights = []
    modules = []
    #print(cands)
    for id in cands:
        module = r.get('candidate:' + id)
        module = json.loads(module)
        modules.append(module)
        try:
            histories.append(module['history'])
            weights.append(module['weight'])
        except:
            histories.append([0,0])
            weights.append(1)
    alg = algo['algorithm']
    collation = algo['collation']
    error = algo['error']
    scaling = algo['scaling']
    bootstrapping = algo['bootstrapping']
    average, history, weights = vdx.vote_numeric(input, histories, weights, alg, collation, float(error), float(scaling), bootstrapping)
    for i in range(len(modules)):
        modules[i]['history'] = history[i]
        modules[i]['weight'] = weights[i]
        #print(modules[i])
        module_temp = json.dumps(modules[i])
        r.set('candidate:' + modules[i]['name'], module_temp)
    return average, history, weights

def vote_alpha(algorithm, candidates, values):
    algo = r.get('algo:' + algorithm)
    algo = json.loads(algo)
    input = values
    histories = []
    for id in candidates:
        module = r.get('candidate:' + id)
        module = json.loads(module)
        histories.append(module['history'])
    alg = algo['algorithm']
    average, history = vdx.vote_alpha(input, histories, alg)
    for i in range(len(candidates)):
        candidates[i]['history'] = history[i]
        module_temp = json.dumps(candidates[i])
        r.set('candidate:' + candidates[i]['name'], module_temp)
    return average, history

