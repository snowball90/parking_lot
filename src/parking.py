import numpy as np
from src.space_slot import SpaceSlot


class ParkingLot():
    """
    Class with a simplified functionality of a parking lot.

    Attributes:
        capacity (int): the capacity of the parking lot.
        # TODO space_slots description attributes
        parking_data (dict): dictionary including info of lot id (as a key) and a list of tuple epochs (as a value)
            -> e.g. {1, [(start_1, stop_1), (start_2, stop_2)]}

    """

    def __init__(self, capacity):
        """
        Args:
            capacity (int): the capacity of the parking lot.

        Raises:
            ValueError: if the type of the capacity isn't castable as int.
            ValueError: if the value of the capacity is smaller than zero.
        """

        try:
            self.capacity = int(capacity)
        except ValueError:
            raise ValueError(
                f'The capacity of the parking lot should be castable to an int.')

        if self.capacity <= 0:
            raise ValueError(
                f'The capacity of the parking lot should be greater than zero(0).')

        self.space_slots = [SpaceSlot(id) for id in np.arange(1, capacity + 1, 1)]
        self.parking_data = {}

    def reserve(self, epoch: tuple) -> str:
        """Make a usage of the functionality of the 'add_reservation' method from
        the Class ParkingSlot to all slots of the parking, and stores the parking's lot data
        into a dictionary.

        Args:
            epoch (tuple): The start/end of the parking reservation in epoch time
                        (e.g. number of seconds that have elapsed since Unix epoch -> 1970-01-01)
        Returns:
            message (str): the printed message confirming or not that the specific parking-slot is available for the given time-slot

        """
        for space_slot in self.space_slots:
            boolean = space_slot.add_reservation(epoch)
            # Check if the reservation is succesful. Otherwise, check the avaliability of the remaining slots.
            if boolean:
                message = (
                    f'Space-slot number {space_slot.id} is available '
                    f'for the time-slot {epoch}.'
                )
                print(message)

                # check if the reservation's calendar of the current slot has data -> add new data into calendar.
                if self.parking_data.get(space_slot.id) is not None:
                    epochs = []
                    epochs.append(self.parking_data[space_slot.id])
                    epochs.append(epoch)
                    epoch = epochs
                self.parking_data[space_slot.id] = epoch
                return str(message)

            # check if the reservation isn't succesful -> chek the avaliability of the remaining slots.
            if not boolean:
                # check if all slots are unavaliable for this reservation and print a statemnt.
                if self.parking_data.get(space_slot.id) is not None and space_slot.id == self.capacity:
                    message = (
                        f'All space-slots are unavaliable for the epoch {epoch}.')
                    print(message)
                    return str(message)
                continue
