#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains healthcheck related functions."""


from typing import Union

from ..dataset import Dataset, FusionDataset
from .labeltable_check import check_label_table


class HealthReport:
    def __init__(self) -> None:
        pass


def healthcheck(dataset: Union[Dataset, FusionDataset]) -> HealthReport:
    for label_type, error in check_label_table(dataset.label_tables):
        print(label_type)
        print(error)
