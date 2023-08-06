#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Segment and FusionSegment."""

from typing import Any, Dict, Iterable, List, MutableSequence, Optional, Union, overload

from ..sensor import Sensor, SensorType
from ..utility import NameClass, NameSortedDict
from .data import Data
from .frame import Frame


class Segment(NameClass, MutableSequence[Data]):
    """This class defines the concept of segment,
    which represents a list of Data.

    :param loads: {
        "name": <str>
        "description": <str>
        "data": [
            data_dict{...},
            data_dict{...},
            ...
            ...
        ]
    }
    """

    def __init__(
        self,
        name: str = "",
        *,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._data: List[Data] = []

        if loads:
            super().__init__(loads=loads)
            for data_dict in loads["data"]:
                self._data.append(Data(loads=data_dict))
            return

        super().__init__(name)

    def dumps(self) -> Dict[str, Any]:
        """Dump a Segment into a list.

        :return: A dictionary contains name and annotations
        """

        segment_dict: Dict[str, Any] = super().dumps()
        segment_dict["data"] = [data.dumps() for data in self._data]

        return segment_dict

    def insert(self, index: int, value: Data) -> None:
        """Insert Data before index."""
        return self._data.insert(index, value)

    @overload
    def __getitem__(self, index: int) -> Data:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[Data]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[List[Data], Data]:
        return self._data.__getitem__(index)

    @overload
    def __setitem__(self, index: int, value: Data) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[Data]) -> None:
        ...

    def __setitem__(self, index: Union[int, slice], value: Union[Data, Iterable[Data]]) -> None:
        # https://github.com/python/mypy/issues/7858
        self._data.__setitem__(index, value)  # type: ignore[index, assignment]

    def __delitem__(self, index: Union[int, slice]) -> None:
        self._data.__delitem__(index)

    def __len__(self) -> int:
        return self._data.__len__()


class FusionSegment(NameClass, MutableSequence[Frame]):
    """This class defines the concept of multi-sensor segment,
    which represents a list of Frames.

    :param loads: {
        "name": <str>
        "description": <str>
        "sensors": [
            sensor_dict{...},
            sensor_dict{...},
            ...
            ...
        ]
        "frames": [
            frame_dict{...},
            frame_dict{...},
            ...
            ...
        ]
    }
    """

    def __init__(
        self,
        name: str = "",
        *,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:
        self._frames: List[Frame] = []
        self._sensors: NameSortedDict[Sensor] = NameSortedDict()

        if loads:
            super().__init__(loads=loads)
            for sensor_dict in loads["sensors"]:
                self._sensors.add(Sensor(loads=sensor_dict))
            for frame_dict in loads["frames"]:
                self._frames.append(Frame(loads=frame_dict))
            return

        super().__init__(name)

    def dumps(self) -> Dict[str, Any]:
        """Dumps the segment into a dictionary.

        :return: A dictonary contains name, sensors and frames
        """

        segment_dict: Dict[str, Any] = super().dumps()
        segment_dict["sensors"] = [sensor.dumps() for sensor in self._sensors.values()]
        segment_dict["frames"] = [frame.dumps() for frame in self._frames]

        return segment_dict

    def insert(self, index: int, value: Frame) -> None:
        """Insert Frame before index."""
        return self._frames.insert(index, value)

    @overload
    def __getitem__(self, index: int) -> Frame:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[Frame]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[List[Frame], Frame]:
        return self._frames.__getitem__(index)

    @overload
    def __setitem__(self, index: int, value: Frame) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[Frame]) -> None:
        ...

    def __setitem__(self, index: Union[int, slice], value: Union[Frame, Iterable[Frame]]) -> None:
        self._frames.__setitem__(index, value)  # type: ignore[index, assignment]

    def __delitem__(self, index: Union[int, slice]) -> None:
        self._frames.__delitem__(index)

    def __len__(self) -> int:
        return self._frames.__len__()

    def add_sensor(self, sensor: Sensor) -> None:
        """Add sensor.

        :param sensor: sensor to add
        """

        self._sensors.add(sensor)

    def get_sensor(self, sensor_name: str) -> Sensor:
        """Return sensor info corresponding to input sensor name."""

        return self._sensors[sensor_name]

    def get_sensors(self, sensor_type: Optional[SensorType] = None) -> NameSortedDict[Sensor]:
        """Return all sensors with given sensor type.

        :param sensor_type: sensor type
        :return: a dict of sensors with given sensor type
        """

        if not sensor_type:
            return self._sensors

        data: NameSortedDict[Sensor] = NameSortedDict()
        for sensor in self._sensors.values():
            if sensor.enum == sensor_type:
                data.add(sensor)
        return data

    def get_data_list(self, sensor: Union[str, Sensor]) -> List[Data]:
        """Return all Datas corresponding to given sensor.

        :param sensor: a sensor name or a sensor class
        :return: a list of Datas corresponding to given sensor
        """

        sensor_name = sensor.name if isinstance(sensor, Sensor) else sensor

        return [frame[sensor_name] for frame in self._frames]
