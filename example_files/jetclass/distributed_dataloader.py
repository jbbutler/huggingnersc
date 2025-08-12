import os
import torch
from torch.utils.data import Dataset, DataLoader
from torch.utils.data.distributed import DistributedSampler
from torch.distributed import init_process_group, destroy_process_group

class JetClassDataset(Dataset):
    def __init__(self, data_dir):
        self.data_dir = data_dir
    def __len__(self):
        return len(os.listdir(self.data_dir))*100000
    def __getitem__(self, idx):
        filenum = idx//100000
        idxfile = idx%100000
        f = h5py.File(os.path.join(self.data_dir, f'JetClass_{filenum}.h5'), 'r')
        jet_features = f['data'][idxfile]
        jet_label = f['pid'][idxfile]

        return jet_features, jet_label

world_size = int(os.environ['WORLD_SIZE'])
init_process_group(backend='nccl', init_method='env://')
world_rank = torch.distributed.get_rank()
local_rank = int(os.environ['LOCAL_RANK'])

train_path = '/global/cfs/cdirs/dasrepo/www/ai_ready_datasets/jetclass/data/train/'
train_dataset = JetClassDataset(train_path)
sampler = DistributedSampler(train_dataset)
train_dataloader = DataLoader(train_dataset,
                              batch_size=64,
                              num_workers=4,
                              sampler=sampler)

destroy_process_group()