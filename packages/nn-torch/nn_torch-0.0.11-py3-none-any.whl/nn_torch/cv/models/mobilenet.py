# -*- coding: utf-8 -*-
import abc

import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init


class Hswish(nn.Module):
    def forward(self, x):
        return x * F.relu6(x + 3, inplace=True) / 6


class Hsigmoid(nn.Module):
    def forward(self, x):
        return F.relu6(x + 3, inplace=True) / 6


class SeModule(nn.Module):
    """
    squeeze-and-excite
    """

    def __init__(self, in_size, reduction=4):
        super(SeModule, self).__init__()
        self.se = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Conv2d(in_size, in_size // reduction, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(in_size // reduction),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_size // reduction, in_size, kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(in_size),
            Hsigmoid()
        )

    def forward(self, x):
        return x * self.se(x)


class Block(nn.Module):
    """expand + depthwise + pointwise"""

    def __init__(self, kernel_size, in_channels, expand_size, out_channels, nonlinearity, semodule, stride):
        super(Block, self).__init__()
        self.stride = stride
        self.se = semodule

        self.conv1 = nn.Conv2d(in_channels, expand_size, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn1 = nn.BatchNorm2d(expand_size)
        self.nolinear1 = nonlinearity
        self.conv2 = nn.Conv2d(expand_size, expand_size, kernel_size=kernel_size, stride=stride,
                               padding=kernel_size // 2, groups=expand_size, bias=False)
        self.bn2 = nn.BatchNorm2d(expand_size)
        self.nolinear2 = nonlinearity
        self.conv3 = nn.Conv2d(expand_size, out_channels, kernel_size=1, stride=1, padding=0, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels)

        if stride == 1 and in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False),
                nn.BatchNorm2d(out_channels),
            )
        else:
            self.shortcut = nn.Sequential()

    def forward(self, x):
        out = self.nolinear1(self.bn1(self.conv1(x)))
        out = self.nolinear2(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        if self.se is not None:
            out = self.se(out)
        out = out + self.shortcut(x) if self.stride == 1 else out
        return out


class MobileNetV3(nn.Module, metaclass=abc.ABCMeta):
    """
    References:
        https://arxiv.org/abs/1905.02244
    """

    def __init__(self, num_classes: int):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(16),
            Hswish()
        )

        # initializing bneck conv2 linear3 is in subclass

        self.linear4 = nn.Linear(1280, num_classes)

    def forward(self, x):
        out = self.conv1(x)
        out = self.bneck1(out)
        out = self.bneck2(out)
        out = self.bneck3(out)
        out = self.bneck4(out)
        out = self.conv2(out)
        out = F.avg_pool2d(out, 7)
        out = out.view(out.size(0), -1)
        out = self.linear3(out)
        out = self.linear4(out)
        return out

    def _init_params(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                init.kaiming_normal_(m.weight, mode='fan_out')
                if m.bias is not None:
                    init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                init.constant_(m.weight, 1)
                init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                init.normal_(m.weight, std=0.001)
                if m.bias is not None:
                    init.constant_(m.bias, 0)


class MobileNetV3Large(MobileNetV3):

    def __init__(self, num_classes: int = 10000):
        super().__init__(num_classes)
        self.bneck1 = nn.Sequential(
            Block(3, 16, 16, 16, nn.ReLU(inplace=True), None, 1),
            Block(3, 16, 64, 24, nn.ReLU(inplace=True), None, 2),
            Block(3, 24, 72, 24, nn.ReLU(inplace=True), None, 1)
        )
        self.bneck2 = nn.Sequential(
            Block(5, 24, 72, 40, nn.ReLU(inplace=True), SeModule(40), 2),
            Block(5, 40, 120, 40, nn.ReLU(inplace=True), SeModule(40), 1),
            Block(5, 40, 120, 40, nn.ReLU(inplace=True), SeModule(40), 1)
        )
        self.bneck3 = nn.Sequential(
            Block(3, 40, 240, 80, Hswish(), None, 2),
            Block(3, 80, 200, 80, Hswish(), None, 1),
            Block(3, 80, 184, 80, Hswish(), None, 1),
            Block(3, 80, 184, 80, Hswish(), None, 1)
        )
        self.bneck4 = nn.Sequential(
            Block(3, 80, 480, 112, Hswish(), SeModule(112), 1),
            Block(3, 112, 672, 112, Hswish(), SeModule(112), 1),
            Block(5, 112, 672, 160, Hswish(), SeModule(160), 1),
            Block(5, 160, 672, 160, Hswish(), SeModule(160), 2),
            Block(5, 160, 960, 160, Hswish(), SeModule(160), 1),
        )

        self.conv2 = nn.Sequential(
            nn.Conv2d(160, 960, kernel_size=1, bias=False),
            nn.BatchNorm2d(960),
            Hswish()
        )
        self.linear3 = nn.Sequential(
            nn.Linear(960, 1280),
            nn.BatchNorm1d(1280),
            Hswish()
        )

        self._init_params()


class MobileNetV3Small(MobileNetV3):

    def __init__(self, num_classes: int = 10000):
        super().__init__(num_classes)
        self.bneck1 = nn.Sequential(
            Block(3, 16, 16, 16, nn.ReLU(inplace=True), SeModule(16), 2),
        )
        self.bneck2 = nn.Sequential(
            Block(3, 16, 72, 24, nn.ReLU(inplace=True), None, 2),
            Block(3, 24, 88, 24, nn.ReLU(inplace=True), None, 1)
        )
        self.bneck3 = nn.Sequential(
            Block(5, 24, 96, 40, Hswish(), SeModule(40), 2),
            Block(5, 40, 240, 40, Hswish(), SeModule(40), 1),
            Block(5, 40, 240, 40, Hswish(), SeModule(40), 1),
            Block(5, 40, 120, 48, Hswish(), SeModule(48), 1),
            Block(5, 48, 144, 48, Hswish(), SeModule(48), 1)
        )
        self.bneck4 = nn.Sequential(
            Block(5, 48, 288, 96, Hswish(), SeModule(96), 2),
            Block(5, 96, 576, 96, Hswish(), SeModule(96), 1),
            Block(5, 96, 576, 96, Hswish(), SeModule(96), 1),
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(96, 576, kernel_size=1, bias=False),
            nn.BatchNorm2d(576),
            Hswish()
        )
        self.linear3 = nn.Sequential(
            nn.Linear(576, 1280),
            nn.BatchNorm1d(1280),
            Hswish()
        )

        self._init_params()
