from libs.dataset.polygon import *
from libs.dataset.cifar10 import Cifar10Maker, CombineCifar10Data
from libs.dataset.polygon import OnMousePolygonDrawer, PolygonShower, PolygonAnalyzer
from libs.import_basic_utils import *
import json
import numpy as np
import math

class GripCifar10DMaker(Cifar10Maker):
    def load_params(self, args):
        super().load_params(args=args)
        self.ann_poly = os.path.join(self.args.root_dir, self.args.ann_poly)
        assert ProcUtils().isexists(self.ann_poly)

    def process_single(self):
    # def process_single(self):
        # read polygon from json
        json_path = os.path.join(self.ann_poly,self.filename+'.json')
        assert ProcUtils().isexists(json_path)
        json_file = open(json_path)
        ann_dict = json.load(json_file)
        json_file.close()
        classes = ann_dict['Classes']
        polygons = ann_dict['Polygons']

        # pad
        h,w = self.rgbd.height, self.rgbd.width
        diag = int(np.linalg.norm((h,w)))
        top, left = int((diag-h)/2), int((diag-w)/2)
        bottom, right = diag-h-top, diag-w-left
        center = (int(diag/2), int(diag/2))

        rgbd_pad =  self.rgbd.pad(top=top, left=left, bottom=bottom, right=right)

        count = 0
        for cls, poly in zip(classes, polygons):
            pt1, pt2, = poly[:2]
            x1, y1 = pt1
            x2, y2 = pt2
            if self.args.show_steps: self.rgbd.show(title='rgbd', args=self.args, grips=GRIPS(grips=[GRIP(pts=[(x1,y1),(x2,y2)])]))

            # compute angle
            dx, dy = pt1[0] - pt2[0], pt1[1] - pt2[1]
            angle = math.atan(dy/(dx+0.000001)) * 180 /math.pi

            # totate
            rgbd_rot = rgbd_pad.rotate(angle=angle)

            # new pt (y1=y2)
            x1, y1 = x1+left, y1+top
            x1,y1 = ProcUtils().rotateXY(x1,y1, -angle, org=center)
            x2, y2 = x2 + left, y2 + top
            x2, y2 = ProcUtils().rotateXY(x2, y2, -angle, org=center)
            if self.args.show_steps:
                rgbd_rot.show(title='rgbd_rot',args=self.args, grips=GRIPS(grips=[GRIP(pts=[(x1,y1),(x2,y2)])]))

            xmin, xmax = min(x1, x2), max(x1, x2)
            # crop
            grip_hs, grip_w_margins =self.args.train_grip_hs, self.args.train_grip_w_margins
            # if cls=='ungrip' and self.filename not in self.args.feedback_images:
            #     grip_hs, grip_w_margins = self.args.ungrip_hs, self.args.ungrip_w_margins

            for grip_h in grip_hs:
                for grip_w_margin in grip_w_margins:
                    count += 1
                    r = int(grip_h/2)
                    rgbd_crop=rgbd_rot.crop(left=xmin-grip_w_margin, top=y1-r, right=xmax+1+grip_w_margin, bottom=y1+r+1)

                    if self.args.show_steps:
                        rgbd_crop.show(title='rgbd_crop',args=self.args)

                    self.cls_ind = self.args.classes.index(cls)
                    super().process_single(rgbd=rgbd_crop)
        print('>>> %d samples ...' % count)

class OnMouseDrawGrip(OnMousePolygonDrawer):

    def show_draws(self, rgbd):
        grips = [GRIP(pts=poly[:2]) for poly in self.polygons]
        Grips = GRIPS(grips=grips, disp_colors=self.disp_colors)
        self.im = rgbd.disp(args=self.args, grips=Grips)


if __name__ =='__main__':
    cfg_path = 'configs/grasp_detection/grip_net.cfg'

    # OnMouseDrawGrip(cfg_path=cfg_path).run()   #1
    # PolygonShower(cfg_path=cfg_path).run() #2
    # GripCifar10DMaker(cfg_path=cfg_path).run() #3


    # PolygonAnalyzer(cfg_path=cfg_path).run()
    CombineCifar10Data(cfg_path='configs/grasp_detection/grip_net.cfg').run()





