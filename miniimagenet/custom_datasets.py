from __future__ import print_function
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from torch.autograd import Variable
import os
# import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import scipy as sp
# import sklearn as skl
import pickle

import torch.utils.data as data
from PIL import Image
import os
import os.path
import errno
import torch
import codecs
import random

import util

class RandomCIFAR10(data.Dataset):

    def __init__(self, data_dir, train=False, transform=None, target_transform=None, download=False):
        self.transform = transform
        self.target_transform = target_transform


    def __getitem__(self, index):
        img = torch.randn(3, 32, 32)
        target = random.randint(0,9)
        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        #img = Image.fromarray(img.numpy(), mode='L')

        #if self.transform is not None:
        #    img = self.transform(img)

        #if self.target_transform is not None:
        #    target = self.target_transform(target)

        return img, target

    def __len__(self):
        return 1000

class Noisy_Data(data.Dataset):
    # Add Normal Noise to Training Data
    def __init__(self, transform=None, target_transform=None, filename="adv_set_e_2.p", transp = False):
        """

        :param transform:
        :param target_transform:
        :param filename:
        :param transp: Set shuff= False for PGD based attacks
        :return:
        """
        self.transform = transform
        self.target_transform = target_transform
        self.adv_dict=pickle.load(open(filename,"rb"))
        self.adv_flat=self.adv_dict["adv_input"]
        self.num_adv=np.shape(self.adv_flat)[0]
        self.shuff = transp
        self.sample_num = 0

    def __getitem__(self, index):

        img=self.adv_flat[self.sample_num,:]

        if(self.shuff == False):
            # shuff is true for non-pgd attacks
            img = torch.from_numpy(np.reshape(img,(3,32,32)))
        else:
            img = torch.from_numpy(img).type(torch.FloatTensor)
        target = np.argmax(self.adv_dict["adv_labels"],axis=1)[self.sample_num]
        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        self.sample_num = self.sample_num + 1
        return img, target

    def __len__(self):

        return 1328

class Adv(data.Dataset):

    def __init__(self, transform=None, target_transform=None, filename="adv_set_e_2.p", transp = False):
        """

        :param transform:
        :param target_transform:
        :param filename:
        :param transp: Set shuff= False for PGD based attacks
        :return:
        """
        self.transform = transform
        self.target_transform = target_transform
        self.adv_dict={}
        self.adv_dict["adv_input"]=None
        self.adv_dict["adv_labels"]= None

        for i in range(16):
            if("Test" in filename):
                print('OK')
                new_adv_dict=pickle.load(open(filename.split(".")[0]+str(i)+"."+filename.split(".")[1],"rb"))
            else:
                new_adv_dict=pickle.load(open(filename.split(".")[0]+"_"+str(i)+"."+filename.split(".")[1],"rb"))

            if(self.adv_dict["adv_input"] is None):
                self.adv_dict["adv_input"] = (new_adv_dict["adv_input"])
                self.adv_dict["adv_labels"] = (new_adv_dict["adv_labels"])
            else:
                 self.adv_dict["adv_input"] = np.concatenate((new_adv_dict["adv_input"],self.adv_dict["adv_input"]))
                 self.adv_dict["adv_labels"] = np.concatenate((new_adv_dict["adv_labels"],self.adv_dict["adv_labels"]))

        self.adv_flat=self.adv_dict["adv_input"]
        self.num_adv=np.shape(self.adv_flat)[0]
        self.shuff = transp
        self.sample_num = 0

    def __getitem__(self, index):

        img=self.adv_flat[self.sample_num,:]

        if(self.shuff == False):
            # shuff is true for non-pgd attacks
            img = torch.from_numpy(np.reshape(img,(3,224,224)))
        else:
            img = torch.from_numpy(img).type(torch.FloatTensor)
        target = self.adv_dict["adv_labels"][self.sample_num]
        # doing this so that it is consistent with all other datasets
        # to return a PIL Image
        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            target = self.target_transform(target)

        self.sample_num = self.sample_num + 1
        return img, target

    def __len__(self):

        return 1328
