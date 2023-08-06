from mmdet.apis import init_detector, inference_detector, show_result
import mmcv
import numpy as np
import pycocotools.mask as maskUtils
from time import time
import configparser
import cv2
from ttcv.import_basic_utils import *
from ttcv.basic.basic_objects import BasDetectObj

class FasterRCNNDetector():
    def get_model(self, config_file, checkpoint_file):
        self.model = init_detector(config_file, checkpoint_file, device='cuda:0')

    def predict_array(self, anArray, need_rot=False, test_shape=None):
        h,w = anArray.shape[:2]
        if need_rot: im = np.rot90(anArray, k=-1)           # 90 rot
        else: im = anArray

        need_reshape = (test_shape is not None)
        if need_reshape:
            h1, w1 = im.shape[:2]
            im = cv2.resize(im, test_shape, interpolation=cv2.INTER_CUBIC)
            h2, w2 = im.shape[:2]
            fx, fy = w1/w2, h1/h2       # restore ratios

        boxes_list=inference_detector(self.model, im)

        if need_reshape:                # unscale
            for boxes in boxes_list:
                for box in boxes:
                    box[[0,2]] *= fx
                    box[[1, 3]] *= fy


        if need_rot:
            new_boxes_list = []
            for boxes in boxes_list:
                if len(boxes) ==0:
                    new_boxes_list.append(boxes)
                    continue
                new_boxes = []
                for box in boxes:
                    box = box[[1,2,3,0,4]]
                    box[1] = h-box[1]
                    box[3] = h - box[3]
                    new_boxes.append(box)
                new_boxes_list.append(new_boxes)
        else: new_boxes_list = boxes_list

        return new_boxes_list











