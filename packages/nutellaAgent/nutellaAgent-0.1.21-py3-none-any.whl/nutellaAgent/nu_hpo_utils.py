from hyperopt import hp, fmin, tpe, space_eval

def hpchoice(label, p_options):
    return hp.pchoice(label, p_options)


def choice(label, options):
    return hp.choice(label, options)

def randint(label, *args, **kwargs):
    return hp.randint(label, *args, **kwargs)


def uniform(label, *args, **kwargs):
    return hp.uniform(label, *args, **kwargs)


def uniformint(label, *args, **kwargs):
    return hp.uniformint(label, *args, **kwargs)


def quniform(label, *args, **kwargs):
    return hp.quniform(label, *args, **kwargs)


def loguniform(label, *args, **kwargs):
    return hp.loguniform(label, *args, **kwargs)


def qloguniform(label, *args, **kwargs):
    return hp.qloguniform(label, *args, **kwargs)


def normal(label, *args, **kwargs):
    return hp.normal(label, *args, **kwargs)


def qnormal(label, *args, **kwargs):
    return hp.qnormal(label, *args, **kwargs)


def lognormal(label, *args, **kwargs):
    return hp.lognormal(label, *args, **kwargs)


def qlognormal(label, *args, **kwargs):
    return hp.qlognormal(label, *args, **kwargs)


def hpo(objective, space, algo = tpe.suggest, max_evals = 100):
    best = fmin(objective, space, algo = tpe.suggest, max_evals = 100)
    return best


