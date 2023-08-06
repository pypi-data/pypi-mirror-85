# -*- coding: utf-8 -*-
"""
残差神经网络模块
"""

import torch
import torch.nn as nn
from torch import Tensor

__all__ = ["ResNet34"]


class ResidualBlock(nn.Module):
    """残差块，用于构造ResNet"""

    def __init__(self, input_channels: int, out_channels: int, *, first_stride=1):
        super().__init__()
        assert first_stride == 1 or first_stride == 2

        self.relu = nn.ReLU(inplace=True)
        self.layer1 = nn.Sequential(
            nn.Conv2d(input_channels, out_channels, kernel_size=3, stride=first_stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )

        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        self.projection = nn.Conv2d(input_channels, out_channels, kernel_size=1,
                                    stride=2, bias=False) if first_stride == 2 else None

    def forward(self, x):
        identity = x

        out = self.layer1(x)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.projection is not None:
            identity = self.projection(identity)

        out += identity
        return self.relu(out)


class ResNet34(nn.Module):
    """
    残差神经网络
    References:
        https://arxiv.org/abs/1512.03385
    """

    def __init__(self, class_num: int = 1000):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3,
                      bias=False),
            nn.BatchNorm2d(64),
        )

        self.conv2_x = nn.Sequential(nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
                                     ResNet34._residual_blocks(64, 3))

        self.conv3_x = nn.Sequential(
            ResidualBlock(64, 128, first_stride=2),
            ResNet34._residual_blocks(128, 3)
        )

        self.conv4_x = nn.Sequential(
            ResidualBlock(128, 256, first_stride=2),
            ResNet34._residual_blocks(256, 5)
        )

        self.conv5_x = nn.Sequential(
            ResidualBlock(256, 512, first_stride=2),
            ResNet34._residual_blocks(512, 2)
        )

        self.avg_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, class_num)

    @staticmethod
    def _residual_blocks(channels: int, layer_num):
        layers = []
        for _ in range(layer_num):
            layers.append(ResidualBlock(channels, channels))

        return nn.Sequential(*layers)

    def forward(self, x: Tensor):
        x = self.conv1(x)
        x = self.conv2_x(x)
        x = self.conv3_x(x)
        x = self.conv4_x(x)
        x = self.conv5_x(x)

        x = self.avg_pool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        return x
