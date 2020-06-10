# Docker for the Full-Stack ML Workshops

## Prerequisites

You need 2 things:

* `docker` - see instructions on how to [Install Docker](https://docs.docker.com/engine/installation/)
* `docker-compose` - see instructions on how to [Install Docker Compose](https://docs.docker.com/compose/install/)

Some general knowledge about `docker` infrastructure might be useful (that's an interesting topic on its own), but it isn't strictly required to just run the code.

## Usage

### Using Docker for tests before running jobs on cloud platform

* Download the Docker image with `docker pull louisdorard/full-stack-ml`.
* Check the docker-compose configuration with the following command, executed from the current directory (`setup/docker/`):
    ```bash
    docker-compose config
    ```
  * At first, `${DATA_PATH}` won't be resolved. Create a link at `setup/docker/.env` to the `.env` file at this repo's root. Thus, in the docker-compose configuration, `${DATA_PATH}` will get replaced with the value contained in that file.
    ```bash
    ln ../../.env .env
    ```
  * In [`docker-compose.yml`](docker-compose.yml), you might need to adapt the location of `auth.env` in the `env_file` property, in case this file isn't in your home directory (`~`).
  * Some remarks on `DATA_PATH`: In this repo we use a data loader found in [mlxtend.utils.data](https://github.com/louisdorard/mlxtend/tree/master/mlxtend/utils/data.py). It starts looking for data files in the `DATA_PATH` environment variable. This is `/data` in the docker container, which is mapped to `${DATA_PATH}` on the host... i.e. the location where the data files are!
* Run Python notebooks as scripts in a Docker container, from this repo's root:

   ```bash
   export NOTEBOOK_NAME="00-Version-Information"
   export CMD="papermill $NOTEBOOK_NAME.ipynb output/$NOTEBOOK_NAME.ipynb"
   bash -c "cd setup/docker/; docker-compose run full-stack-ml $CMD"
   ```

### Serving Jupyter notebooks

From the `setup/docker/` subdirectory, run the following command:

```bash
docker-compose up
```

This starts a docker container which runs a Jupyter server as its main command. When you're done, shut it down with:

```bash
docker-compose down
```

## Building the docker image

This is done by Docker Hub.

The configuration can be edited at [https://hub.docker.com/repository/docker/louisdorard/full-stack-ml/builds/edit](https://hub.docker.com/repository/docker/louisdorard/full-stack-ml/builds/edit) (build rules, build environment variables, etc.) (this is only accessible to the owner of this repo).

### Building locally

Add the following to `docker-compose.yml`, under the `full-stack-ml` service:

```
    build:
      context: ../ # i.e. the setup/ directory
      dockerfile: ./docker/Dockerfile
    container_name: full-stack-ml
```

Trigger the build with:

```bash
docker-compose build
```

If needed, get access to an interactive bash session with:

```bash
docker-compose run full-stack-ml bash
```

Pushing the image (this is only accessible to the owner of this repo :)) :

```bash
docker tag full-stack-ml louisdorard/full-stack-ml
docker push louisdorard/full-stack-ml
```
