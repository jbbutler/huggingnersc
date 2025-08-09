import huggingface_hub as hf
from jinja2 import Environment, FileSystemLoader
import json
import jsonschema as js
import os

from constants import HF_FILEPATH, HF_ORG, NERSC_PATH

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

    def __grab_loader_script(self, script_path: str):

        with open(script_path, "r") as script:
            loading_code = script.read()
            
        return loading_code

    def upload_loader_scripts(self, script_path: str, batch_path: str = None):

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
        Method to template and upload the README.
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
        if batch_path:
            batch_code = self.__grab_loader_script(batch_path)
            fill_metadata['batch_code'] = batch_code

        # filling the readme
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('/readme_templates/readme_template.md')
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