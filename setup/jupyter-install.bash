# TODO: activate full-stack-ml environment first?
conda activate full-stack-ml

# Make the kernel of the environment accessible via its own name (i.e. "full-stack-ml" instead of "Python [conda env:full-stack-ml]")
python -m ipykernel install --name full-stack-ml

# Install Bash kernel
python -m bash_kernel.install

# Install and enable Jupyter extensions
# (some where already installed via conda packages included in environment.yml)

jupyter contrib nbextension install
jupyter nbextension enable livemdpreview/livemdpreview
jupyter nbextension enable hinterland/hinterland
jupyter nbextension enable snippets/main
jupyter nbextension enable snippets_menu/main
jupyter nbextension enable toc2/main
jupyter nbextension enable --py --sys-prefix qgrid
jupyter nbextension enable varInspector

jupyter labextension install @lckr/jupyterlab_variableinspector
jupyter labextension install @jupyterlab/toc
jupyter labextension install @jupyterlab/git
jupyter labextension install nbdime-jupyterlab
jupyter labextension install jupyterlab-jupytext

jupyter lab build