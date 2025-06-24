import pandas as pd
import huggingface_hub as hf
import os


HF_FILEPATH = 'https://huggingface.co/datasets/butlerj/'
HF_ORG = 'butlerj'
NERSC_PATH = '/global/cfs/projectdirs/dasrepo/data_curation/'

class HuggingNERSCDataset:

    def __init__(self, dataset_name, metadata):
        self.dataset_name = dataset_name
        self.hf_dir = HF_FILEPATH + dataset_name
        self.nersc_dir = NERSC_PATH + dataset_name
        self.metadata = metadata
        self.__make_directory()
        self.__make_repository()

    def __make_directory(self):
        os.mkdir(self.nersc_dir)

    def __make_repository(self):
        hf.create_repo(HF_ORG + '/' + self.dataset_name, repo_type="dataset")

#def __upload_readme(self):
    
    

#def construct_entry(self):
    
    


#def upload_data(self):
    