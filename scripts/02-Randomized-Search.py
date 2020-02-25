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
# # Hyper-parameter tuning with Randomized Search
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
SCORING = "neg_log_loss" # negative log likelihood
NTREES = 10 # reasonable values between 10 and 100; this has an impact on the time an evaluation takes
ESTIMATOR = "rf" # "rf" or "xgb"
HP_DIST = { # this is for rf; adapt for xgb
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
# ## Hyper-parameter distributions
#
# Create distributions based on values stored in `HP_DIST`.

# +
from scipy.stats import randint
from scipy.stats import uniform

hp = {}
for v in HP_DIST.keys():
    if HP_DIST[v]['type']=="int":
        hp[v] = randint(HP_DIST[v]['min'], HP_DIST[v]['max'])
    elif HP_DIST[v]['type']=="float":
        hp[v] = uniform(loc=HP_DIST[v]['min'], scale=(HP_DIST[v]['max']-HP_DIST[v]['min']))
    elif HP_DIST[v]['type']=="choice":
        hp[v] = HP_DIST[v]["values"]

# + [markdown] slideshow={"slide_type": "slide"}
# ## Search
#
# Define the base model, hyper-parameter distributions, number and type of evaluations to be performed for the search

# +
from sklearn.model_selection import RandomizedSearchCV

random_search = RandomizedSearchCV(
    default_model,
    param_distributions=hp,
    n_iter=EVALS,
    scoring=SCORING,
    cv=FOLDS,
    iid=False,
    error_score='raise',
    random_state=SEED,
    n_jobs=-1,
    verbose=1
)

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
# ## Fit
#
# Run (and time) the search
# -

# %time random_search.fit(X, y)

# + [markdown] slideshow={"slide_type": "subslide"}
# Save results

# + slideshow={"slide_type": "-"}
from joblib import dump
dump(random_search, "output/random_search_" + DATASET + ".joblib")

# + [markdown] slideshow={"slide_type": "slide"}
# Review results

# + slideshow={"slide_type": "-"}
from mlxtend.evaluate.hyper_search import hyper_search_report
hyper_search_report(random_search, n_top=3)
