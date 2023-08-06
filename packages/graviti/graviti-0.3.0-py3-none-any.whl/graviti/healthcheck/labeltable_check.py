#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains healthcheck related functions."""


from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Tuple,
    Type,
    TypeVar,
)

from ..label import LabelTables, LabelType
from ..label.label_table import AttributeInfo, AttributeType, CategoryInfo
from .pipeline import PipelineForIterable

T = TypeVar("T", bound="AttributeInfoError")  # pylint: disable=invalid-name

attribute_info_pipeline: PipelineForIterable[
    AttributeInfo, "AttributeInfoError"
] = PipelineForIterable()


def check_label_table(
    label_tables: LabelTables,
) -> Generator[Tuple[LabelType, "AttributeInfoError"], None, None]:
    for label_type, label_table in label_tables.items():
        if hasattr(label_table, "attributes"):
            for error in attribute_info_pipeline(label_table.attributes.values()):
                yield label_type, error


class AttributeInfoError:
    def __init__(self, name: str) -> None:
        self._name = name


class NeitherTypeNorEnumError(AttributeInfoError):
    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": Neither "type" nor "enum" field exists'


@attribute_info_pipeline.register
def check_neither_type_nor_enum(
    attribute_info: AttributeInfo,
) -> Generator[NeitherTypeNorEnumError, None, None]:
    if not attribute_info.enum and not attribute_info.attribute_type:
        yield NeitherTypeNorEnumError(attribute_info.name)


class RedundantTypeError(AttributeInfoError):
    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": "type" field is redundant when "enum" field exists'


@attribute_info_pipeline.register
def check_redundant_type(
    attribute_info: AttributeInfo,
) -> Generator[RedundantTypeError, None, None]:
    if attribute_info.enum and attribute_info.attribute_type:
        yield RedundantTypeError(attribute_info.name)


class RangeNotSupportError(AttributeInfoError):
    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": Only number type supports range'


@attribute_info_pipeline.register
def check_range_not_support(
    attribute_info: AttributeInfo,
) -> Generator[RangeNotSupportError, None, None]:
    if attribute_info.maximum is None and attribute_info.minimum is None:
        return

    if isinstance(attribute_info.attribute_type, list):
        if AttributeType.number in attribute_info.attribute_type:
            return

        if AttributeType.integer in attribute_info.attribute_type:
            return

    else:
        if attribute_info.attribute_type in (AttributeType.number, AttributeType.integer):
            return

    yield RangeNotSupportError(attribute_info.name)


class InvalidRangeError(AttributeInfoError):
    def __str__(self) -> str:
        return f'AttributeInfo "{self._name}": Maximum is not larger than minimum'


@attribute_info_pipeline.register
def check_invalid_range(attribute_info: AttributeInfo) -> Generator[InvalidRangeError, None, None]:
    if (
        attribute_info.maximum is not None
        and attribute_info.minimum is not None
        and attribute_info.maximum <= attribute_info.minimum
    ):
        yield InvalidRangeError(attribute_info.name)
