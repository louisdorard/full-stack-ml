# Full-Stack Machine Learning Workshops

<img src="http://s3.louisdorard.com.s3.amazonaws.com/ML_icon.png">

This repository serves as a base for my online course and in-person workshops. It contains Jupyter notebooks, Python scripts (automatically generated from notebooks), and environment configurations (conda and docker). Join for exclusive additional content (exercices and ressources) — reach out to me at [louisdorard.com/contact](https://www.louisdorard.com/contact) for more information!

Below is a description of the contents of this repo, and a list of steps to prepare for the exercises and projects you'll do on your laptop ("set-up"):

## Contents

### Core

During the course/workshop you'll be using the following Jupyter notebooks:

* `Experiments.ipynb`: Bash notebook to run notebook-based experiments, locally or on cloud infrastructure
* More to come! Click on "Watch" to get notified.

### Others

The repo also contains:

* `setup/`: files used to prepare the ML development environment
* `scripts/`: Python and Bash scripts automatically generated from notebooks by `jupytext`

### Set-up

  - [Create accounts](#create-accounts)
  - [Install development environment](#install-development-environment)
  - [Set environment variables](#set-environment-variables)
  - [Download data](#download-data)
  - [Test environment](#test-environment)
  - [Cloud platform](#cloud-platform)
  - [Install IDE (optional)](#install-ide-optional)
  
All commands given below should be executed from the root of this repo and are meant for the `bash` shell (see [Appendix: set-up shell](#appendix-set-up-shell) if needed).

## Create accounts

You'll need accounts on the following platforms:

* [Kaggle](https://www.kaggle.com): ML competitions
* [Gradient](https://gradient.paperspace.com): cloud ML development and deployment (freemium - no credit card required for this workshop)

## Install development environment

Our ML development environment is based on Python and Jupyter. We use `conda` to install it. [Conda](https://conda.io) is a Python distribution, an environment manager, and a package manager (it resolves dependencies).

1. Clone this repo and `cd` into it:
   ```bash
   git clone https://github.com/louisdorard/full-stack-ml.git
   cd full-stack-ml/
   ```
2. Create an `output/` directory, meant for storage of artifacts from notebook executions and experiments (note: it's included in [`.gitignore`](.gitignore)).
   ```bash
   mkdir output/
   ```
3. Install `conda`. The fastest way for this is to install [Miniconda](https://conda.io/en/latest/miniconda.html) (a mini version of [Anaconda](https://docs.continuum.io/anaconda/)): see official instructions for [Windows](https://conda.io/projects/conda/en/latest/user-guide/install/windows.html#install-win-silent) (use the example command), [macOS](https://conda.io/projects/conda/en/latest/user-guide/install/macos.html#install-macos-silent) (use the example command under _Installing in silent mode_), or [Linux](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html). If you're asked whether to add (Ana)conda to you PATH, choose yes (or tick the appropriate box in the graphical installer). (Note: On macOS I used [Homebrew](https://brew.sh): `brew cask install miniconda`.)
4. Update conda:
   ```bash
   conda update —all -y
   ```
5. Create the `full-stack-ml` environment, which will contain the packages listed in [`environment.yml`](setup/environment.yml):
   ```bash
   conda install anaconda-client
   conda env create louisdorard/full-stack-ml
   ```
   (Note that this downloads and uses the `environment.yml` file from [Anaconda Cloud](https://anaconda.org/louisdorard/full-stack-ml) — which might be different from the local file.)
6. Initialize conda for your shell (replace `YOUR_SHELL_NAME` with the name of your shell, e.g. `bash`):
   ```bash
   conda init YOUR_SHELL_NAME
   ```
7. Activate the `full-stack-ml` environment:
   ```bash
   conda activate full-stack-ml
   ```
8. Run script to finalize Jupyter installation and configuration:
   ```bash
   bash setup/jupyter-install.bash
   ```

Remarks:

* If you run into any difficulties with installing this environment, you can try using a Docker-powered environment, based on the [`louisdorard/full-stack-ml` image](https://hub.docker.com/repository/docker/louisdorard/full-stack-ml) and on the docker-compose configuration in [`setup/docker/`](setup/docker/)). The installation steps above match the instructions in the [Dockerfile](setup/docker/Dockerfile) used to create that image, so you can jump straight to the next section.
* Alternatively, you can also try using a [cloud platform](#cloud-platform).

## Set environment variables

1. Add path to directory where you store raw data files, in `~/.env`. Add Kaggle and Gradient authentication variables in `~/auth.env`. As a starting point, you can just copy the [`sample-auth.env`](setup/sample-auth.env) and [`sample.env`](setup/sample.env) files found in `setup/`, which contain example key/value pairs. You'll need to change the values!
   1. For Kaggle:
      * Your username can be found in the top right corner of the Kaggle web interface, once you're logged in. Let's call it `USERNAME` (please replace in the URL below)
      * Go to the _API_ section on https://www.kaggle.com/`USERNAME`/account and click on _Create New API Token_
   2. For Gradient:
      * You can create an API key from https://www.paperspace.com/console/account/api: enter a Name (this can be whatever you want, e.g. "workshop"), a Description (optional), and click on "Create API token".
      * Your project ID can be found at https://www.paperspace.com/console/projects.
2. Add the following lines at the end of your shell config file (e.g. `~/.bash_config` or `~/.bashrc` for bash):
   ```bash
   source .env
   source auth.env
   ```

## Download data

We'll use 3 datasets from Kaggle competitions:

* [Avazu](http://kaggle.com/c/avazu-ctr-prediction/) (~1 GB compressed - 7 GB uncompressed)
* [House Prices](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/) (~200 KB)
* [Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit/) (~7 MB)

They can be downloaded to your raw data directory with the following command:

```bash
bash setup/scripts/Download-Data.sh
```

## Test environment

Assuming that you've already activated the `full-stack-ml` environment in your current shell session...

1. Test that the environment is functional by running `00-Version-Information.ipynb`, which displays the versions of the core libraries used in this workshop:
   
   ```bash
   papermill 00-Version-Information.ipynb output/00-Version-Information.ipynb
   ```
   The output notebook should contain:
   ```
   sklearn	0.22.1
   ```
2. Test notebooks (this can take a couple of minutes):
   ```bash
   jupytext --from ipynb --execute ??-*.ipynb
   ```
3. Fire up Jupyter Lab, to interact with the notebooks:
   ```bash
   jupyter-lab
   ```

This should automatically open your browser at http://localhost:8888/

## Cloud platform

TODO: include Gradient.md (work in progress, see _gradient_ branch of this repo)

## Install IDE (optional)

Using an IDE can be a useful complement to Jupyter Lab, e.g. for linting or refactoring or moving code around, or for creating Python modules. I recommend [Visual Studio Code](https://code.visualstudio.com) (VS Code):

* It's a free and popular IDE for many programming languages
* It has built-in support for Git

Go through [Getting Started with Python in VS Code](https://code.visualstudio.com/docs/python/python-tutorial). Alternative ways to install it are to use Homebrew on macOS (`brew cask install visual-studio-code`), or to download from the [Snap Store](snapcraft.io/store) on Linux.

Some recommended extensions: Python, Docker, Rainbow CSV, Excel Viewer, Markdown All in One.

## Appendix: set-up shell

Installation of the development environment is done from the shell. The most popular option is Bash; however, I prefer to use the [fish shell](http://fishshell.com). Regarding terminals:

* macOS: I recommand [iTerm](http://iterm2.com).
* Windows:
   * I recommend [Cmder](https://cmder.net) (which uses Bash by default). Download the "Full" version of cmder, which includes Git. You'll need to right-click on `Cmder.exe` and choose _Run as administrator_ (otherwise you won't be able to create conda environments).
   * Other popular options to use the command line for Windows users are [Cygwin](http://cygwin.com), or to use the [Ubuntu](https://ubuntu.com/) linux distribution. There are 3 possible ways to do that:
      * [Ubuntu app](https://www.microsoft.com/p/ubuntu/9nblggh4msv6?activetab=pivot:overviewtab) for Windows
      * [Dual-boot installation](https://help.ubuntu.com/community/WindowsDualBoot) alongside Windows
      * [Bootable USB stick](https://ubuntu.com/tutorials/tutorial-create-a-usb-stick-on-windows#1-overview).

Once your shell and your terminal are set up, you'll be ready to execute all the commands given here!

## About the author

[Louis Dorard](https://www.louisdorard.com) | Follow me on Twitter [@louisdorard](https://twitter.com/louisdorard)

