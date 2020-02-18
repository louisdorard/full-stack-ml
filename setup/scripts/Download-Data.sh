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

pushd $DATA_PATH

mkdir avazu
pushd avazu/
kaggle competitions download -c avazu-ctr-prediction
unzip avazu-ctr-prediction.zip && rm avazu-ctr-prediction.zip
popd

mkdir house-prices
pushd house-prices/
kaggle competitions download -c house-prices-advanced-regression-techniques
unzip house-prices-advanced-regression-techniques.zip && rm house-prices-advanced-regression-techniques.zip
popd

mkdir give-me-some-credit
pushd give-me-some-credit/
kaggle competitions download -c GiveMeSomeCredit
unzip GiveMeSomeCredit.zip && rm GiveMeSomeCredit.zip
popd
