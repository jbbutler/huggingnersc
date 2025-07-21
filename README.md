# HuggingNERSC

An API facilitating use of Huggingface to catalog NERSC-hosted datasets.

Implements a CLI to catalog your dataset on NERSC's Huggingface repo, populating a readme with desired metadata (making your dataset more searchable), adding a dataloader script, and providing public links to download the data from NERSC. Also links your dataset entry on Huggingface to a location on the NERSC CFS.

To catalog your dataset, use the following command, 

```
python main.py <official_name> <nickname> <script_path> <metadata_path>
```

with the following inputs:

+ `official_name` the name of your dataset you'd like to see in titles, etc.
+ `script_path` path to the dataloader script you'd like to provide (.py file only)
+ `nickname` the name you'd like to see in filepaths
+ `metadata_path` path to a json file with metadata that describes your dataset (to be added to the Huggingface repository)