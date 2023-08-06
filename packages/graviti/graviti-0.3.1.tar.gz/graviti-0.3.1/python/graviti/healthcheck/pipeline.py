#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains healthcheck related functions."""

from typing import Callable, Generator, Generic, Iterable, List, Optional, TypeVar, Union

V = TypeVar("V")  # pylint: disable=invalid-name
R = TypeVar("R")  # pylint: disable=invalid-name


class Pipeline(Generic[V, R]):
    def __init__(self) -> None:
        self._pipeline: List[Callable[[V], Generator[R, None, None]]] = []

    def register(
        self, func: Callable[[V], Generator[R, None, None]]
    ) -> Callable[[V], Generator[R, None, None]]:
        self._pipeline.append(func)
        return func

    def __call__(self, *args: V) -> Generator[R, None, None]:
        for check in self._pipeline:
            yield from check(*args)


class PipelineForIterable(Pipeline[V, R]):
    def __call__(self, args: Iterable[V]) -> Generator[R, None, None]:
        for arg in args:
            yield from super().__call__(arg)
