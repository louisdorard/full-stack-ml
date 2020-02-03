# Full-Stack Machine Learning Workshops

## Set-up

### Accounts

You'll need the following:

* [Kaggle](https://www.kaggle.com)
* TODO: Gradient or Floyd?

### Environment variables

#### Authentication

Add authentication variables to `auth.env`. As a starting point, you can just copy the `auth.env.sample` file which contains example key/value pairs. You'll need to change the values!

For Kaggle:

* Your username can be found in the top right corner of the Kaggle web interface, once you're logged in. Let's call it `USERNAME` (please replace in the URL below)
* Go to the _API_ section on https://www.kaggle.com/`USERNAME`/account and click on _Create New API Token_

#### `DATA_PATH`

Let's say that your data files are in directory `X`...

* Add `export DATA_PATH=X` in your bashrc file
* Make sure that the `volumes` property of `docker-compose.yml` has an item which is `X:/data`

### Conda

### Docker

## Create or update conda environment

TODO: test this on Windows

The `full-stack-ml` environment configuration was uploaded to Anaconda cloud via `anaconda upload environment.yml` and can be found at [`louisdorard/full-stack-ml`](https://anaconda.org/louisdorard/full-stack-ml). The environment can then be created anywhere via the following command (no need to have the `environment.yml` file, but just an internet connection; replace `create` with `update` if you've already created this environment and just need to update it):

```bash
conda env create louisdorard/ml-workshops
```

For development purposes, you can make changes to the environment config and then make sure that the environment can be created or updated. For this, execute the following command from this repo's directory (again, `create` can be replaced by `update`):

```bash
conda env create -f environment.yml
```

## Build docker image

From the `docker/` subdirectory:

```bash
docker-compose build
```

Test all is working well by starting a docker container from the docker image that was built, and executing a notebook:

```bash
docker-compose up
```

If needed, get access to an interactive bash session with this command:

```bash
docker-compose run full-stack-ml bash
```
