import os.path as osp
import xml.etree.ElementTree as ET

import mmcv

from .builder import DATASETS
from .xml_style import XMLDataset

import numpy as np

@DATASETS.register_module()
class WIDERFaceDataset(XMLDataset):
    """
    Reader for the WIDER Face dataset in PASCAL VOC format.
    Conversion scripts can be found in
    https://github.com/sovrasov/wider-face-pascal-voc-annotations
    """
    CLASSES = ('face', )

    def __init__(self, **kwargs):
        self.box_min_size = kwargs['min_size'] if 'min_size' in kwargs.keys() else None
        super(WIDERFaceDataset, self).__init__(**kwargs)

    def load_annotations(self, ann_file):
        data_infos = []
        img_ids = mmcv.list_from_file(ann_file)
        for img_id in img_ids:
            filename = f'{img_id}.jpg'
            xml_path = osp.join(self.img_prefix, 'Annotations',
                                f'{img_id}.xml')
            tree = ET.parse(xml_path)
            root = tree.getroot()
            size = root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)
            folder = root.find('folder').text
            data_infos.append(
                dict(
                    id=img_id,
                    filename=osp.join('images', folder, filename),
                    width=width,
                    height=height))

        return data_infos

    def _filter_imgs(self, min_size=32):
        """Filter images too small or without required ground truths."""
        valid_inds = []
        for i, img_info in enumerate(self.img_infos):
            if len(self.get_boxes_info(i)) == 0:
                continue
            if min(img_info['width'], img_info['height']) >= min_size:
                valid_inds.append(i)
        return valid_inds

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
            bbox = [
                int(bnd_box.find('xmin').text),
                int(bnd_box.find('ymin').text),
                int(bnd_box.find('xmax').text),
                int(bnd_box.find('ymax').text)
            ]
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
