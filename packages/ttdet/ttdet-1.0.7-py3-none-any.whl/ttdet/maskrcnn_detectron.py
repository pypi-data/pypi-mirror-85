from libs.import_basic_utils import *
from libs.basic.basic_objects import BasDetectObj
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
import cv2
from detectron2.utils.visualizer import Visualizer
from detectron2.data import DatasetCatalog, MetadataCatalog
import numpy as np

class MaskRCNNDetectron(BasDetectObj):
    def get_model(self):
        cfg = get_cfg()
        cfg.merge_from_file(model_zoo.get_config_file(self.args.merge_from_file))
        cfg.DATASETS.TEST = self.args.test_dataset
        cfg.DATALOADER.NUM_WORKERS = self.args.num_workers
        cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = self.args.batch_size_per_image
        cfg.MODEL.ROI_HEADS.NUM_CLASSES = self.args.num_classes  # only has one class (ballon)
        cfg.MODEL.ANCHOR_GENERATOR.SIZES = self.args.anchor_sizes
        cfg.MODEL.WEIGHTS = self.args.checkpoint
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.args.score_thresh_test

        self.detector = DefaultPredictor(cfg)

    def predict_array(self, anArray, workspace=None):
        height, width = anArray.shape[:2]
        if workspace is None:
            ret = self.detector(anArray)["instances"].to("cpu")
            boxes = ret.pred_boxes.tensor.numpy()
            masks = ret.pred_masks.numpy().astype('uint8')
            classes = ret.pred_classes.numpy()
            scores = ret.scores.numpy()

            return {'boxes': boxes, 'masks': masks, 'classes':classes, 'scores': scores}

        if workspace is not None:
            array_crop = anArray[workspace.rect.top: workspace.rect.bottom, workspace.rect.left:workspace.rect.right, :]
            ret = self.predict_array(array_crop)

            num_detected= len(ret)
            if num_detected==0: return  ret

            ret['boxes'][0] +=  workspace.rect.left
            ret['boxes'][2] += workspace.rect.left
            ret['boxes'][1] += workspace.rect.top
            ret['boxes'][3] += workspace.rect.top

            right = width-workspace.rect.right
            bottom = height-workspace.rect.bottom

            new_masks = []
            for i in range(num_detected):
                mask = ret['masks'][i, :,:]
                mask = cv2.copyMakeBorder(mask,workspace.rect.top, bottom,workspace.rect.left, right, cv2.BORDER_CONSTANT, value=0)
                new_masks.append(mask)

            ret['mask'] = np.vstack(new_masks)

            return ret






    def show_detect_results(self, im, detect_rets):
        boxes = detect_rets['boxes']
        masks = detect_rets['masks']
        classes = detect_rets['classes']
        scores = detect_rets['scores']
        out = np.copy(im)
        obj_ind = 0
        num_detected = boxes.shape[0]
        if num_detected==0: return im

        for i in range(num_detected):
            cls = classes[i]
            score = scores[i]
            if cls == '__background__': continue
            box = boxes[i,:].astype('int')
            mask = masks[i, :,:]

            color = ProcUtils().get_color(obj_ind)

            left, top, right, bottom = box

            loc = np.where(mask)

            out[loc] = 0.8 * out[loc] + tuple(0.2 * np.array(color))
            cv2.rectangle(out, (left, top), (right, bottom), color, 2)
            cv2.putText(out, '%s: %d' %(cls, int(100*score)), (left, top-3), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)

            obj_ind += 1

        return out



    def visualize_ret(self, rgb, ret):


        for d in ["val"]:
            # DatasetCatalog.register("prop_" + d, lambda d=d: get_dicts("prop/" + d))
            MetadataCatalog.get("prop_" + d).set(thing_classes=["prop"])
        prop_metadata = MetadataCatalog.get("prop_train")

        v = Visualizer(rgb,
                       metadata=prop_metadata,
                       scale=0.8
                       # instance_mode=ColorMode.IMAGE_BW  # remove the colors of unsegmented pixels
                       )
        # print(outputs["instances"])
        v = v.draw_instance_predictions(ret)
        print(ret.pred_classes)
        print(ret.pred_boxes)
        return v.get_image()[:,:,::-1]
