# HuggingNERSC

An API facilitating use of Huggingface to catalog NERSC-hosted datasets.

Implements a CLI to catalog your dataset on NERSC's Huggingface repo, populating a readme with desired metadata (making your dataset more searchable), adding a dataloader script, and providing public links to download the data from NERSC. Also links your dataset entry on Huggingface to a location on the NERSC CFS.

To catalog your dataset, use the following command, where `official_name` is the name of your dataset you'd like to see in titles, etc., `nickname` is the name you'd like to see in filepaths, `script_path` is a path to the dataloader script you'd like to provide (.py file only), and `metadata_path` is a path to a json file with metadata that describes your dataset (to be added to the Huggingface repository).

```
python main.py <official_name> <nickname> <script_path> <metadata_path>
```