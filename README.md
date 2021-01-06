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

* [Kaggle](https://www.kaggle.com) — ML competitions platform. We'll use it to download datasets and send predictions for evaluation.
* [Gradient](https://gradient.paperspace.com) — cloud ML development and deployment platform. We explain its benefits in the [Cloud platform](#cloud-platform) section below, and we provide information to get started.

Note that Gradient is a paid service which offers some free functionalities. No credit card is required for creating your account. If you get asked for one, feel free to ignore. We'll add you to our Gradient team so you'll be able to use all paid features during the workshop, without having to enter your credit card.

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
   (Note that this downloads and uses the `environment.yml` file from [Anaconda Cloud](https://anaconda.org/louisdorard/full-stack-ml), which might be different from the local file, if you have made any changes.)
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
9. Since Jupyter is a web-based environment, you might need to update your web browser to ensure proper functioning of the Jupyter (Lab) interface.

Remarks:

* If you run into any difficulties with installing this environment, you can try using a Docker-powered environment, based on the [`louisdorard/full-stack-ml` image](https://hub.docker.com/repository/docker/louisdorard/full-stack-ml) and on the docker-compose configuration in [`setup/docker/`](setup/docker/)). The installation steps above match the instructions in the [Dockerfile](setup/docker/Dockerfile) used to create that image, so you can jump straight to the next section.
* Alternatively, you can also try using a [cloud platform](#cloud-platform).

## Set environment variables

Add environment files:

* `.env` (at the root of this repo), which will store the `DATA_PATH` variable: this should be the path to the directory where you store raw data files. This variable will be used by our data loading utils ([mlxtend.utils.data](https://github.com/louisdorard/mlxtend/tree/master/mlxtend/utils/data.py)).
* `~/auth.env` (in your **home folder** this time), which will contain Kaggle and Gradient authentication variables.

As a starting point, you can copy the sample files found in `setup/`, which contain example key/value pairs. You'll need to change the values!
```bash
cp setup/sample.env .env
cp setup/sample-auth.env ~/auth.env
```

* For Kaggle:
   * Your username can be found in the top right corner of the Kaggle web interface, once you're logged in. Let's call it `USERNAME` (please replace in the URL below)
   * Go to the _API_ section on https://www.kaggle.com/`USERNAME`/account and click on _Create New API Token_
* For Gradient:
   * You can create an API key from https://www.paperspace.com/console/account/api: enter a Name (this can be whatever you want, e.g. "workshop"), a Description (optional), and click on "Create API token".
   * Your project ID can be found at https://www.paperspace.com/console/projects.

Finally, add the following line at the end of your shell config file (e.g. `~/profile` or `~/.bash_profile` or `~/.bashrc` for bash):
```bash
source auth.env
```
This will allow you to use the `kaggle` CLI, for downloading datasets or uploading submissions.

Note: the `.env` file is kept specific to the current project; this allows to specify different data paths for different projects, in different repos. The same `~/auth.env` file can be useful for several different projects.

## Download data

We'll use 4 datasets (the first 3 are from Kaggle competitions):

* [Avazu](http://kaggle.com/c/avazu-ctr-prediction/) (~1 GB compressed - 7 GB uncompressed) - classification - categorical features with many possible values
* [House Prices](https://www.kaggle.com/c/house-prices-advanced-regression-techniques/) (~200 KB) - regression - numerical and categorical features
* [Give Me Some Credit](https://www.kaggle.com/c/GiveMeSomeCredit/) (~7 MB) - classification - numerical features
* [MNIST](http://yann.lecun.com/exdb/mnist/) (~55 MB) - classification - numerical features, no missing values (pixels)

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

We'll be using the Gradient cloud ML platform during this workshop (see link in _Accounts_ section).

<!--
As a first step, please send the email address associated to your Gradient account to your instructor via Slack (@louis or @christophe), so he can add you to our Gradient team. In case you missed it, the Slack invite link was sent to you in the workshop confirmation email. Slack is the preferred way to communicate with your instructor during and prior to the workshop.
-->

There are 2 main ways to use Gradient: for [Running Jobs](#running-jobs-on-gradient) (paid feature) and for [Running Notebooks](#running-notebooks-on-gradient). Once we have added you to our Gradient team, you'll be able to run Jobs without having to pay. In the meantime, you can run Notebooks for free with a "Free-CPU" cloud instance.

### Why cloud ML platforms / Gradient?

* It’s common practice to use powerful machines in the cloud for Machine and Deep Learning experiments, equipped with GPUs or high-performing CPUs with many cores. They make it faster to run jobs, and they can continue running while your laptop is closed.
* Another advantage of the cloud is that you can have access to a development environment without having to install anything. You can have access to this workshop's development environment via Notebooks, which will run a docker container based on this repo's docker image.
* ML platforms (as opposed to regular cloud services) like Gradient make it faster to set up cloud machines and more convenient to persist work done on these machines.
* You won’t have to use your own wifi for downloading heavy datasets (some of which weigh several GBs): downloads will happen via the platform's internet connection (FYI Gradient's download speed can reach ~ 80 MB/s).

### Running Jobs on Gradient

When we add you to our team project, you'll have access to paid features such as running Jobs. But if you don't want to wait until we add you to the team, you can add a credit card to your Gradient Private Workspace. A "workspace" on ML cloud platforms is a place where you can create projects, in which all your experiment files will be stored (code, assets, outputs, results).

1. Install the Gradient CLI (Command Line Interface)
   ```bash
   pip install -U gradient
   ```
2. Add your API key (assuming that you've already added `GRADIENT_API_KEY` to `auth.env` and sourced it):
   ```bash
   gradient apiKey $GRADIENT_API_KEY
   ```
   The key gets stored in `~/.paperspace/config.json`.
3. Create and run your Jobs via the [`Experiments.ipynb`](Experiments.ipynb) Bash notebook.

### Running Notebooks on Gradient

Notebooks on Gradient provide an interesting way to get started faster with ML development, or when you don't want to have to install anything on your machine.

* When we add you to our team workspace, you'll have access to our data storage (mapped to `/storage/data/`), where the necessary data files have already been copied. But if you want to start using some of the notebooks here in the meantime, you'll need to use your Private Workspace and to [download that data](#download-data).
* You'll need to start by creating a Notebook and setting environment variables:
  * Click on _Create Notebook_ at https://www.paperspace.com/console/notebooks
    * In "01. Choose Container":
      * "Enter Container Name" -> _louisdorard/full-stack-ml_ 
      * "Container user" -> _root_
    * In "02. Choose Machine", pick _Free-CPU_
    * Click on _Create Notebook_ to confirm everything
  * Once the notebook is running, get the _Notebook ID_ from the list
  * Go to https://NOTEBOOK_ID.gradient.paperspace.com/lab
  * Click on "New terminal"
  * Adapt the following commands by adding your Kaggle username and key, and execute:
    ```bash
    git clone https://github.com/louisdorard/full-stack-ml.git

    sudo echo "export KAGGLE_USERNAME=" >> /root/.bashrc
    sudo echo "export KAGGLE_KEY=" >> /root/.bashrc

    sudo bash full-stack-ml/scripts/Download-Data.sh
    ```

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
   * I recommend [Cmder](https://cmder.net) (which uses Bash by default). Download the "Full" version of Cmder, which includes Git.
   * Other popular options to use the command line for Windows users are [Cygwin](http://cygwin.com), or to use the [Ubuntu](https://ubuntu.com/) linux distribution. There are 3 possible ways to do that:
      * [Ubuntu app](https://www.microsoft.com/p/ubuntu/9nblggh4msv6?activetab=pivot:overviewtab) for Windows
      * [Dual-boot installation](https://help.ubuntu.com/community/WindowsDualBoot) alongside Windows
      * [Bootable USB stick](https://ubuntu.com/tutorials/tutorial-create-a-usb-stick-on-windows#1-overview).

Once your shell and your terminal are set up, you'll be ready to execute all the commands given here! Note for Cmder users on Windows: after typing "~" in a command, press the Tab key, and it will replace "~" with the path to your home directory.

## About the author

[Louis Dorard](https://www.louisdorard.com) | Follow me on Twitter [@louisdorard](https://twitter.com/louisdorard)

