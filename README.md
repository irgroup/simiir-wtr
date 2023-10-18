# Simulating Users in Interactive Web Table Retrieval

This repository accompanies our CIKM'23 short paper submission entitled "Simulating Users in Interactive Web Table Retrieval". It contains the code and results to make the experiments transparent and reproducible. All of the experiments can be reproduced with the help of the source code and the Jupyter notebooks. Before rerunning the code, the web table retrieval (WTR) data has to be downloaded from [this repository](https://github.com/Zhiyu-Chen/Web-Table-Retrieval-Benchmark).

The code can be rerun to reproduce the experiments, but we also provide the generated resources like queries or simulated interaction logs in the subdirectories.

## Publication
The author's version of the work can be found on the [arXiv](). Please cite the work as follows:
```
@inproceedings{10.1145/3583780.3615187, 
    author = {Engelmann, Björn and Breuer, Timo and Schaer, Philipp}, 
    title = {Simulating Users in Interactive Web Table Retrieval}, 
    year = {2023},     
    publisher = {Association for Computing Machinery}, 
    address = {New York, NY, USA},     
    doi = {10.1145/3583780.3615187}, 
    booktitle = {Proceedings of the 32nd ACM International Conference on Information and Knowledge Management (CIKM '23), October 21--25, 2023, Birmingham, United Kingdom}, 
    series = {CIKM '23} 
}
```

## Query datasets

- [Doc2Query dataset](./doc2queries)
- [GPT-3.5 dataset](./wtr/wtr-uqvs-orig.txt)

## Directory 

This repository is a fork of [SIMIIR 2.0](https://github.com/padre-lab-eu/simiir-2). In the following, we list the directory that were added by us.

| Directory | Description |
| --- | --- |
| `doc2queries/` | This directory contains the generated queries for every table in the WTR dataset. |
| `query_expansion_server/` | This directory contains the webserver required for on-the-fly querying during the simulations. |
| `sims/` | This directory contains the user configurations and the simulated interaction logs. |
| `wtr/` | This directory contains the additional resources that are required to use the simulation toolkit for interactive WTR experiments. |

## Notebooks

| Notebook | Description |
| --- | --- |
| [`main.ipynb`](./main.ipynb) | Use this notebook to rerun the simulations. |
| [`main_eval.ipynb`](./main_eval.ipynb) | Use this notebook to evaluate the simulations. |
