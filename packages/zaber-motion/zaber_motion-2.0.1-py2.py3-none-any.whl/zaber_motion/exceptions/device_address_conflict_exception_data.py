# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
# pylint: disable=W0201

from typing import List
from ..protobufs import main_pb2


class DeviceAddressConflictExceptionData:
    """
    Contains additional data for DeviceAddressConflictException.
    """

    @property
    def device_ids(self) -> List[int]:
        """
        The full list of device ids.
        """

        return self._device_ids

    @device_ids.setter
    def device_ids(self, value: List[int]) -> None:
        self._device_ids = value

    def __repr__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def from_protobuf(
        pb_data: main_pb2.DeviceAddressConflictExceptionData
    ) -> 'DeviceAddressConflictExceptionData':
        instance = DeviceAddressConflictExceptionData.__new__(
            DeviceAddressConflictExceptionData
        )  # type: DeviceAddressConflictExceptionData
        instance.device_ids = list(pb_data.device_ids)
        return instance
