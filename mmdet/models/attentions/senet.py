from __future__ import print_function, division, absolute_import
from collections import OrderedDict
from ..registry import ATTENTIONS
from mmcv.runner import load_checkpoint
import logging
from mmcv.cnn import constant_init, kaiming_init
import math
 
import torch.nn as nn
from torch.utils import model_zoo


@ATTENTIONS.register_module
class SENet(nn.Module):
    def __init__(self, inplanes, reduction=16, bias=True):
        super(SENet, self).__init__()
        self.inplanes = inplanes
        self.reduction = reduction
        self.bias = bias
        self.init_layer()
        self.fp16_enabled = False

    def init_layer(self):
        self.avg_pool = nn.AdaptiveAvgPool2d(output_size=(1, 1))
        self.fc = nn.Sequential(
            nn.Conv2d(self.inplanes, self.inplanes // self.reduction,
                      kernel_size=(1, 1), stride=(1, 1), bias=self.bias),
            nn.ReLU(inplace=True),
            nn.Conv2d(self.inplanes // self.reduction, self.inplanes,
                      kernel_size=(1, 1), stride=(1, 1), bias=self.bias),
            nn.Sigmoid()
        )


    def forward(self, x):
        module_input = x
        x = self.avg_pool(x)
        x = self.fc(x)
        # x = self.fc1(x)
        # x = self.relu(x)
        # x = self.fc2(x)
        # x = self.sigmoid(x)
        output = module_input * x + module_input
        return output
