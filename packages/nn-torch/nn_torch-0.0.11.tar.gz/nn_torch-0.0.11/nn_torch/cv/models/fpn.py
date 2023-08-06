# -*- coding: utf-8 -*-
import abc
from typing import List

import torch
import torch.nn as nn
import torch.nn.functional as F

from nn_torch.cv.models.mobilenet import MobileNetV3Large
from nn_torch.cv.models.resnet import ResNet34


class FPN(nn.Module):
    """
    FPN Module

    References: http://arxiv.org/abs/1612.03144
    """

    class Backbone(nn.Module, metaclass=abc.ABCMeta):
        """Backbone for FPN"""

        @property
        @abc.abstractmethod
        def in_channels_tuple(self) -> tuple:
            pass

        @abc.abstractmethod
        def bottom_up(self, x: torch.Tensor):
            pass

    def __init__(self, body: Backbone, *, features_num: int, out_channels: int):
        super().__init__()
        self._features_num = features_num
        self._out_channels = out_channels

        self.body = body

        self.inner_block_modules = nn.ModuleList(
            [nn.Conv2d(kernel_size=1, in_channels=i, out_channels=out_channels) for i in
             body.in_channels_tuple]
        )
        self.layer_block_modules = nn.ModuleList([
            nn.Conv2d(kernel_size=3, in_channels=out_channels, out_channels=out_channels, padding=1) for _ in
            range(len(body.in_channels_tuple))]
        )

    @property
    def num_features(self) -> int:
        """
        Number of feature map
        """
        return self._features_num

    @property
    def out_channels(self) -> int:
        return self._out_channels

    def forward(self, x: torch.Tensor) -> List[torch.Tensor]:
        layers = self.body.bottom_up(x)

        last_layer = self.inner_block_modules[0](layers[0])
        features = [self.layer_block_modules[0](last_layer)]

        feat_shape = list(layers[1].shape[-2:])
        for idx, layer in enumerate(layers[1:], start=1):
            up_sample = F.interpolate(last_layer, size=feat_shape)

            # undergoes a 1x1 convolutional layer to reduce channel dimensions
            inner_layer = self.inner_block_modules[idx](layer)
            last_layer = inner_layer + up_sample
            feat = self.layer_block_modules[idx](last_layer)
            features.append(feat)
            feat_shape[0] *= 2
            feat_shape[1] *= 2

        return features


class ResNet34Backbone(FPN.Backbone):

    def __init__(self, resnet34: ResNet34):
        super().__init__()
        self._resnet34 = resnet34

    @property
    def in_channels_tuple(self) -> tuple:
        return 512, 256, 128, 64

    def bottom_up(self, x: torch.Tensor) -> tuple:
        x = self._resnet34.conv1(x)

        layer1: torch.Tensor = self._resnet34.conv2_x(x)
        layer2: torch.Tensor = self._resnet34.conv3_x(layer1)
        layer3: torch.Tensor = self._resnet34.conv4_x(layer2)
        layer4: torch.Tensor = self._resnet34.conv5_x(layer3)
        return layer4, layer3, layer2, layer1


class MobileNetV3LargeBackbone(FPN.Backbone):

    def __init__(self, mobilenet_v3: MobileNetV3Large):
        super().__init__()
        self._mobilenet_v3 = mobilenet_v3

    @property
    def in_channels_tuple(self) -> tuple:
        return 960, 80, 40, 24, 16

    def bottom_up(self, x: torch.Tensor) -> tuple:
        layer1: torch.Tensor = self._mobilenet_v3.conv1(x)
        layer2: torch.Tensor = self._mobilenet_v3.bneck1(layer1)
        layer3: torch.Tensor = self._mobilenet_v3.bneck2(layer2)
        layer4: torch.Tensor = self._mobilenet_v3.bneck3(layer3)
        layer5: torch.Tensor = self._mobilenet_v3.conv2(self._mobilenet_v3.bneck4(layer4))
        return layer5, layer4, layer3, layer2, layer1
