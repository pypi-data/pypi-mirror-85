from mmdet.apis import init_detector, inference_detector, show_result
import mmcv
import numpy as np
import pycocotools.mask as maskUtils
from time import time
import configparser
import cv2
from libs.utils.proc_utils import get_color, correct_workspace
from libs.basic.basic_objects import BasDetectObj

class MaskRCNNDetector(BasDetectObj):

    def get_model(self):
        self.model = init_detector(self.args['config_file'], self.args['checkpoint_file'], device='cuda:0')

    def predict_array(self, inputs):
        t = time()
        print('---------------------------->>>>>>>>>> Mask RCNN detection')

        self.crop_rect = correct_workspace(inputs['im'].shape[:2], self.args['crop_rect'], self.args['crop_im'])
        # self.crop_rect = self.args['crop_rect']

        crop_im =inputs['im'][self.crop_rect[0]:self.crop_rect[2], self.crop_rect[1]:self.crop_rect[3], :]
        boxes_list, masks_list = inference_detector(self.model, inputs['im'][self.crop_rect[0]:self.crop_rect[2], self.crop_rect[1]:self.crop_rect[3], :])

        num_boxes = 0
        for i, cls in enumerate(self.args['classes']):
            boxes = boxes_list[i]
            masks = masks_list[i]
            if len(boxes) == 0: continue
            num_boxes += len(boxes)
            new_masks = []
            # new_boxes = []
            for j in range(len(boxes)):
                mask = 255*maskUtils.decode(masks[j]).astype(np.uint8)
                left, top, right, bottom = boxes[j,:4].astype('int')

                new_masks.append(mask[top:bottom, left:right])
                boxes[j, :4] = left + self.crop_rect[1], top + self.crop_rect[0], right + self.crop_rect[1], bottom + self.crop_rect[0]

            boxes_list[i] = boxes
            masks_list[i] = new_masks

        print('Detected %d objects in %.3f s' % (num_boxes, (time() - t)))
        return {'boxes':boxes_list, 'masks':masks_list}

    def show_detect_results(self, im, detect_rets):
        boxes_list = detect_rets['boxes']
        masks_list = detect_rets['masks']
        out = np.copy(im)
        obj_ind = 0
        for j, cls in  enumerate(self.args['classes']):
            boxes = boxes_list[j]
            num_boxes = len(boxes)
            if num_boxes == 0 or cls == '__background__': continue
            masks = masks_list[j]

            for box, mask in zip(boxes, masks):
                color = get_color(obj_ind)

                left, top, right, bottom, prob = box
                left, top, right, bottom = int(left), int(top), int(right), int(bottom)

                Y, X = np.where(mask==255)
                Y += top
                X += left
                loc = (Y,X)

                out[loc] = 0.8 * out[loc] + tuple(0.2 * np.array(color))
                cv2.rectangle(out, (left, top), (right, bottom), color, 2)
                cv2.putText(out, '%s: %.2f' %(cls, prob), (left, top-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)

                obj_ind += 1
        return out







