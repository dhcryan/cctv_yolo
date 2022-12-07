import os
import sys
from PIL import Image
import torch
from torch import Tensor
import numpy as np
import torch.utils.data as data
import torchvision.transforms as transforms
import torchvision.datasets as datasets

data_list={'data_path': '/home/dhc4003/cctv_yolo/data_list/', 'train_list_path': '/home/dhc4003/cctv_yolo/data_list/foottraffic/FOOTTRAFFIC_train_list.txt', 'val_list_path': '/home/dhc4003/cctv_yolo/data_list/foottraffic/FOOTTRAFFIC_test_list.txt'}

def default_loader(path):
    return Image.open(path).convert('RGB')
class MultiLabelDataset(data.Dataset):
    def __init__(self, root, label, transform = None, loader = default_loader):
        images = []
        labels = open(label).readlines()
        for line in labels:
            items = line.split()
            img_name = items.pop(0) #이미지 이름
            if os.path.isfile(os.path.join(root, img_name)):
                cur_label = tuple([int(v) for v in items])#000100.....여기서 label들 말하는 거임
                images.append((img_name, cur_label))
#('foottraffic/ye_ma/2021-09-01_18-48-00_wed_sunny_out_ye-ma_CD0001_person_0_133.jpg', (0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0))
            else:
                print(os.path.join(root, img_name) + 'Not Found.')
        self.root = root
        self.images = images
        self.transform = transform
        self.loader = loader

    def __getitem__(self, index):
        img_name, label = self.images[index]
        # print(img_name,label)
        #img_name: foottraffic/ye_ma/2021-09-09_20-18-00_thu_sunny_out_ye-ma_CD0002_actor_29_502.jpg
        #label: (1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0)
        img = self.loader(os.path.join(self.root, img_name)) #image loader
        raw_img = img.copy()
        if self.transform is not None:
            img = self.transform(img)
        # print(img.shape) 3*256*128
        return img, torch.Tensor(label)
    
    def __len__(self):
        return len(self.images)
attr_nums = {}
attr_nums['foottraffic'] = 43
description = {}
description['foottraffic'] = ['male',
                        'female',
                        'child',
                        'teenager',
                        'adult',
                        'senior',
                        'long_sleeve',
                        'short_sleeve',
                        'sleeveless',
                        'onepice',
                        'top_red',
                        'top_orange',
                        'top_yellow',
                        'top_green',
                        'top_blue',
                        'top_purple',
                        'top_pink',
                        'top_brown',
                        'top_white',
                        'top_grey',
                        'top_black',
                        'long_pants',
                        'short_pants',
                        'skirt',
                        'bottom_type_none',
                        'bottom_red',
                        'bottom_orange',
                        'bottom_yellow',
                        'bottom_green',
                        'bottom_blue',
                        'bottom_purple',
                        'bottom_pink',
                        'bottom_brown',
                        'bottom_white',
                        'bottom_grey',
                        'bottom_black',
                        'carrier',
                        'umbrella',
                        'bag',
                        'hat',
                        'glasses',
                        'acc_none',
                        'pet']
#dataset 만들기
def Get_Dataset(experiment, approach):
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    transform_train = transforms.Compose([
        transforms.Resize(size=(256, 128)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        normalize
        ])
    transform_test = transforms.Compose([
        transforms.Resize(size=(256, 128)),
        transforms.ToTensor(),
        normalize
        ])
    if experiment=='foottraffic':
        train_dataset = MultiLabelDataset(root=data_list['data_path'],label=data_list['train_list_path'], transform=transform_train)
        val_dataset = MultiLabelDataset(root=data_list['data_path'],label=data_list['val_list_path'], transform=transform_test)
        return train_dataset, val_dataset, attr_nums['foottraffic'], description['foottraffic']
# Get_Dataset('foottraffic', data_list)