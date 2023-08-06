"""
Copyright (c) 2019-present NAVER Corp.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import torch.nn as nn

from .transformation import TPS_SpatialTransformerNetwork
from .feature_extraction import VGG_FeatureExtractor, RCNN_FeatureExtractor, ResNet_FeatureExtractor
from .sequence_modeling import BidirectionalLSTM
from .prediction import Attention


class Model(nn.Module):

    def __init__(self, args):
        super(Model, self).__init__()
        self.args = args
        self.stages = {'Trans': args['transformation'], 'Feat': args['featureextraction'],
                       'Seq': args['sequencemodeling'], 'Pred': args['prediction']}

        """ Transformation """
        if args['transformation'] == 'TPS':
            self.Transformation = TPS_SpatialTransformerNetwork(
                F=args['num_fiducial'], I_size=(args['imgh'], args['imgw']),
                I_r_size=(args['imgh'], args['imgw']), I_channel_num=args['input_channel'])
        else:
            print('No Transformation module specified')

        """ FeatureExtraction """
        if args['featureextraction'] == 'VGG':
            self.FeatureExtraction = VGG_FeatureExtractor(args['input_channel'], args['output_channel'])
        elif args['featureextraction'] == 'RCNN':
            self.FeatureExtraction = RCNN_FeatureExtractor(args['input_channel'], args['output_channel'])
        elif args['featureextraction'] == 'ResNet':
            self.FeatureExtraction = ResNet_FeatureExtractor(args['input_channel'], args['output_channel'])
        else:
            raise Exception('No FeatureExtraction module specified')
        self.FeatureExtraction_output = args['output_channel']  # int(imgH/16-1) * 512
        self.AdaptiveAvgPool = nn.AdaptiveAvgPool2d((None, 1))  # Transform final (imgH/16-1) -> 1

        """ Sequence modeling"""
        if args['sequencemodeling'] == 'BiLSTM':
            self.SequenceModeling = nn.Sequential(
                BidirectionalLSTM(self.FeatureExtraction_output, args['hidden_size'], args['hidden_size']),
                BidirectionalLSTM(args['hidden_size'], args['hidden_size'], args['hidden_size']))
            self.SequenceModeling_output = args['hidden_size']
        else:
            print('No SequenceModeling module specified')
            self.SequenceModeling_output = self.FeatureExtraction_output

        """ Prediction """
        if args['prediction'] == 'CTC':
            self.Prediction = nn.Linear(self.SequenceModeling_output, args['num_class'])
        elif args['prediction'] == 'Attn':
            self.Prediction = Attention(self.SequenceModeling_output, args['hidden_size'], args['num_class'])
        else:
            raise Exception('Prediction is neither CTC or Attn')

    def forward(self, input, text, is_train=True):
        """ Transformation stage """
        if not self.stages['Trans'] == "None":
            input = self.Transformation(input)

        """ Feature extraction stage """
        visual_feature = self.FeatureExtraction(input)
        visual_feature = self.AdaptiveAvgPool(visual_feature.permute(0, 3, 1, 2))  # [b, c, h, w] -> [b, w, c, h]
        visual_feature = visual_feature.squeeze(3)

        """ Sequence modeling stage """
        if self.stages['Seq'] == 'BiLSTM':
            contextual_feature = self.SequenceModeling(visual_feature)
        else:
            contextual_feature = visual_feature  # for convenience. this is NOT contextually modeled by BiLSTM

        """ Prediction stage """
        if self.stages['Pred'] == 'CTC':
            prediction = self.Prediction(contextual_feature.contiguous())
        else:
            prediction = self.Prediction(contextual_feature.contiguous(), text, is_train, batch_max_length=self.args['batch_max_length'])

        return prediction
