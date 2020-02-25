# ---
# jupyter:
#   jupytext:
#     formats: ipynb,scripts//py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: full-stack-ml
#     language: python
#     name: full-stack-ml
# ---

# + [markdown] slideshow={"slide_type": "slide"}
# # Hyper-parameter tuning with Smart Search
#
# All hyper-parameters that influence the learning are searched simultaneously (except for the number of estimators, which poses a time / quality tradeoff).

# + [markdown] slideshow={"slide_type": "slide"}
# ## Notebook variables
#
# (Can be accessed by papermill)

# + tags=["parameters"]
EVALS = 4 # the number of evaluations roughly determines how long search procedures will take; this value is just for tests, it should be increased for meaningful results!
DATASET = "digits" # "digits" (rather small, good to start running experiments) or "credit" (bigger)
FOLDS = 3 # smaller values will make the evaluation quicker; recommended values are between 3 and 10
NTREES = 10 # reasonable values between 10 and 100; this has an impact on the time an evaluation takes
ESTIMATOR = "rf" # "rf" or "xgb"
HP_DIST = { # this is for rf
    "max_depth": {
        "type": "int",
        "min": 2,
        "max": 11
    },
    "max_features": {
        "type": "float",
        "min": 0.1,
        "max": 1.0
    },
    "bootstrap": {
        "type": "choice",
        "values": [True, False]
    }
}
SCORING = "neg_log_loss" # negative log likelihood
SEED = 42 # for reproducibility of results

# + [markdown] slideshow={"slide_type": "slide"}
# ## Default model
#
# Initialize an empty model with specified number of trees (`NTREES`) and random state (`SEED`), and with default hyper-parameter values.

# +
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

if (ESTIMATOR=="rf"):
    default_params = {"n_estimators": NTREES, "random_state": SEED}
    default_model = RandomForestClassifier(**default_params)
elif (ESTIMATOR=="xgb"):
    default_params = {"n_estimators": NTREES, "seed": SEED}
    default_model = XGBClassifier(**default_params)
    if (DATASET=="credit"):
        default_params.update({"objective": "multi:softprob"})

# + [markdown] slideshow={"slide_type": "slide"}
# ## Data
#
# Import data and prepare X and y (inputs and outputs)
# -

if (DATASET=="digits"):
    from sklearn.datasets import load_digits
    digits = load_digits()
    X, y = digits.data, digits.target
elif (DATASET=="credit"):
    from mlxtend.data.kaggle_gmsc import kaggle_gmsc_data_nomissing
    X, y = kaggle_gmsc_data_nomissing()

# + [markdown] slideshow={"slide_type": "slide"}
# ## Hyper-parameter distributions
#
# Create hyperopt-compatible distributions based on values stored in `HP_DIST`.
# -

from hyperopt import hp     
hp_space = {}
for v in HP_DIST.keys():
    if HP_DIST[v]['type']=="int":
        hp_space[v] = hp.quniform(v, HP_DIST[v]['min'], HP_DIST[v]['max'], 1)
    elif HP_DIST[v]['type']=="float":
        hp_space[v] = hp.uniform(v, HP_DIST[v]['min'], HP_DIST[v]['max'])
    elif HP_DIST[v]['type']=="choice":
        hp_space[v] = hp.choice(v, HP_DIST[v]["values"])

# Hyperopt uses float, but when parameters are actually int, scikit needs them to be int! In the following, we use a function that "converts" hyper-parameters in use by hyperopt to ones that can be used in scikit.

# + [markdown] slideshow={"slide_type": "slide"}
# ## Define loss to minimize
#
# Hyperopt aims at minimizing the loss incurred by using a certain set of hyperparameter values. We define the loss function to use, which implements the evaluation of these hyperparameter values and requires access to the data (`X` and `y`).

# +
from hyperopt import STATUS_OK
from sklearn.model_selection import cross_val_score
from mlxtend.evaluate.hyper_search import hyperopt2sklearn

def hp_loss(h_params):
    s_params = hyperopt2sklearn(h_params, HP_DIST, default_params)
    if (ESTIMATOR=="xgb"):
        model = XGBClassifier(**s_params)
    elif (ESTIMATOR=="rf"):
        model = RandomForestClassifier(**s_params)
    s = cross_val_score(model, X, y, scoring=SCORING, cv=FOLDS, n_jobs=-1, verbose=1)
    return {'loss': -s.mean(), 'status': STATUS_OK}


# + [markdown] slideshow={"slide_type": "slide"}
# ## Run minimization
#
# With hyperopt, we pass the hyper-parameter distributions to use, along with the loss function to minimize.
#
# Note the differences in design compared to scikit's RandomizedSearch (where we just pass the data via a `fit` function).

# +
from hyperopt import fmin, tpe, Trials
from numpy.random import RandomState

trials = Trials() # this is where the history will be saved
# %time best = fmin(hp_loss, hp_space, algo=tpe.suggest, trials=trials, max_evals=EVALS) # TODO: specify seed
# -

hyperopt2sklearn(best, HP_DIST, default_params)

# (Note on using `neg_log_loss` as our performance metric: we expect to see loss values which are > 0 since we're dealing with negative log likelihood (likelihood is between 0 and 1 and log makes those values negative); the smaller the loss, the higher the likelihood, the better!)

# + [markdown] slideshow={"slide_type": "subslide"}
# Save results

# + slideshow={"slide_type": "-"}
from joblib import dump
dump(trials, "output/smart_search_" + DATASET + ".joblib")

# + [markdown] slideshow={"slide_type": "slide"}
# Review results

# + slideshow={"slide_type": "-"}
trials.losses()
# -

trials.best_trial

trials.best_trial['misc']['vals']
