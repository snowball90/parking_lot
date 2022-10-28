from datetime import datetime
import time
import warnings
from typing import Any


class SpaceSlot:
    """
        Class with a simplified functionality of reserving a space-slot (e.g. parking area).

        Attributes:
            id (int): the identification number of the slot.
            # TODO reservation attribute description
    """

    def __init__(self, id):
        """
        Args:
            id (int): the identification of the slot.

        Raises:
            ValueError: if the type of the id isn't castable as int.
            ValueError: if the value of the id is smaller than zero.
        """

        try:
            self.id = int(id)
        except ValueError:
            raise ValueError(
                f'The id of the space slot should be castable to an int.')

        if self.id <= 0:
            raise ValueError(
                f'The id of the space slot should be bigger than zero(0).')

        self.reservations = []

    def add_reservation(self, epoch: tuple) -> Any:
        """check the reservation's calendar of the space slot,
        and enhance it with the new reservation if there is avaliable time-slot.

        Args:
            epoch (tuple): The start/end of the parking reservation in epoch time
                        (e.g. number of seconds that have elapsed since Unix epoch -> 1970-01-01)
        Raises:
            TypeError: If the type of epoch is not tuple.
            TypeError: If the epoch isn;t castable to int.

        Returns:
            (boolean): True when the reservation is succesful, false when slot is occupied for the given epoch.
        """

        # Attributes check
        # check if the argument epoch is of tuple type
        if not isinstance(epoch, tuple):
            raise TypeError(
                f'The argument epoch should be of type tuple. Type {type(epoch)} given instead.')
        # Check if argument epoch is castable to int
        try:
            start, end = int(epoch[0]), int(epoch[1])
            epoch = (start, end)
        except TypeError:
            raise TypeError(f'The epoch should be castavle to int.')
        # check if the start epoch time of the reservation has expired
        if epoch[0] - time.mktime(datetime.now().timetuple()) < 0:
            warnings.warn("The starting time of the reservation is expired.")
            pass

        number_of_reservations = len(self.reservations)
        # check if the slot hasn't any reservation yet -> add reservation
        if number_of_reservations == 0:
            self.reservations.append(epoch)
            return True
        # short the reservation list by the 2nd element of the epochs (e.g. end)
        self.reservations.sort(key=lambda x: x[1])
        # check if the new reservation ends before the start of the already existing reservations of that space slot. -> add
        if epoch[1] < self.reservations[0][0]:
            self.reservations.insert(0, epoch)
        # check if the new reservation starts after the end of the last reservation of the list -> add reservation
        if epoch[0] > self.reservations[-1][1]:
            self.reservations.append(epoch)
            return True
        # check if there is avaliable time-slot for the new reservation -> add reservation
        for i, res in enumerate(self.reservations):
            if i < len(self.reservations) - 1 and epoch[0] > res[1] and epoch[1] < self.reservations[i+1][0]:
                self.reservations.insert(i+1, epoch)
        # if the reservation couln't be made, raise warning message + show avaliable time-slots of the space slot.
        if number_of_reservations == len(self.reservations):
            warnings.warn(
                f'Slot number ({self.id}) is not avaliable for the time-slot -> {epoch}.\n'
                f'The avaliable time-slot(s) for this space-slot is/are -> {self.avaliable_time_slots()}, \n'
                f'and everything after {self.reservations[-1][1]}.')
            return False
        return True

    def avaliable_time_slots(self) -> list:
        """check the avaliability of the slot and return a list with all potential time-slot gaps.

        Returns:
            list: a list with all avaliable time slot gaps.
        """
        free_time_slots = []
        for i, res in enumerate(self.reservations):
            # check if there is a non-overlapping time-slot gap
            if i < len(self.reservations) - 1 and (self.reservations[i+1][0] - res[1]) > 2:
                free_time_slots.append(
                    (res[1] + 1, self.reservations[i+1][0] - 1))
        return free_time_slots

    def clear_expired_time_slots(self):
        """remove the expired time-slots from the reservation's calendar list.
        """
        now = datetime.now()
        index_of_expired_reservations = []
        [index_of_expired_reservations.append(i) for i, res in enumerate(
            self.reservations) if (time.mktime(now.timetuple()) - res[1]) > 0]
        if len(index_of_expired_reservations) > 0:
            index_of_expired_reservations = sorted(
                index_of_expired_reservations, reverse=True)
            [self.reservations.pop(
                idx) for idx in index_of_expired_reservations if idx < len(self.reservations)]
