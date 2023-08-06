# -*- coding: utf-8 -*-
from typing import List

import torch

from nn_torch.cv.models.fpn import FPN, ResNet34Backbone, MobileNetV3LargeBackbone
from nn_torch.cv.models.mobilenet import MobileNetV3Large
from nn_torch.cv.models.resnet import ResNet34


def test_mobilenet_v3():
    batch_size = 10
    num_class = 4
    net = MobileNetV3Large(num_class)
    x = torch.rand(batch_size, 3, 224, 224)
    y = net(x)
    assert y.shape == torch.Size([batch_size, num_class])


def test_fpn():
    out_channels = 256
    batch_size = 10

    fpns: List[FPN] = [FPN(ResNet34Backbone(ResNet34()), features_num=3, out_channels=out_channels),
                       FPN(MobileNetV3LargeBackbone(MobileNetV3Large()), features_num=3, out_channels=out_channels)]

    x = torch.rand([batch_size, 3, 224, 224])
    for fpn in fpns:
        features = fpn(x)
        assert len(features) == len(fpn.body.in_channels_tuple)
        last_feature_sizes = list(features[0].shape[-2:])
        for feat in features:
            assert feat.shape == torch.Size([batch_size, out_channels] + last_feature_sizes)
            last_feature_sizes[0] *= 2
            last_feature_sizes[1] *= 2
            print(feat.shape)
