from .registry import DATASETS
from .xml_style import XMLDataset


@DATASETS.register_module
class DIORDataset(XMLDataset):

    #CLASSES = ('aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car',
    #           'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse',
    #           'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train',
    #           'tvmonitor')
    CLASSES = ('airplane','airport','baseballfield','basketballcourt',
               'bridge','chimney','dam','Expressway-Service-area',
               'golffield','groundtrackfield','harbor','overpass',
               'ship','stadium','storagetank','tenniscourt','trainstation',
               'vehicle','windmill','Expressway-toll-station')

    def __init__(self, **kwargs):
        super(DIORDataset, self).__init__(**kwargs)
