# -*- coding: utf-8 -*-
import abc
from typing import Tuple, List

import torch
from PIL import Image
from PIL.ImageFile import ImageFile
from torch.utils.data import Dataset
from torchvision import transforms

from nn_torch.common import Size


def collate(batch: List[Tuple[torch.Tensor, Tuple[int, int], torch.Tensor]]):
    """
    replace the default_collate function in torch.utils.data.DataLoader
    """
    images, img_sizes, labels = zip(*batch)
    return torch.stack(images), img_sizes, labels


class ObjectDetectionDataset(Dataset, metaclass=abc.ABCMeta):
    """
    Abstract Dataset class for object detection
    """

    def __init__(self, transform: transforms.Compose):
        self._transform: transforms.Compose = transform

    def _open_img(self, img_path: str) -> Tuple[torch.Tensor, Size]:
        img: ImageFile = Image.open(img_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        size = Size.from_tuple(img.size)
        return self._transform(img), size

    @abc.abstractmethod
    def __getitem__(self, index: int) -> Tuple[torch.Tensor, Size, torch.Tensor]:
        """
        Get image and labels
        Args:
            index: index of data

        Returns:
            JPG image, raw image width and height, labels
        """
        pass

    @abc.abstractmethod
    def __len__(self) -> int:
        pass
