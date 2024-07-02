# reinvent-transfer-learning
Train REINVENT's model generate 3d similar molecules.


## Getting Started

To create a dev environment using `env.yml` and `conda` run the following command:

```bash
conda env create -f env.yml
```

To update already create env run the following command:

```bash
conda env update -f env.yml
```

> Make sure you are in the correct directory before running this command. 

To activate the env (reinvent-transfer-learning) run the following command:

```bash
conda activate reinvent-transfer-learning
```

> If it ran successfully then you will see `(reinvent-transfer-learning)` at the beginning of each line in your terminal

To start the notebook run the following command:

```bash
jupyter notebook 
```
> Make sure you have activated  


## Troubleshoot

#### While opening a notebook (*.ipynb) file, getting 500: internal server error

This usually happens when you have an outdated version of `nbconvert` package. To solve the error, open your terminal and update the package by running the following command:

```bash
pip install --upgrade nbconvert
```