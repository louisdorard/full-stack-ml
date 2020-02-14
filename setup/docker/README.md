# Docker for the Full-Stack ML Workshops

## Prerequisites

You need 2 things:

* `docker` - see instructions on how to [Install Docker](https://docs.docker.com/engine/installation/)
* `docker-compose` - see instructions on how to [Install Docker Compose](https://docs.docker.com/compose/install/)

Some general knowledge about `docker` infrastructure might be useful (that's an interesting topic on its own), but it isn't strictly required to just run the code.

## Usage

### Using Docker for tests before running jobs on cloud platform

* Download the Docker image with `docker pull louisdorard/full-stack-ml`.
* Adapt [`docker-compose.yml`](docker-compose.yml):
  * Make sure that the `volumes` property has an item which is `X:/data` (mapping `X` on the host to `/data` in the container, where `X` is the path to your raw data files)
  * Adapt location of `auth.env` in the `env_file` property, if needed
* Run Python notebooks as scripts in a Docker container:

   ```bash
   export NOTEBOOK_NAME="00-Version-Information"
   export CMD="papermill $NOTEBOOK_NAME.ipynb output/$NOTEBOOK_NAME.ipynb"
   bash -c "cd docker; docker-compose run full-stack-ml $CMD"
   ```

### Serving Jupyter notebooks

From the `docker/` subdirectory, run the following command:

```bash
docker-compose up
```

This starts a docker container which runs a Jupyter server as its main command.


## Building the docker image

```bash
docker-compose build
```

If needed, get access to an interactive bash session with this command:

```bash
docker-compose run full-stack-ml bash
```

Pushing the image (this is only for me, the author :) :

```bash
docker tag full-stack-ml louisdorard/full-stack-ml
docker push louisdorard/full-stack-ml
```
