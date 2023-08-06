import torch
from ..utils.deeptext_utils import CTCLabelConverter, AttnLabelConverter
from .deeptext_model.model import Model
from KAI.utils.deeptext_utils import RawDataset, AlignCollate
import torch.nn.functional as F
import os

class TextRecognizer():
    def __int__(self, args):

        self.load_params(args)
        self.load_model()

    def load_params(self, args):
        self.args = args
        if 'CTC' in self.args['prediction']:
            self.converter = CTCLabelConverter(self.args['character'])
        else:
            self.converter = AttnLabelConverter(self.args['character'])
        self.args.update({'num_class' : len(self.converter.character)})
        checpoint_file = '%s-%s-%s-%s.pth' \
                     %(self.args['transformation'], self.args['featureextraction'],
                       self.args['sequencemodeling'],self.args['prediction'])

        self.model_path = os.path.join(self.args['text_recogizer_checkpoint_dir'], checpoint_file)

    def load_model(self):
        model = Model(self.args)
        self.model = torch.nn.DataParallel(model).to('cuda')
        self.model.load_state_dict(torch.load(self.model_path, map_location='cuda'))


    def predict_arrays(self, im_list, labels='unnamed'):

        AlignCollate_demo = AlignCollate(imgH=self.args['imgh'], imgW=self.args['imgw'],
                                         keep_ratio_with_pad=self.args['pad'])
        demo_data = RawDataset(im_list, self.args, labels)
        demo_loader = torch.utils.data.DataLoader(
            demo_data, batch_size=self.args['batch_size'],
            shuffle=False,
            num_workers=self.args['workers'],
            collate_fn=AlignCollate_demo, pin_memory=True)

        # predict
        self.model.eval()
        text_outs = []
        score_outs = []
        # with torch.no_grad():
        for image_tensors, image_path_list in demo_loader:
            batch_size = image_tensors.size(0)
            image = image_tensors.to('cuda')
            # For max length prediction
            length_for_pred = torch.IntTensor([self.args['batch_max_length']] * batch_size).to('cuda')
            text_for_pred = torch.LongTensor(batch_size, self.args['batch_max_length'] + 1).fill_(0).to('cuda')

            if 'CTC' in self.args['prediction']:
                preds = self.model(image, text_for_pred).log_softmax(2)

                # Select max probabilty (greedy decoding) then decode index to character
                preds_size = torch.IntTensor([preds.size(1)] * batch_size)
                _, preds_index = preds.max(2)
                preds_index = preds_index.view(-1)
                preds_str = self.converter.decode(preds_index.data, preds_size.data)

            else:
                preds = self.model(image, text_for_pred, is_train=False)

                # select max probabilty (greedy decoding) then decode index to character
                _, preds_index = preds.max(2)
                preds_str = self.converter.decode(preds_index, length_for_pred)

            if self.args['show_steps']:
                print('-' * 80)
                print('image_path \tpredict_label \t\tconfidence score')
                print('-' * 80)

            preds_prob = F.softmax(preds, dim=2)
            preds_max_prob, _ = preds_prob.max(dim=2)
            angles = [90, -90]
            for img_name, pred, pred_max_prob in zip(image_path_list, preds_str, preds_max_prob):

                if 'Attn' in self.args['prediction']:
                    pred_EOS = pred.find('[s]')
                    pred = pred[:pred_EOS]  # prune after "end of sentence" token ([s])
                    pred_max_prob = pred_max_prob[:pred_EOS]

                confidence_score = pred_max_prob.cumprod(dim=0)[-1]
                if self.args['show_steps']:
                    print('%s \t\t%s \t\t\t%.4f' % (img_name, pred, confidence_score))

                text_outs.append(pred)
                score_outs.append(float(confidence_score))



        return text_outs, score_outs








