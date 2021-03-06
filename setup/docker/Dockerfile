# TODO: credit Aurélien Géron's Dockerfile from which this one is inspired

FROM continuumio/miniconda3:latest


####
# Update all system packages, install additional packages, and update conda
####

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
        git \
        sudo \
        unzip zip \
        curl \
        jq

RUN conda update -y -n base conda


####
# Set up /data (to be used as DATA_PATH -- see accompanying docker-compose.yml)
####

RUN mkdir /data


####
# Install conda environment
# This uses environment.yml, which is in the build context (see README.md#Building-the-docker-image)
####

COPY environment.yml /tmp/
RUN conda env create -f /tmp/environment.yml \
    && rm /tmp/environment.yml
RUN conda clean -y -t
# IDEA: is this also cleaning the new environment? combine this line with previous one?
# IDEA: try -a (all) instead of -t (tarballs only)?

ENV PATH /opt/conda/envs/full-stack-ml/bin:$PATH
RUN conda init bash
RUN chsh -s /bin/bash

# Finalize Jupyter installation and configuration
COPY jupyter-install.bash /tmp/
RUN bash /tmp/jupyter-install.bash && rm /tmp/jupyter-install.bash


####
# Configure user
####

ARG username=devel
ARG userid=1000

ARG home=/home/${username}
ARG workdir=${home}/full-stack-ml

RUN adduser ${username} --uid ${userid} --gecos '' --disabled-password \
    && echo "${username} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${username} \
    && chmod 0440 /etc/sudoers.d/${username}

WORKDIR ${workdir}
RUN chown ${username}:${username} ${workdir}

USER ${username}
WORKDIR ${workdir}

# conda setup for user
ENV PATH /opt/conda/envs/full-stack-ml/bin:$PATH
RUN conda init bash

COPY docker/bashrc.bash /tmp/
RUN cat /tmp/bashrc.bash >> ${home}/.bashrc \
    && echo "export PATH=\"${workdir}/docker/bin:$PATH\"" >> ${home}/.bashrc \
    && sudo rm /tmp/bashrc.bash


# The config below enables diffing notebooks with nbdiff (and nbdiff support
# in git diff command) after connecting to the container by "make exec" (or
# "docker-compose exec full-stack-ml bash")
#       You may also try running:
#         nbdiff NOTEBOOK_NAME.ipynb
#       to get nbdiff between checkpointed version and current version of the
# given notebook.

RUN git-nbdiffdriver config --enable --global

# INFO: Optionally uncomment any (one) of the following RUN commands below to ignore either
#       metadata or details in nbdiff within git diff
#RUN git config --global diff.jupyternotebook.command 'git-nbdiffdriver diff --ignore-metadata'
RUN git config --global diff.jupyternotebook.command 'git-nbdiffdriver diff --ignore-details'


# INFO: Uncomment lines below to enable automatic save of python-only and html-only
#       exports alongside the notebook
#COPY docker/jupyter_notebook_config.py /tmp/
#RUN cat /tmp/jupyter_notebook_config.py >> ${home}/.jupyter/jupyter_notebook_config.py
#RUN sudo rm /tmp/jupyter_notebook_config.py


# INFO: Uncomment the RUN command below to disable git diff paging
#RUN git config --global core.pager ''


# INFO: Uncomment the RUN command below for easy and constant notebook URL (just localhost:8888)
#       That will switch Jupyter to using empty password instead of a token.
#       To avoid making a security hole you SHOULD in fact not only uncomment but
#       regenerate the hash for your own non-empty password and replace the hash below.
#       You can compute a password hash in any notebook, just run the code:
#          from notebook.auth import passwd
#          passwd()
#       and take the hash from the output
#RUN mkdir -p ${home}/.jupyter && \
#    echo 'c.NotebookApp.password = u"sha1:c6bbcba2d04b:f969e403db876dcfbe26f47affe41909bd53392e"' \
#    >> ${home}/.jupyter/jupyter_notebook_config.py


# Change default shell
# RUN chsh -s /bin/bash
USER root
RUN usermod ${username} -s /bin/bash
