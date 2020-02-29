from .registry import DATASETS
from .xml_style import XMLDataset


@DATASETS.register_module
class VOCDataset(XMLDataset):

    #CLASSES = ('aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',
    #           'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
    #           'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train',
    #           'tvmonitor')
    #CLASSES = ('airplane','airport','baseballfield','basketballcourt',
    #           'bridge','chimney','dam','Expressway-Service-area',
    #           'golffield','groundtrackfield','harbor','overpass',
    #           'ship','stadium','storagetank','tenniscourt','trainstation',
    #           'vehicle','windmill','Expressway-toll-station')
    CLASSES = ('large-vehicle', 'swimming-pool', 'helicopter', 'bridge',
               'plane', 'ship', 'soccer-ball-field', 'basketball-court',
               'ground-track-field', 'small-vehicle', 'harbor', 'baseball-diamond',
               'tennis-court', 'roundabout', 'storage-tank'. 'container-crane')


    def __init__(self, **kwargs):
        super(VOCDataset, self).__init__(**kwargs)
        if 'VOC2007' in self.img_prefix:
            self.year = 2007
        elif 'VOC2012' in self.img_prefix:
            self.year = 2012
        else:
            raise ValueError('Cannot infer dataset year from img_prefix')
