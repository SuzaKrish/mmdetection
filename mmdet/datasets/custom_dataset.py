form .coco import CocoDataset
from .registry import DATASETS
from .xml_style import XMLDataset

@DATASETS.register_module
class MyDataset(XMLDataset):
  CLASSES = ('RBC')
