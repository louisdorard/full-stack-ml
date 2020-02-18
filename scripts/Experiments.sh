# ---
# jupyter:
#   jupytext:
#     formats: ipynb,scripts//sh
#     text_representation:
#       extension: .sh
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.3
#   kernelspec:
#     display_name: Bash
#     language: bash
#     name: bash
# ---

# # Experiments
#
# This Bash notebook can be used to run notebook-based experiments, locally or on cloud infrastructure: notebooks are run as scripts by papermill.

export NOTEBOOK_NAME="00-Version-Information"

export CMD_LOCAL="papermill $NOTEBOOK_NAME.ipynb output/$NOTEBOOK_NAME.ipynb"
export CMD_CLOUD_LOCAL="papermill $NOTEBOOK_NAME.ipynb /artifacts/$NOTEBOOK_NAME.ipynb"

# ## Run with local Python environment

bash -c "$CMD_LOCAL"

# ## Run experiment on Cloud
#
# Using Gradient Jobs with the following options:
#
# * `--name` gives the name of the job/experiment
# * `--machineType`: see Gradient's [instance types](https://docs.paperspace.com/gradient/instances/instance-types)
# * `--jobEnv` allows to specify [environment variables](https://docs.paperspace.com/gradient/experiments/using-experiments/environment-variables); here we define `DATA_PATH`, which will be used by our data loading utils ([mlxtend.utils.data](https://github.com/louisdorard/mlxtend/tree/master/mlxtend/utils/data.py)) to find data files
# * `--workspace`: setting it to the current directory (`./`) will upload the contents of this directory to the instance used for this job/experiment, at `/paperspace/`; an alternative is to use [`--workspaceRef`](https://docs.paperspace.com/gradient/experiments/using-experiments/git-commit-tracking#example)
# * `--command`: this is executed from `/paperspace/`

gradient jobs create \
   --name version-information \
   --machineType C3 \
   --container louisdorard/full-stack-ml \
   --command "bash -c '$CMD_CLOUD_LOCAL'" \
   --workspace ./ \
   --jobEnv "{\"DATA_PATH\":\"/storage/data/\"}" \
   --projectId $GRADIENT_PROJECT_ID

# Download output notebook from job's artifacts, and move to `output/`:

gradient jobs artifacts download \
--jobId XXX \
--destinationDir output/

# Note: it's also possible to use `experiments run` instead of `jobs create`.

# [Gradient documentation](https://docs.paperspace.com/gradient/)

# ## Work in Process: turn this into bash script
#
# `NOTEBOOK_NAME` and `EXEC_MODE` would be arguments of this script

case $EXEC_MODE in
    docker) CMD=$CMD_DOCKER
    cloud) CMD=...
    *) CMD=$CMD_LOCAL
esac
