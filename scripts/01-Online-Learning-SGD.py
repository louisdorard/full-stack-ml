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
# # Online Learning with SGD
# -

# Define run parameter (can be accessed by papermill)

# + tags=["parameters"]
FULL_RUN = False

# + [markdown] slideshow={"slide_type": "slide"}
# ## Load data
#
# Kaggle [Avazu CTR Prediction challenge](https://www.kaggle.com/c/avazu-ctr-prediction)
#
# Look at size of training set and number of lines. For this, use the following commands:
#
# ```bash
# du -h train.csv
# wc -l train.csv
# ```

# + [markdown] slideshow={"slide_type": "slide"}
# We'll go through this data by "chunks". Let's set the size of a chunk (can be accessed by papermill):

# + tags=["parameters"]
CHUNK_SIZE = 1000 # small value for fast execution; can bump to 10000
# -

# Let's create a chunk "reader":

from mlxtend.utils.data import filename2path
from pandas import read_csv
TRAIN_FILE = filename2path("avazu")
HEADER = ['id','click','hour','C1','banner_pos','site_id','site_domain','site_category','app_id','app_domain','app_category','device_id'\
        ,'device_ip','device_model','device_type','device_conn_type','C14','C15','C16','C17','C18','C19','C20','C21']
reader = read_csv(TRAIN_FILE, chunksize=CHUNK_SIZE, names=HEADER, header=0)

reader

# + [markdown] slideshow={"slide_type": "slide"}
# There are about 4,000 chunks of size 10,000 in this data.
#
# Let's look at the first chunk:
# -

chunk = reader.get_chunk()
print("Chunk weighs " + str(chunk.memory_usage(index=True).sum()/(1024**2)) + " MB")

chunk

import qgrid
qgrid_widget = qgrid.show_grid(chunk, show_toolbar=True)
qgrid_widget

# + [markdown] slideshow={"slide_type": "slide"}
# ## Prepare data
#
# Let's create a function that
#
# * Extracts inputs `X` and outputs `y` from a chunk dataframe
# * Applies feature hashing to the inputs (here, using $2^{20}$ features)

# +
from numpy import asarray
from sklearn.feature_extraction import FeatureHasher
fh = FeatureHasher(n_features=2**20, input_type='string')

def chunk2Xy(chunk):
    y = chunk['click'].values
    X = chunk.drop(['id', 'click'], axis=1) # remove id and target columns
    X = fh.transform(asarray(X.astype(str))) # transform X to array of strings, so we can apply feature hashing
    return X, y


# + [markdown] slideshow={"slide_type": "subslide"}
# Test this function:
# -

chunk2Xy(reader.get_chunk())

# + [markdown] slideshow={"slide_type": "slide"}
# ## Set model hyper-parameters
#
# We'll use the first INIT_SIZE lines of the dataset as training data to tune hyper-parameters:
#
# * SGD parameters: learning rate and number of epochs
# * model parameters: regularization
# * featurization parameters: number of features

# + [markdown] slideshow={"slide_type": "slide"}
# Re-set `reader` so we start reading from the beginning of the dataset:
# -

reader = read_csv(TRAIN_FILE, chunksize=CHUNK_SIZE, names=HEADER, header=0)

# Choose INIT_SIZE so that training data fits in memory and search isn't too long (can be accessed by papermill):

# + tags=["parameters"]
INIT_SIZE = 100000 # small value for fast execution; can bump to 1000000
# -

chunk_init = reader.get_chunk(INIT_SIZE)

print("Chunk weighs " + str(chunk_init.memory_usage(index=True).sum()/(1024**2)) + " MB")

# + [markdown] slideshow={"slide_type": "slide"}
# Hyper-parameter tuning...

# +
# look at output distribution
# split X, y into train and val sets
# fit on train
# compute accuracy on val set
# -

1-sum(chunk_init['click'].values)/len(chunk_init['click'].values)

from sklearn.model_selection import train_test_split
X, y = chunk2Xy(chunk_init)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import SGDClassifier
model = SGDClassifier(loss='log', random_state=42, max_iter=100)
classes = [0, 1]
model.fit(X_train, y_train)

from sklearn import metrics
y_pred_val = model.predict(X_val)
y_pred_proba_val = model.predict_proba(X_val)
print("Accuracy: " + str(metrics.accuracy_score(y_val, y_pred_val)))
print("F-measure: " + str(metrics.f1_score(y_val, y_pred_val)))
print("log-loss: " + str(metrics.log_loss(y_val, y_pred_proba_val)))

# + [markdown] slideshow={"slide_type": "slide"}
# ## Fit model chunk-by-chunk
#
# Let's iterate over the chunk reader, update our model with every new chunk, and display logloss every K chunks.

# + [markdown] slideshow={"slide_type": "fragment"}
# Let's set K to 100 and initialize a variable to store loss values every K chunks
# -

K = 100
chunk_indices_processed = []
losses_Kchunks = []
# print("The number of loss values will grow in size from 0 to " + N/(CHUNK_SIZE*K))
print("Each loss value will be computed over " + str(CHUNK_SIZE*K) + " data points")

# Initialize variables to store outputs and predictions for these data points:

y_Kchunks = []
y_pred_Kchunks = []
y_pred_no_update_Kchunks = []

# + [markdown] slideshow={"slide_type": "fragment"}
# Define a function that plots the loss:

# +
from IPython.display import clear_output
from pandas import DataFrame
import matplotlib.pyplot as plt

def display_loss():
    clear_output()
    DataFrame({'linear_regression': losses_Kchunks}).plot()
    plt.xlabel('Number of times (K chunks) were processed (K=' + str(K) + ')')
    plt.ylabel('Log-loss')
    plt.show()


# + [markdown] slideshow={"slide_type": "slide"}
# Iterate on `reader`, apply model to new chunk so we can update `y_pred_Kchunks`, and then update it using the new chunk.

# +
from sklearn.metrics import log_loss

for c, chunk in enumerate(reader): # c is a chunks counter

    X, y = chunk2Xy(chunk)
    
    # Compute loss over the last K chunks
    # Step 1. Update lists of outputs and predictions at every chunk
    y_Kchunks.extend(y)
    y_pred_Kchunks.extend(model.predict_proba(X))
    # Step 2. Every K chunks...
    if (c % K == 0):
        # Display loss over the last K chunks
        chunk_indices_processed.append(c)
        losses_Kchunks.append(log_loss(y_Kchunks, y_pred_Kchunks))
        # losses_Kchunks_no_update.append(log_loss(y_Kchunks, y_pred_no_update_Kchunks))
        display_loss()
        
        # Reset lists of outputs and predictions used to compute loss
        y_Kchunks = []
        y_pred_Kchunks = []
        # y_pred_no_update_Kchunks = []

    model.partial_fit(X, y, classes=classes) # this runs only 1 epoch; try more?

    # if not doing a full run, stop loop after 2*K chunks
    if (not FULL_RUN and c==2*K):
        break
