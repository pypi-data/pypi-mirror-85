from common.utils.proc_utils import *
import torch
import torchvision
import torch.utils.data
import cv2
from ikea.model.classification_models import Net
# from model import classification_models as models
import os
import torchvision.transforms as transforms
import configparser
from scipy.ndimage import rotate


class Classifier():
    def __int__(self, conf_path):
        config = configparser.RawConfigParser()
        config.read(conf_path)

        rgb_mean = tuple([float(l.strip()) for l in config.get('data', 'rgb_mean').split(',')])
        rgb_std = tuple([float(l.strip()) for l in config.get('data', 'rgb_std').split(',')])
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(rgb_mean, rgb_std)])
        self.classes = list([l.strip() for l in config.get('data', 'classes').split(',')])
        self.data_shape = tuple([int(l.strip()) for l in config.get('data', 'shape').split(',')])

        net_model = config.get('net', 'model')
        self.net = Net(net_model, input_shape=self.data_shape, num_classes=len(self.classes))

        net_path = config.get('net', 'path')
        self.net.load_state_dict(torch.load(net_path))

    def predict_array_single(self, im):

        im = fix_size(im, self.data_shape[:2])
        # cv2.imshow('scaled_im', im)
        im_tensor = self.transform(im)
        im_tensor = im_tensor.reshape((1,) + im_tensor.shape)
        outputs = self.net(im_tensor)
        _, predicted = torch.max(outputs, 1)
        probs = torch.softmax(outputs, 1)
        return self.classes[predicted[0]], probs[[0,predicted[0]]]

    def predict_list_array(self, im_list):

        num_im = len(im_list)
        inputs = None
        for im in im_list:
            im = fix_size(im, self.data_shape[:2])
            im_tensor = self.transform(im)
            im_tensor = im_tensor.reshape((1,) + im_tensor.shape)
            if inputs is None:
                inputs = im_tensor
            else:
                inputs = torch.cat((inputs, im_tensor), dim=0)

        outputs = self.net(inputs)
        _, predicted = torch.max(outputs, 1)

        out_classes = []
        for i in range(num_im):
            out_classes.append(self.classes[predicted[i]])

        return out_classes





