import pandas as pd
import huggingface_hub as hf
from jinja2 import Environment, FileSystemLoader
import json
import os

from constants import HF_FILEPATH, HF_ORG, NERSC_PATH, NERSC_WEB_PATH

class HuggingNERSCDataset:

    def __init__(self, official_name: str, nickname: str):
        self.nickname = nickname
        self.official_name = official_name
        self.hf_dir = HF_FILEPATH + nickname + '/'
        self.nersc_dir = NERSC_PATH + nickname + '/'

    def __repr__(self):
        display_str = f'''NERSC HuggingFace Dataset Object: 
        \n -official_name: {self.official_name} 
        \n -nickname: {self.nickname}
        \n -huggingface location: {self.hf_dir}
        \n -nersc location: {self.nersc_dir}'''

        return display_str

    def construct_repo(self):
        # create a directory on NERSC CFS repo
        ## Assume repo on NERSC CFS is already created
        #os.mkdir(self.nersc_dir)
        # create the dataset folder
        #os.mkdir(self.nersc_dir + 'data/')
        # create directory on NERSC Huggingface repo
        hf.create_repo(HF_ORG + '/' + self.nickname, repo_type='dataset')

    def __grab_loader_script(self, filename: str):

        # grab and fill loader script as simple python string
        with open('loader_templates/basic_loader.py', 'r') as file:
            loading_code = file.read()
        loading_code = eval('f' + repr(loading_code))

        return loading_code

    def construct_notebook(self, filename: str):

        loading_code = self.__grab_loader_script(filename)
        
        with open('template_notebook/template_loader.ipynb', 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
        # change title
        notebook_data['cells'][0]['source'][0] = f'# {self.official_name} Data Loader'
        # change loading script
        notebook_data['cells'][1]['source'][0] = loading_code

        with open(self.nersc_dir + f'{self.nickname}_dataloader.ipynb', 'w', encoding='utf-8') as f:
            json.dump(notebook_data, f, indent=4)

    def upload_readme(self, metadata: dict):

        loading_code = self.__grab_loader_script(metadata['filename'])

        # copying metadata dictionary to add loading code
        # so as to not clunk up the original metadata dictionary
        fill_metadata = metadata.copy()
        fill_metadata['loading_code'] = loading_code
        fill_metadata['nersc_loc'] = self.nersc_dir
        fill_metadata['download_link'] = NERSC_WEB_PATH + self.nickname + '/data/'

        # filling the readme
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('readme_template.md')
        filled_readme = template.render(fill_metadata)
        
        with open(self.nersc_dir + 'README.md', 'w') as f:
            f.write(filled_readme)

        # upload to huggingface
        api = hf.HfApi()
        api.upload_file(path_or_fileobj=self.nersc_dir + 'README.md', 
                        path_in_repo='README.md',
                        repo_id=HF_ORG + '/' + self.nickname, repo_type='dataset')

    def save_dataset_info(self, metadata: dict):
        
        dataset_info = self.__dict__
        dataset_info['metadata'] = metadata
        
        with open(self.nersc_dir + f'{self.nickname}_info.json', 'w') as f:
            json.dump(dataset_info, f, indent=4)