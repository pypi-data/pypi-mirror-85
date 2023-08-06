import torch.nn.functional as F
from torch.nn.parameter import Parameter
import numpy.random as npr
from collections import OrderedDict
import random
from torch.utils.data import Dataset
import torchvision.transforms as transforms
from torch.utils.data import sampler
import lmdb
import six
import sys
from PIL import Image
import numpy as np
import torch
import torch.nn as nn
from torch.autograd import Variable
import collections
import cv2
import os, shutil
from ttcv.basic.basic_objects import BasDetectObj


class MoranTextRecognizer():
    def get_model(self, checkpoint, alphabet):
        self.cuda_flag = False
        if torch.cuda.is_available():
            self.cuda_flag = True
            self.model = MORAN(1, len(alphabet.split(':')), 256, 32, 100, BidirDecoder=True, CUDA=self.cuda_flag)
            self.model = self.model.cuda()
        else:
            self.model = MORAN(1, len(alphabet.split(':')), 256, 32, 100, BidirDecoder=True,
                          inputDataType='torch.FloatTensor', CUDA=self.cuda_flag)
        # ----------- >>>> Load pretrained model
        if self.cuda_flag:
            state_dict = torch.load(checkpoint)
        else:
            state_dict = torch.load(checkpoint, map_location='cpu')
        MORAN_state_dict_rename = OrderedDict()
        for k, v in state_dict.items():
            name = k.replace("module.", "")  # remove `module.`
            MORAN_state_dict_rename[name] = v
        self.model.load_state_dict(MORAN_state_dict_rename)

        for p in self.model.parameters():
            p.requires_grad = False
        self.model.eval()

        self.converter = strLabelConverterForAttention(alphabet, ':')
        self.transformer = resizeNormalize((100, 32))

    def get_probs_string(self, preds_in, length, flip=False):
        preds = F.softmax(preds_in, dim=1)
        probs, preds = preds.max(1)
        probs = probs.cpu().numpy()

        sim_preds = self.converter.decode(preds.data, length.data)
        text_len = sim_preds.find('$')

        if not any(el.isdigit() for el in sim_preds):  # no digit in text
            sim_preds = ''
            text_len = 0

        if text_len == 0:
            return '', text_len, [],0.0

        sim_preds = sim_preds[:text_len]
        probs = np.abs(probs[:text_len])
        prob = probs.mean()

        if flip: return sim_preds[::-1], text_len, probs[::-1], prob
        return sim_preds, text_len, probs, prob


    def predict_arrays(self, im_in, label='unlabeled', text_baselen=6):

        im_list = [im_in, np.rot90(im_in, axes=(0, 1)), np.rot90(im_in, axes=(1, 0))]

        best_pred = None
        pred_ind = -1
        pred_prob = -1

        texts = []
        for i in range(3):
            image = Image.fromarray(im_list[i]).convert('L')
            image = self.transformer(image)

            if self.cuda_flag:
                image = image.cuda()
            image = image.view(1, *image.size())
            image = Variable(image)
            text = torch.LongTensor(1 * 5)
            length = torch.IntTensor(1)
            text = Variable(text)
            length = Variable(length)

            max_iter = 20
            t, l = self.converter.encode('0' * max_iter)
            loadData(text, t)
            loadData(length, l)
            output = self.model(image, length, text, text, test=True, debug=True)

            preds, preds_reverse = output[0]
            demo = output[1]

            sim_preds, text_len, probs, prob = self.get_probs_string(preds, length)
            sim_preds_reverse, text_len_reverse, probs_reverse, prob_reverse = self.get_probs_string(preds_reverse, length, flip=True)

            if max(text_len,text_len_reverse) == 0: continue

            len_diff = abs(text_len - text_len_reverse)
            len_avg = (text_len + text_len_reverse)/2
            alpha = (len_avg - len_diff) / len_avg
            if len_diff != 0:
                baselen_diff = abs(text_len - text_baselen)
                baselen_diff_reverse = abs(text_len_reverse - text_baselen)
                if baselen_diff < baselen_diff_reverse:
                    text1 = sim_preds
                    prob1 = prob*alpha
                elif baselen_diff > baselen_diff_reverse:
                    text1 = sim_preds_reverse
                    prob1 = prob_reverse*alpha

                if prob1 > pred_prob:
                    best_pred = text1
                    pred_prob = prob1
            else:
                new_preds = ''
                new_probs = []
                for prob, prob_r, sim, sim_r in zip(probs, probs_reverse, sim_preds, sim_preds_reverse):
                    if prob > prob_r:
                        new_preds += sim
                        new_probs.append(prob)
                    else:
                        new_preds += sim_r
                        new_probs.append(prob_r)
                prob1 = np.mean(np.array(new_probs))
                if prob1 > pred_prob:
                    best_pred = new_preds
                    pred_prob = prob1
        return best_pred

class MORAN(nn.Module):

    def __init__(self, nc, nclass, nh, targetH, targetW, BidirDecoder=False,
    	inputDataType='torch.cuda.FloatTensor', maxBatch=256, CUDA=True):
        super(MORAN, self).__init__()
        self.MORN = MORN(nc, targetH, targetW, inputDataType, maxBatch, CUDA)
        self.ASRN = ASRN(targetH, nc, nclass, nh, BidirDecoder, CUDA)

    def forward(self, x, length, text, text_rev, test=False, debug=False):
        if debug:
            x_rectified, demo = self.MORN(x, test, debug=debug)
            preds = self.ASRN(x_rectified, length, text, text_rev, test)
            return preds, demo
        else:
            x_rectified = self.MORN(x, test, debug=debug)
            preds = self.ASRN(x_rectified, length, text, text_rev, test)
            return preds




class MORN(nn.Module):
    def __init__(self, nc, targetH, targetW, inputDataType='torch.cuda.FloatTensor', maxBatch=256, CUDA=True):
        super(MORN, self).__init__()
        self.targetH = targetH
        self.targetW = targetW
        self.inputDataType = inputDataType
        self.maxBatch = maxBatch
        self.cuda = CUDA

        self.cnn = nn.Sequential(
            nn.MaxPool2d(2, 2),
            nn.Conv2d(nc, 64, 3, 1, 1), nn.BatchNorm2d(64), nn.ReLU(True), nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, 3, 1, 1), nn.BatchNorm2d(128), nn.ReLU(True), nn.MaxPool2d(2, 2),
            nn.Conv2d(128, 64, 3, 1, 1), nn.BatchNorm2d(64), nn.ReLU(True),
            nn.Conv2d(64, 16, 3, 1, 1), nn.BatchNorm2d(16), nn.ReLU(True),
            nn.Conv2d(16, 1, 3, 1, 1), nn.BatchNorm2d(1)
        )

        self.pool = nn.MaxPool2d(2, 1)

        h_list = np.arange(self.targetH) * 2. / (self.targetH - 1) - 1
        w_list = np.arange(self.targetW) * 2. / (self.targetW - 1) - 1

        grid = np.meshgrid(
            w_list,
            h_list,
            indexing='ij'
        )
        grid = np.stack(grid, axis=-1)
        grid = np.transpose(grid, (1, 0, 2))
        grid = np.expand_dims(grid, 0)
        grid = np.tile(grid, [maxBatch, 1, 1, 1])
        grid = torch.from_numpy(grid).type(self.inputDataType)
        if self.cuda:
            grid = grid.cuda()

        self.grid = Variable(grid, requires_grad=False)
        self.grid_x = self.grid[:, :, :, 0].unsqueeze(3)
        self.grid_y = self.grid[:, :, :, 1].unsqueeze(3)

    def forward(self, x, test, enhance=1, debug=False):

        if not test and np.random.random() > 0.5:
            return nn.functional.upsample(x, size=(self.targetH, self.targetW), mode='bilinear')
        if not test:
            enhance = 0

        assert x.size(0) <= self.maxBatch
        assert x.data.type() == self.inputDataType

        grid = self.grid[:x.size(0)]
        grid_x = self.grid_x[:x.size(0)]
        grid_y = self.grid_y[:x.size(0)]
        x_small = nn.functional.upsample(x, size=(self.targetH, self.targetW), mode='bilinear')

        offsets = self.cnn(x_small)
        offsets_posi = nn.functional.relu(offsets, inplace=False)
        offsets_nega = nn.functional.relu(-offsets, inplace=False)
        offsets_pool = self.pool(offsets_posi) - self.pool(offsets_nega)

        offsets_grid = nn.functional.grid_sample(offsets_pool, grid)
        offsets_grid = offsets_grid.permute(0, 2, 3, 1).contiguous()
        offsets_x = torch.cat([grid_x, grid_y + offsets_grid], 3)
        x_rectified = nn.functional.grid_sample(x, offsets_x)

        for iteration in range(enhance):
            offsets = self.cnn(x_rectified)

            offsets_posi = nn.functional.relu(offsets, inplace=False)
            offsets_nega = nn.functional.relu(-offsets, inplace=False)
            offsets_pool = self.pool(offsets_posi) - self.pool(offsets_nega)

            offsets_grid += nn.functional.grid_sample(offsets_pool, grid).permute(0, 2, 3, 1).contiguous()
            offsets_x = torch.cat([grid_x, grid_y + offsets_grid], 3)
            x_rectified = nn.functional.grid_sample(x, offsets_x)

        if debug:

            offsets_mean = torch.mean(offsets_grid.view(x.size(0), -1), 1)
            offsets_max, _ = torch.max(offsets_grid.view(x.size(0), -1), 1)
            offsets_min, _ = torch.min(offsets_grid.view(x.size(0), -1), 1)

            import matplotlib.pyplot as plt
            from colour import Color
            from torchvision import transforms
            import cv2

            alpha = 0.7
            density_range = 256
            color_map = np.empty([self.targetH, self.targetW, 3], dtype=int)
            cmap = plt.get_cmap("rainbow")
            blue = Color("blue")
            hex_colors = list(blue.range_to(Color("red"), density_range))
            rgb_colors = [[rgb * 255 for rgb in color.rgb] for color in hex_colors][::-1]
            to_pil_image = transforms.ToPILImage()

            for i in range(x.size(0)):

                img_small = x_small[i].data.cpu().mul_(0.5).add_(0.5)
                img = to_pil_image(img_small)
                img = np.array(img)
                if len(img.shape) == 2:
                    img = cv2.merge([img.copy()] * 3)
                img_copy = img.copy()

                v_max = offsets_max.data[i]
                v_min = offsets_min.data[i]
                img_offsets = (offsets_grid[i]).view(1, self.targetH, self.targetW).data.cpu().add_(-v_min).mul_(
                    1. / (v_max - v_min))
                img_offsets = to_pil_image(img_offsets)
                img_offsets = np.array(img_offsets)
                color_map = np.empty([self.targetH, self.targetW, 3], dtype=int)
                for h_i in range(self.targetH):
                    for w_i in range(self.targetW):
                        color_map[h_i][w_i] = rgb_colors[int(img_offsets[h_i, w_i] / 256. * density_range)]
                color_map = color_map.astype(np.uint8)
                cv2.addWeighted(color_map, alpha, img_copy, 1 - alpha, 0, img_copy)

                img_processed = x_rectified[i].data.cpu().mul_(0.5).add_(0.5)
                img_processed = to_pil_image(img_processed)
                img_processed = np.array(img_processed)
                if len(img_processed.shape) == 2:
                    img_processed = cv2.merge([img_processed.copy()] * 3)

                total_img = np.ones([self.targetH, self.targetW * 3 + 10, 3], dtype=int) * 255
                total_img[0:self.targetH, 0:self.targetW] = img
                total_img[0:self.targetH, self.targetW + 5:2 * self.targetW + 5] = img_copy
                total_img[0:self.targetH, self.targetW * 2 + 10:3 * self.targetW + 10] = img_processed
                total_img = cv2.resize(total_img.astype(np.uint8), (300, 50))
                # cv2.imshow("Input_Offsets_Output", total_img)
                # cv2.waitKey()

            return x_rectified, total_img

        return x_rectified


class BidirectionalLSTM(nn.Module):

    def __init__(self, nIn, nHidden, nOut):
        super(BidirectionalLSTM, self).__init__()

        self.rnn = nn.LSTM(nIn, nHidden, bidirectional=True, dropout=0.3)
        self.embedding = nn.Linear(nHidden * 2, nOut)

    def forward(self, input):
        recurrent, _ = self.rnn(input)
        T, b, h = recurrent.size()
        t_rec = recurrent.view(T * b, h)

        output = self.embedding(t_rec)  # [T * b, nOut]
        output = output.view(T, b, -1)

        return output


class AttentionCell(nn.Module):
    def __init__(self, input_size, hidden_size, num_embeddings=128, CUDA=True):
        super(AttentionCell, self).__init__()
        self.i2h = nn.Linear(input_size, hidden_size, bias=False)
        self.h2h = nn.Linear(hidden_size, hidden_size)
        self.score = nn.Linear(hidden_size, 1, bias=False)
        self.rnn = nn.GRUCell(input_size + num_embeddings, hidden_size)
        self.hidden_size = hidden_size
        self.input_size = input_size
        self.num_embeddings = num_embeddings
        self.fracPickup = fracPickup(CUDA=CUDA)

    def forward(self, prev_hidden, feats, cur_embeddings, test=False):
        nT = feats.size(0)
        nB = feats.size(1)
        nC = feats.size(2)
        hidden_size = self.hidden_size

        feats_proj = self.i2h(feats.view(-1, nC))
        prev_hidden_proj = self.h2h(prev_hidden).view(1, nB, hidden_size).expand(nT, nB, hidden_size).contiguous().view(
            -1, hidden_size)
        emition = self.score(F.tanh(feats_proj + prev_hidden_proj).view(-1, hidden_size)).view(nT, nB)

        alpha = F.softmax(emition, 0)  # nT * nB

        if not test:
            alpha_fp = self.fracPickup(alpha.transpose(0, 1).contiguous().unsqueeze(1).unsqueeze(2)).squeeze()
            context = (feats * alpha_fp.transpose(0, 1).contiguous().view(nT, nB, 1).expand(nT, nB, nC)).sum(0).squeeze(
                0)  # nB * nC
            if len(context.size()) == 1:
                context = context.unsqueeze(0)
            context = torch.cat([context, cur_embeddings], 1)
            cur_hidden = self.rnn(context, prev_hidden)
            return cur_hidden, alpha_fp
        else:
            context = (feats * alpha.view(nT, nB, 1).expand(nT, nB, nC)).sum(0).squeeze(0)  # nB * nC
            if len(context.size()) == 1:
                context = context.unsqueeze(0)
            context = torch.cat([context, cur_embeddings], 1)
            cur_hidden = self.rnn(context, prev_hidden)
            return cur_hidden, alpha


class Attention(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes, num_embeddings=128, CUDA=True):
        super(Attention, self).__init__()
        self.attention_cell = AttentionCell(input_size, hidden_size, num_embeddings, CUDA=CUDA)
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.generator = nn.Linear(hidden_size, num_classes)
        self.char_embeddings = Parameter(torch.randn(num_classes + 1, num_embeddings))
        self.num_embeddings = num_embeddings
        self.num_classes = num_classes
        self.cuda = CUDA

    # targets is nT * nB
    def forward(self, feats, text_length, text, test=False):

        nT = feats.size(0)
        nB = feats.size(1)
        nC = feats.size(2)
        hidden_size = self.hidden_size
        input_size = self.input_size
        assert (input_size == nC)
        assert (nB == text_length.numel())

        num_steps = text_length.data.max()
        num_labels = text_length.data.sum()

        if not test:

            targets = torch.zeros(nB, num_steps + 1).long()
            if self.cuda:
                targets = targets.cuda()
            start_id = 0

            for i in range(nB):
                targets[i][1:1 + text_length.data[i]] = text.data[start_id:start_id + text_length.data[i]] + 1
                start_id = start_id + text_length.data[i]
            targets = Variable(targets.transpose(0, 1).contiguous())

            output_hiddens = Variable(torch.zeros(num_steps, nB, hidden_size).type_as(feats.data))
            hidden = Variable(torch.zeros(nB, hidden_size).type_as(feats.data))

            for i in range(num_steps):
                cur_embeddings = self.char_embeddings.index_select(0, targets[i])
                hidden, alpha = self.attention_cell(hidden, feats, cur_embeddings, test)
                output_hiddens[i] = hidden

            new_hiddens = Variable(torch.zeros(num_labels, hidden_size).type_as(feats.data))
            b = 0
            start = 0

            for length in text_length.data:
                new_hiddens[start:start + length] = output_hiddens[0:length, b, :]
                start = start + length
                b = b + 1

            probs = self.generator(new_hiddens)
            return probs

        else:

            hidden = Variable(torch.zeros(nB, hidden_size).type_as(feats.data))
            targets_temp = Variable(torch.zeros(nB).long().contiguous())
            probs = Variable(torch.zeros(nB * num_steps, self.num_classes))
            if self.cuda:
                targets_temp = targets_temp.cuda()
                probs = probs.cuda()

            for i in range(num_steps):
                cur_embeddings = self.char_embeddings.index_select(0, targets_temp)
                hidden, alpha = self.attention_cell(hidden, feats, cur_embeddings, test)
                hidden2class = self.generator(hidden)
                probs[i * nB:(i + 1) * nB] = hidden2class
                _, targets_temp = hidden2class.max(1)
                targets_temp += 1

            probs = probs.view(num_steps, nB, self.num_classes).permute(1, 0, 2).contiguous()
            probs = probs.view(-1, self.num_classes).contiguous()
            probs_res = Variable(torch.zeros(num_labels, self.num_classes).type_as(feats.data))
            b = 0
            start = 0

            for length in text_length.data:
                probs_res[start:start + length] = probs[b * num_steps:b * num_steps + length]
                start = start + length
                b = b + 1

            return probs_res


class Residual_block(nn.Module):
    def __init__(self, c_in, c_out, stride):
        super(Residual_block, self).__init__()
        self.downsample = None
        flag = False
        if isinstance(stride, tuple):
            if stride[0] > 1:
                self.downsample = nn.Sequential(nn.Conv2d(c_in, c_out, 3, stride, 1),
                                                nn.BatchNorm2d(c_out, momentum=0.01))
                flag = True
        else:
            if stride > 1:
                self.downsample = nn.Sequential(nn.Conv2d(c_in, c_out, 3, stride, 1),
                                                nn.BatchNorm2d(c_out, momentum=0.01))
                flag = True
        if flag:
            self.conv1 = nn.Sequential(nn.Conv2d(c_in, c_out, 3, stride, 1),
                                       nn.BatchNorm2d(c_out, momentum=0.01))
        else:
            self.conv1 = nn.Sequential(nn.Conv2d(c_in, c_out, 1, stride, 0),
                                       nn.BatchNorm2d(c_out, momentum=0.01))
        self.conv2 = nn.Sequential(nn.Conv2d(c_out, c_out, 3, 1, 1),
                                   nn.BatchNorm2d(c_out, momentum=0.01))
        self.relu = nn.ReLU()

    def forward(self, x):
        residual = x
        conv1 = self.conv1(x)
        conv2 = self.conv2(conv1)
        if self.downsample is not None:
            residual = self.downsample(residual)
        return self.relu(residual + conv2)


class ResNet(nn.Module):
    def __init__(self, c_in):
        super(ResNet, self).__init__()
        self.block0 = nn.Sequential(nn.Conv2d(c_in, 32, 3, 1, 1), nn.BatchNorm2d(32, momentum=0.01))
        self.block1 = self._make_layer(32, 32, 2, 3)
        self.block2 = self._make_layer(32, 64, 2, 4)
        self.block3 = self._make_layer(64, 128, (2, 1), 6)
        self.block4 = self._make_layer(128, 256, (2, 1), 6)
        self.block5 = self._make_layer(256, 512, (2, 1), 3)

    def _make_layer(self, c_in, c_out, stride, repeat=3):
        layers = []
        layers.append(Residual_block(c_in, c_out, stride))
        for i in range(repeat - 1):
            layers.append(Residual_block(c_out, c_out, 1))
        return nn.Sequential(*layers)

    def forward(self, x):
        block0 = self.block0(x)
        block1 = self.block1(block0)
        block2 = self.block2(block1)
        block3 = self.block3(block2)
        block4 = self.block4(block3)
        block5 = self.block5(block4)
        return block5


class ASRN(nn.Module):

    def __init__(self, imgH, nc, nclass, nh, BidirDecoder=False, CUDA=True):
        super(ASRN, self).__init__()
        assert imgH % 16 == 0, 'imgH must be a multiple of 16'

        self.cnn = ResNet(nc)

        self.rnn = nn.Sequential(
            BidirectionalLSTM(512, nh, nh),
            BidirectionalLSTM(nh, nh, nh),
        )

        self.BidirDecoder = BidirDecoder
        if self.BidirDecoder:
            self.attentionL2R = Attention(nh, nh, nclass, 256, CUDA=CUDA)
            self.attentionR2L = Attention(nh, nh, nclass, 256, CUDA=CUDA)
        else:
            self.attention = Attention(nh, nh, nclass, 256, CUDA=CUDA)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal(m.weight, mode='fan_out', a=0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant(m.weight, 1)
                nn.init.constant(m.bias, 0)

    def forward(self, input, length, text, text_rev, test=False):
        # conv features
        conv = self.cnn(input)

        b, c, h, w = conv.size()
        assert h == 1, "the height of conv must be 1"
        conv = conv.squeeze(2)
        conv = conv.permute(2, 0, 1).contiguous()  # [w, b, c]

        # rnn features
        rnn = self.rnn(conv)

        if self.BidirDecoder:
            outputL2R = self.attentionL2R(rnn, length, text, test)
            outputR2L = self.attentionR2L(rnn, length, text_rev, test)
            return outputL2R, outputR2L
        else:
            output = self.attention(rnn, length, text, test)
            return output


class fracPickup(nn.Module):

    def __init__(self, CUDA=True):
        super(fracPickup, self).__init__()
        self.cuda = CUDA

    def forward(self, x):
        x_shape = x.size()
        assert len(x_shape) == 4
        assert x_shape[2] == 1

        fracPickup_num = 1

        h_list = 1.
        w_list = np.arange(x_shape[3]) * 2. / (x_shape[3] - 1) - 1
        for i in range(fracPickup_num):
            idx = int(npr.rand() * len(w_list))
            if idx <= 0 or idx >= x_shape[3] - 1:
                continue
            beta = npr.rand() / 4.
            value0 = (beta * w_list[idx] + (1 - beta) * w_list[idx - 1])
            value1 = (beta * w_list[idx - 1] + (1 - beta) * w_list[idx])
            w_list[idx - 1] = value0
            w_list[idx] = value1

        grid = np.meshgrid(
            w_list,
            h_list,
            indexing='ij'
        )
        grid = np.stack(grid, axis=-1)
        grid = np.transpose(grid, (1, 0, 2))
        grid = np.expand_dims(grid, 0)
        grid = np.tile(grid, [x_shape[0], 1, 1, 1])
        grid = torch.from_numpy(grid).type(x.data.type())
        if self.cuda:
            grid = grid.cuda()
        self.grid = Variable(grid, requires_grad=False)

        x_offset = nn.functional.grid_sample(x, self.grid)

        return x_offset

class strLabelConverterForAttention(object):
    """Convert between str and label.

    NOTE:
        Insert `EOS` to the alphabet for attention.

    Args:
        alphabet (str): set of the possible characters.
        ignore_case (bool, default=True): whether or not to ignore all of the case.
    """

    def __init__(self, alphabet, sep):
        self._scanned_list = False
        self._out_of_list = ''
        self._ignore_case = True
        self.sep = sep
        self.alphabet = alphabet.split(sep)

        self.dict = {}
        for i, item in enumerate(self.alphabet):
            self.dict[item] = i

    def scan(self, text):
        # print(text)
        text_tmp = text
        text = []
        for i in range(len(text_tmp)):
            text_result = ''
            for j in range(len(text_tmp[i])):
                chara = text_tmp[i][j].lower() if self._ignore_case else text_tmp[i][j]
                if chara not in self.alphabet:
                    if chara in self._out_of_list:
                        continue
                    else:
                        self._out_of_list += chara
                        file_out_of_list = open("out_of_list.txt", "a+")
                        file_out_of_list.write(chara + "\n")
                        file_out_of_list.close()
                        print('" %s " is not in alphabet...' % chara)
                        continue
                else:
                    text_result += chara
            text.append(text_result)
        text_result = tuple(text)
        self._scanned_list = True
        return text_result

    def encode(self, text, scanned=True):
        """Support batch or single str.

        Args:
            text (str or list of str): texts to convert.

        Returns:
            torch.IntTensor [length_0 + length_1 + ... length_{n - 1}]: encoded texts.
            torch.IntTensor [n]: length of each text.
        """
        self._scanned_list = scanned
        if not self._scanned_list:
            text = self.scan(text)

        if isinstance(text, str):
            text = [
                self.dict[char.lower() if self._ignore_case else char]
                for char in text
            ]
            length = [len(text)]
        elif isinstance(text, collections.Iterable):
            length = [len(s) for s in text]
            text = ''.join(text)
            text, _ = self.encode(text)
        return (torch.LongTensor(text), torch.LongTensor(length))

    def decode(self, t, length):
        """Decode encoded texts back into strs.

        Args:
            torch.IntTensor [length_0 + length_1 + ... length_{n - 1}]: encoded texts.
            torch.IntTensor [n]: length of each text.

        Raises:
            AssertionError: when the texts and its length does not match.

        Returns:
            text (str or list of str): texts to convert.
        """
        if length.numel() == 1:
            length = length[0]
            assert t.numel() == length, "text with length: {} does not match declared length: {}".format(t.numel(), length)
            return ''.join([self.alphabet[i] for i in t])
        else:
            # batch mode
            assert t.numel() == length.sum(), "texts with length: {} does not match declared length: {}".format(t.numel(), length.sum())
            texts = []
            index = 0
            for i in range(length.numel()):
                l = length[i]
                texts.append(
                    self.decode(
                        t[index:index + l], torch.LongTensor([l])))
                index += l
            return texts

class averager(object):
    """Compute average for `torch.Variable` and `torch.Tensor`. """

    def __init__(self):
        self.reset()

    def add(self, v):
        if isinstance(v, Variable):
            count = v.data.numel()
            v = v.data.sum()
        elif isinstance(v, torch.Tensor):
            count = v.numel()
            v = v.sum()

        self.n_count += count
        self.sum += v

    def reset(self):
        self.n_count = 0
        self.sum = 0

    def val(self):
        res = 0
        if self.n_count != 0:
            res = self.sum / float(self.n_count)
        return res

def loadData(v, data):
    major, _ = get_torch_version()

    if major >= 1:
        v.resize_(data.size()).copy_(data)
    else:
        v.data.resize_(data.size()).copy_(data)

def get_torch_version():
    """
    Find pytorch version and return it as integers
    for major and minor versions
    """
    torch_version = str(torch.__version__).split(".")
    return int(torch_version[0]), int(torch_version[1])


class lmdbDataset(Dataset):

    def __init__(self, root=None, transform=None, reverse=False, alphabet='0123456789abcdefghijklmnopqrstuvwxyz'):
        self.env = lmdb.open(
            root,
            max_readers=1,
            readonly=True,
            lock=False,
            readahead=False,
            meminit=False)

        if not self.env:
            print('cannot creat lmdb from %s' % (root))
            sys.exit(0)

        with self.env.begin(write=False) as txn:
            nSamples = int(txn.get('num-samples'.encode()))
            self.nSamples = nSamples

        self.transform = transform
        self.alphabet = alphabet
        self.reverse = reverse

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'
        index += 1
        with self.env.begin(write=False) as txn:
            img_key = 'image-%09d' % index
            imgbuf = txn.get(img_key.encode())

            buf = six.BytesIO()
            buf.write(imgbuf)
            buf.seek(0)
            try:
                img = Image.open(buf).convert('L')
            except IOError:
                print('Corrupted image for %d' % index)
                return self[index + 1]

            label_key = 'label-%09d' % index
            label = str(txn.get(label_key.encode()).decode('utf-8'))

            label = ''.join(label[i] if label[i].lower() in self.alphabet else ''
                            for i in range(len(label)))
            if len(label) <= 0:
                return self[index + 1]
            if self.reverse:
                label_rev = label[-1::-1]
                label_rev += '$'
            label += '$'

            if self.transform is not None:
                img = self.transform(img)

        if self.reverse:
            return (img, label, label_rev)
        else:
            return (img, label)


class resizeNormalize(object):

    def __init__(self, size, interpolation=Image.BILINEAR):
        self.size = size
        self.interpolation = interpolation
        self.toTensor = transforms.ToTensor()

    def __call__(self, img):
        img = img.resize(self.size, self.interpolation)
        img = self.toTensor(img)
        img.sub_(0.5).div_(0.5)
        return img


class randomSequentialSampler(sampler.Sampler):

    def __init__(self, data_source, batch_size):
        self.num_samples = len(data_source)
        self.batch_size = batch_size

    def __len__(self):
        return self.num_samples

    def __iter__(self):
        n_batch = len(self) // self.batch_size
        tail = len(self) % self.batch_size
        index = torch.LongTensor(len(self)).fill_(0)
        for i in range(n_batch):
            random_start = random.randint(0, len(self) - self.batch_size)
            batch_index = random_start + torch.arange(0, self.batch_size)
            index[i * self.batch_size:(i + 1) * self.batch_size] = batch_index
        # deal with tail
        if tail:
            random_start = random.randint(0, len(self) - self.batch_size)
            tail_index = random_start + torch.arange(0, tail)
            index[(i + 1) * self.batch_size:] = tail_index

        return iter(index)





