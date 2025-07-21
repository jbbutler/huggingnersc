import typer
import os
import json
from huggingnersc_dataset import HuggingNERSCDataset
from constants import NERSC_PATH

app = typer.Typer()

@app.command()
def catalog_new_dataset(official_name: str, nickname: str, script_path: str, metadata_path: str):
    '''
    Command to catalog a new dataset on the NERSC CFS and NERSC Huggingface.
    Inputs:
        official_name (string): the name you want to give your dataset, to show up in titles, etc.
        nickname (string): name for your dataset to appear in filepaths
        script_path (string): path to .py file with your dataset's loader script in it
        metadata_path (string): path to json file with your dataset's metadata in it
    '''

    with open(metadata_path) as f:
        metadata = json.load(f)

    hn_obj = HuggingNERSCDataset(official_name, nickname)
    hn_obj.construct_repo()
    hn_obj.construct_notebook(script_path)
    hn_obj.upload_readme(metadata, script_path)
    hn_obj.save_dataset_info(metadata)

    print(f'Dataset successfully cataloged! \n NERSC Location: {hn_obj.nersc_dir} \n HuggingFace Location: {hn_obj.hf_dir}')

@app.command()
def inspect_dataset(nickname: str):
    '''
    Command to inspect and print the contents of a dataset's json metadata, if it exists.
    Inputs:
        nickname (string): the nickname of the dataset
    '''

    data_path = NERSC_PATH + nickname + '/'
    json_path = data_path + nickname + '_info.json'

    if os.path.exists(json_path):
        with open(json_path) as f:
            data_info = json.load(f)
            print(data_info)
    else:
        print('The requested dataset/metadata does not exist.')

if __name__ == '__main__':
    app()