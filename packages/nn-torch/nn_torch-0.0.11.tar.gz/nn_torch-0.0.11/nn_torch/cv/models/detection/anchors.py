# -*- coding: utf-8 -*-
from typing import Tuple

import torch

BboxFmt = int
# --- BboxFmt ---

MIN_WH = 0
MIN_MAX = 1
CWH = 2


# ---------------

def _min_wh2min_max(bbox: torch.Tensor) -> torch.Tensor:
    bbox[..., 2] += bbox[..., 0]
    bbox[..., 3] += bbox[..., 1]
    return bbox


def _min_wh2cwh(bbox: torch.Tensor) -> torch.Tensor:
    bbox[..., 0] += bbox[..., 2] / 2
    bbox[..., 1] += bbox[..., 3] / 2
    return bbox


def _cwh2min_wh(bbox: torch.Tensor) -> torch.Tensor:
    bbox[..., 0] -= bbox[..., 2] / 2
    bbox[..., 1] -= bbox[..., 3] / 2
    return bbox


def _cwh2min_max(bbox: torch.Tensor) -> torch.Tensor:
    return _min_wh2min_max(_cwh2min_wh(bbox))


def _min_max2min_wh(bbox: torch.Tensor) -> torch.Tensor:
    bbox[..., 2] -= bbox[..., 0]
    bbox[..., 3] -= bbox[..., 1]
    return bbox


def _min_max2cwh(bbox: torch.Tensor) -> torch.Tensor:
    return _min_wh2cwh(_min_max2min_wh(bbox))


_methods = [[lambda x: x] * 3 for _ in range(3)]
_methods[MIN_WH][MIN_MAX] = _min_wh2min_max
_methods[MIN_WH][CWH] = _min_wh2cwh
_methods[CWH][MIN_WH] = _cwh2min_wh
_methods[CWH][MIN_MAX] = _cwh2min_max
_methods[MIN_MAX][CWH] = _min_max2cwh
_methods[MIN_MAX][MIN_WH] = _min_max2min_wh


def transform(
        bbox: torch.Tensor,
        bbox_fmt: BboxFmt,
        tar_fmt: BboxFmt,
        inplace: bool = False) -> torch.Tensor:
    """
    Transform bound box's format.
    x corresponds to width, y corresponds to height.
    Args:
        bbox: bound box
        bbox_fmt: format of bbox
        tar_fmt: target format after transform
        inplace: True for change the bbox, False for generate an new object instead of change the bbox.
    """
    if not inplace:
        bbox = bbox.clone()

    return _methods[bbox_fmt][tar_fmt](bbox)


def calc_iou(box1: torch.Tensor, box2: torch.Tensor, fmt1: int, fmt2: int) -> torch.Tensor:
    """
    compute the iou of two boxes.
    Args:
        box1: bound box1
        box2: bound box2
        fmt1: format of bound box1
        fmt2: format of bound box2
    Return:
        iou: iou of box1 and box2.
    See Also:
        BBoxFmt
    """
    box1 = transform(box1, fmt1, MIN_MAX)
    box2 = transform(box2, fmt2, MIN_MAX)

    x1_min, y1_min, x1_max, y1_max = (box1[..., i] for i in range(4))
    x2_min, y2_min, x2_max, y2_max = (box2[..., i] for i in range(4))

    # calculate intersection rectangle's coordinate
    x_i1 = torch.where(x1_min > x2_min, x1_min, x2_min)
    y_i1 = torch.where(y1_min > y2_min, y1_min, y2_min)
    x_i2 = torch.where(x1_max < x2_max, x1_max, x2_max)
    y_i2 = torch.where(y1_max < y2_max, y1_max, y2_max)

    # calculate two bound boxes' areas
    area1 = (x1_max - x1_min) * (y1_max - y1_min)
    area2 = (x2_max - x2_min) * (y2_max - y2_min)

    # calculate intersection area
    inter_area = (torch.where(x_i2 > x_i1, x_i2 - x_i1, torch.tensor(0., dtype=box1.dtype)) *
                  torch.where(y_i2 > y_i1, y_i2 - y_i1, torch.tensor(0., dtype=box1.dtype)))
    iou = inter_area / (area1 + area2 - inter_area + 1e-6)

    return iou


def encode_bboxes(bboxes: torch.Tensor,
                  raw_img_size: Tuple[int, int],
                  transformed_img_size: Tuple[int, int]) -> torch.Tensor:
    """

    Args:
        bboxes: bound boxes[..., 4]
        raw_img_size:
        transformed_img_size:

    Returns:
        resized bound box
    """
    assert bboxes.size(-1) == 4
    bboxes = bboxes.clone()
    wr, hr = transformed_img_size[0] / raw_img_size[0], transformed_img_size[1] / raw_img_size[1]
    bboxes[..., 0] *= wr
    bboxes[..., 2] *= wr
    bboxes[..., 1] *= hr
    bboxes[..., 3] *= hr
    return bboxes
