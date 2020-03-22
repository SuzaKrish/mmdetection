import os
import os.path as osp
import shutil
import xml.etree.ElementTree as ET

import mmcv
from mmdet.core import eval_map, eval_recalls

from .registry import DATASETS
from .xml_style import XMLDataset

import numpy as np


def check_fileDir(filePath, cover=0):
    out_file_dir = os.path.split(filePath)[0]
    if not os.path.isdir(out_file_dir):
        os.makedirs(out_file_dir)
    elif cover:
        shutil.rmtree(out_file_dir)
        os.makedirs(out_file_dir)


def get_valFilePath(saveDir, imgPath):
    imgPathList = imgPath.split('/')
    if imgPath.find('DeepMoon'):
        return os.path.join(saveDir, '/'.join(imgPathList[-3:-1]), imgPathList[-1].split('.')[0] + '.txt')
    else:
        return os.path.join(saveDir, imgPathList[-1].split('.')[0] + '.txt')


@DATASETS.register_module
class MOONCraterDataset(XMLDataset):
    """
    Reader for the MOON Crater dataset in PASCAL VOC format.
    Conversion scripts can be found in
    https://github.com/sovrasov/wider-face-pascal-voc-annotations
    """
    CLASSES = ('crater', )

    def __init__(self, **kwargs):
        self.box_min_size = kwargs['min_size'] if 'min_size' in kwargs.keys() else None
        super(MOONCraterDataset, self).__init__(**kwargs)

    def _filter_imgs(self, min_size=32):
        """Filter images too small or without required ground truths."""
        valid_inds = []
        for i, img_info in enumerate(self.img_infos):
            if len(self.get_boxes_info(i)) == 0:
                continue
            if min(img_info['width'], img_info['height']) >= min_size:
                valid_inds.append(i)
        return valid_inds

    def get_ann_info(self, idx):
        img_id = self.img_infos[idx]['id']
        xml_path = osp.join(self.img_prefix, 'Annotations',
                            '{}.xml'.format(img_id))
        tree = ET.parse(xml_path)
        root = tree.getroot()
        bboxes = []
        labels = []
        bboxes_ignore = []
        labels_ignore = []
        for obj in root.findall('object'):
            name = obj.find('name').text
            label = self.cat2label[name]
            difficult = int(obj.find('difficult').text)
            bnd_box = obj.find('bndbox')
            bbox = [
                float(bnd_box.find('xmin').text),
                float(bnd_box.find('ymin').text),
                float(bnd_box.find('xmax').text),
                float(bnd_box.find('ymax').text)
            ]
            ignore = False
            if self.min_size:
                # assert not self.test_mode
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                if w < self.min_size or h < self.min_size:
                    ignore = True
            if difficult or ignore:
                bboxes_ignore.append(bbox)
                labels_ignore.append(label)
            else:
                bboxes.append(bbox)
                labels.append(label)
        if not bboxes:
            bboxes = np.zeros((0, 4))
            labels = np.zeros((0, ))
        else:
            bboxes = np.array(bboxes, ndmin=2) - 1
            labels = np.array(labels)
        if not bboxes_ignore:
            bboxes_ignore = np.zeros((0, 4))
            labels_ignore = np.zeros((0, ))
        else:
            bboxes_ignore = np.array(bboxes_ignore, ndmin=2) - 1
            labels_ignore = np.array(labels_ignore)
        ann = dict(
            bboxes=bboxes.astype(np.float32),
            labels=labels.astype(np.int64),
            bboxes_ignore=bboxes_ignore.astype(np.float32),
            labels_ignore=labels_ignore.astype(np.int64))
        return ann

    def get_boxes_info(self, idx):
        img_id = self.img_infos[idx]['id']
        xml_path = osp.join(self.img_prefix, 'Annotations',
                            '{}.xml'.format(img_id))
        tree = ET.parse(xml_path)
        root = tree.getroot()
        bboxes = []
        for obj in root.findall('object'):
            difficult = int(obj.find('difficult').text)
            bnd_box = obj.find('bndbox')
            try:
                bbox = [
                    float(bnd_box.find('xmin').text),
                    float(bnd_box.find('ymin').text),
                    float(bnd_box.find('xmax').text),
                    float(bnd_box.find('ymax').text)
                ]
            except:
                print('done')
            ignore = False
            if self.box_min_size:
                assert not self.test_mode
                w = bbox[2] - bbox[0]
                h = bbox[3] - bbox[1]
                if w < self.box_min_size or h < self.box_min_size:
                    ignore = True
            if not difficult and not ignore:
                bboxes.append(bbox)
        if not bboxes:
            bboxes = np.zeros((0, 4))
        else:
            bboxes = np.array(bboxes, ndmin=2) - 1
        return bboxes.astype(np.float32)

    def format_results(self, results, **kwargs):
        data_loader = kwargs['data_loader']
        save_dir = kwargs['save_dir']
        prog_bar = mmcv.ProgressBar(len(data_loader))
        for i, data in enumerate(data_loader):
            img_path = data['img_meta'][0].data[0][0]['filename']
            im_save_path = get_valFilePath(save_dir, img_path)
            check_fileDir(im_save_path)
            result_file = open(im_save_path, 'w')
            result_file.write('{}\n'.format(img_path))
            dets = results[i][0]
            for det in dets:
                bbox = det[:4]
                score = det[4]
                result_file.write('{:.1f} {:.1f} {:.1f} {:.1f} {:.3f}\n'.
                                 format(bbox[0], bbox[1],
                                        bbox[2], bbox[3],
                                        score))
            result_file.close()
            prog_bar.update()

    def evaluate(self, results, metric='mAP', logger=None, iou_thr=0.5, nproc=4, **kwargs):
        if not isinstance(metric, str):
            assert len(metric) == 1
            metric = metric[0]
        if 'logger' in kwargs.keys():
            logger = kwargs['logger']
        ds_name = self.CLASSES
        allowed_metrics = ['mAP']
        if metric not in allowed_metrics:
            raise KeyError('metric {} is not supported'.format(metric))
        annotations = [self.get_ann_info(i) for i in range(len(self))]
        eval_results = {}
        assert isinstance(iou_thr, float)
        mean_ap, _ = eval_map(
                        results,
                        annotations,
                        scale_ranges=None,
                        iou_thr=iou_thr,
                        dataset=ds_name,
                        logger=logger)
        eval_results['mAP'] = mean_ap
        return eval_results