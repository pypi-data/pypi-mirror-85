import cv2
import numpy as np

def nms(boxes, scores, score_thresh=0.5, nms_thresh=0.7):
    # boxes = [[left, top, right, bottom]]
    boxes_array = np.array(boxes)               # convert to x,y,w,h
    boxes_array[:, 2] -= boxes_array[:,0]
    boxes_array[:, 3] -= boxes_array[:, 1]
    bboxes = boxes_array.tolist()

    idxs = cv2.dnn.NMSBoxes(bboxes, scores,
                            score_threshold=score_thresh, nms_threshold=nms_thresh).flatten()
    return [boxes[i] for i in idxs], [scores[i] for i in idxs]