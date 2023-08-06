from processing.proc_utils import fix_size
import numpy as np
from keras.models import load_model
import cv2
from glob import glob
import os, random


def make_test_pairs(test_im_in, support_ims_array, test_scale=(105, 105)):
    num_support_im = support_ims_array.shape[0]

    test_im = fix_size(test_im_in, test_scale)
    test_im = test_im.reshape((1, ) + test_im.shape + (1,))
    test_ims_array = np.tile(test_im, (num_support_im,1,1,1))

    return [test_ims_array, support_ims_array]


def make_support_set( support_set_dir, test_scale=(105, 105)):
    all_support_subset_dir = glob(os.path.join(support_set_dir, '*'))
    num_chr = len(all_support_subset_dir)
    support_ims = []
    for support_subset in all_support_subset_dir:
        all_support_im = glob(os.path.join(support_subset, '*'))
        num_support_im = len(all_support_im)
        support_im_ind = random.randint(0, num_support_im - 1)
        support_im = fix_size(cv2.imread(all_support_im[support_im_ind], 0), test_scale)

        support_ims.append(support_im.reshape((1,) + support_im.shape))

    support_ims_array = np.vstack(support_ims)
    support_ims_array = support_ims_array.reshape(support_ims_array.shape + (1,))

    return support_ims_array


class SiameseDetector():
    def __int__(self, support_set_dir, test_scale):
        self.model = load_model('../detector/siamese_keras/weights.h5')
        self.test_scale = test_scale
        self.support_set = make_support_set(support_set_dir, self.test_scale)


    def predict_array(self, im):
        print('---------------------------->>>>>>>>>> Siamese detection')
        pairs = make_test_pairs(im, self.support_set, self.test_scale)

        p = self.model.predict(pairs)
        max_ind = int(np.argmax(np.array(p)))
        target = self.support_set[max_ind][:, :, 0]
        target = fix_size(target, im.shape)

        return target, p

    def show_detect_results(self, im, target):
        out = np.concatenate((im, target))
        return out







