# Contributing to this repo

Work In Progress: I'll be progressively adding information that can help make changes and contribute to this repo. Starting here with the Python environment set-up.

## Modify conda environment

The `full-stack-ml` environment configuration was uploaded to Anaconda cloud via `anaconda upload environment.yml` and can be found at [`louisdorard/full-stack-ml`](https://anaconda.org/louisdorard/full-stack-ml). The environment can then be created anywhere via the following command (no need to have the `environment.yml` file, but just an internet connection; replace `create` with `update` if you've already created this environment and just need to update it):

```bash
conda env create louisdorard/full-stack-ml
```

For development purposes, you can make changes to the environment config ([`environment.yml`](environment.yml)) and then make sure that the environment can be created or updated. For this, execute the following command from this repo's directory:

```bash
conda env update -f environment.yml
```