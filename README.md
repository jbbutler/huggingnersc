# HuggingNERSC

An API that interfaces with the NERSC organization on Hugging Face (https://huggingface.co/NERSC), enabling users to catalog their datasets on a Hugging Face repo and link them to their stored locations at NERSC.

A CLI is also provided to catalog new datasets and upload already-cataloged datasets, implementing the HuggingNERSC API under-the-hood.

## The CLI

### What Does it Do?

Easily curate a dataset in a repo on the NERSC Hugging Face organziation by executing a single line in a terminal. 

An example of a repo created for Sir Ronald Fisher's famous iris classification dataset is shown below.

![Example of iris classification dataset repo.](images/iris_example_annotated.png)

See for yourself: https://huggingface.co/datasets/NERSC/iris

### Setup
To use the any of the CLI commands, first clone this repository.
```
git clone https://github.com/jbbutler/huggingnersc
```

Next, make sure to create and activate the conda environment with relevant software packages.
```
conda env create -f huggingnersc_env.yml
conda activate huggingnersc_env
```

### Cataloging a New Dataset
To catalog a new dataset on the NERSC Hugging Face organization, use the `catalog_new_dataset` function
```
python main.py catalog-new-dataset <official_name> <nickname> <loader_script> <metadata_json> <optional: batch_script> <optional: is_distributed>
```
with the following specifications
+ `<official_name>`: the title of your dataset that you want displayed on the repo page
+ `<nickname>`: the name to use in filepaths
+ `<loader_script>`: a script to load up the data
+ `<metadata_json>`: a json file containing metadata tags, etc. you want displayed on the repo dataset card (NOTE: must comply with schema in `metadata_schema.json`; more on this later)
+ `<batch_script>`: an optional parameter, defaults to `None`; if you want to provide a batch script to run your data loader code (useful for multi-node distributed data loaders)
+ `<is_distributed>`: an optional parameter, defaults to `False`; if providing a distributed data loader, will not template a Jupyter notebook (*Pending me figuring out how to provide distributed data loaders on jupyter.nersc.gov...*)

### Inspecting an Already-Cataloged Dataset

TODO: fill in

### Metadata JSON

TODO: describe structure of metadata json files so that they adhere to schema
