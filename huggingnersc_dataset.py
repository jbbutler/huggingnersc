'''
Script with HuggingNERSC API. Used to facilitate interaction between Hugging Face servers
and NERSC for dataset curation.
Jimmy Butler, August 2025
'''

import huggingface_hub as hf
from jinja2 import Environment, FileSystemLoader
import json
import jsonschema as js
import os

from constants import HF_FILEPATH, HF_ORG, NERSC_PATH

class HuggingNERSCDataset:
    '''
    Object that links a dataset hosted at NERSC with a repository on the NERSC
    Hugging Face organization. Methods handle filling repository with info
    automatically.
    '''

    def __init__(self, official_name: str, nickname: str, data_path: str):
        '''
        Object constructor. Idea is to keep storage information together
        all in one place for each curated dataset.

        Inputs:
            official_name (string): the display name of the dataset
            nickname (string): the dataset name to be used in filepaths
            data_path (string): path to where the dataset is located at NERSC
        '''
        self.nickname = nickname
        self.official_name = official_name
        self.hf_dir = HF_FILEPATH + nickname + '/' # huggingface location of dataset
        self.data_dir = data_path
        self.nersc_dir = NERSC_PATH + self.nickname + '/' # 

    def __repr__(self):
        '''
        String representation.
        '''
        display_str = f'''NERSC HuggingFace Dataset Object: 
        \n -official_name: {self.official_name} 
        \n -nickname: {self.nickname}
        \n -huggingface location: {self.hf_dir}
        \n -nersc data location: {self.data_dir}
        \n -nersc catalog location: {self.nersc_dir}'''

        return display_str

    def construct_repo(self):
        '''
        Create a directory on NERSC CFS to store all things associated with the HF repo,
        like metadata, readmes, and notebooks, and create a repo on Hugging Face for 
        the dataset. Note: the data will not be stored at this NERSC CFS location,
        just the byproducts of creating the NERSC repo and metadata.
        '''
        # create a directory on NERSC CFS to store metadata, readmes, notebooks, etc.
        os.mkdir(self.nersc_dir)
        # create the dataset folder
        #os.mkdir(self.nersc_dir + 'data/')
        # create directory on NERSC Huggingface repo
        hf.create_repo(HF_ORG + '/' + self.nickname, repo_type='dataset')

    def __grab_loader_script(self, script_path: str):
        '''
        A private helper method to read the user-supplied loader script as a string.

        Inputs:
            script_path (string): the path where the loading script is located
        Outputs:
            loading_code (string): a string with all of the loading code
        '''

        with open(script_path, "r") as script:
            loading_code = script.read()
            
        return loading_code

    def upload_loader_scripts(self, script_path: str, batch_path: str = None):
        '''
        A method to upload loader script(s) onto the Hugging Face repository.

        Inputs:
            script_path (string): the path where loading script is located
            batch_path (string): optional argument; file path for any batch script needed
                to run loading script
        '''

        script_name = os.path.basename(script_path)
        # upload the loader script to HF
        api = hf.HfApi()
        api.upload_file(path_or_fileobj=script_path, 
                        path_in_repo=script_name,
                        repo_id=HF_ORG + '/' + self.nickname, repo_type='dataset')

        # if providing an example batch script to run with dataloader, also upload it
        if batch_path:
            batch_name = os.path.basename(batch_path)
            api.upload_file(path_or_fileobj=batch_path, 
                            path_in_repo=batch_name,
                            repo_id=HF_ORG + '/' + self.nickname, repo_type='dataset')

    def construct_notebook(self, script_path: str):
        '''
        Method to construct a Jupyter notebook at dataset's NERSC directory with loading
        code.

        Inputs:
            script_path (string): the loading script file
        '''

        loading_code = self.__grab_loader_script(script_path)
        
        with open('template_notebook/template_loader.ipynb', 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
        # change title
        notebook_data['cells'][0]['source'][0] = f'# {self.official_name} Data Loader'
        # change loading script
        notebook_data['cells'][1]['source'][0] = loading_code

        with open(self.nersc_dir + f'{self.nickname}_dataloader.ipynb', 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=4)

    def upload_readme(self, metadata: dict, script_path: str, nersc_portal_link: str, batch_path: str = None, distributed: bool = False):
        '''
        Method to create and upload the Hugging Face readme, filling in a template with relevant info.

        Inputs:
            metadata (dict): a dictionary with metadata that will be input in the readme (must conform to schema)
            script_path (string): loader script path
            nersc_portal_link (string): link to download data from NERSC portal
            batch_path (string): optional argument, batch script to upload dataset
            distributed (bool): whether or not the loader is distributed
        '''

        # read the json schema
        with open('metadata_schema.json') as f:
            schema = json.load(f)
        # check if metadata json file satisfies schema
        js.validate(instance=metadata, schema=schema)

        loading_code = self.__grab_loader_script(script_path)
        # copying metadata dictionary to add loading code
        # so as to not clunk up the original metadata dictionary
        fill_metadata = metadata.copy()
        fill_metadata['loading_code'] = loading_code
        fill_metadata['distributed'] = distributed #controls whether the Jupyter notebook will be created or not
        fill_metadata['nersc_loc'] = self.nersc_dir
        fill_metadata['download_link'] = nersc_portal_link
        # if supplying a batch script to run loader, add that to the template fields
        if batch_path:
            batch_code = self.__grab_loader_script(batch_path)
            fill_metadata['batch_code'] = batch_code

        # filling the readme
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('/readme_templates/readme_template.md')
        filled_readme = template.render(fill_metadata)

        # storing templated README at dataset NERSC directory
        with open(self.nersc_dir + 'README.md', 'w') as f:
            f.write(filled_readme)

        # upload to huggingface
        api = hf.HfApi()
        api.upload_file(path_or_fileobj=self.nersc_dir + 'README.md', 
                        path_in_repo='README.md',
                        repo_id=HF_ORG + '/' + self.nickname, repo_type='dataset')

    def save_dataset_info(self, metadata: dict):
        '''
        Save all metadata associated with dataset at NERSC dataset location. Things like
        data location at NERSC, Hugging Face repo link, and metadata on the Hugging Face repo.

        Inputs:
            metadata (dict): the user-supplied metadata for the dataset (that went on Hugging Face)
        '''
        
        dataset_info = self.__dict__
        dataset_info['metadata'] = metadata
        
        with open(self.nersc_dir + f'{self.nickname}_info.json', 'w') as f:
            json.dump(dataset_info, f, indent=4)