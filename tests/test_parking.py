import unittest

from src.parking import ParkingLot


class ParkingLotTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # initialize an object with a capacity of 2 space-slots
        cls.my_parking_lot = ParkingLot(2)
        return super().setUpClass()

    def test_valid_input(self):
        try:
            ParkingLot(20)
        except Exception as err:
            self.fail(
                f"unable to initialize ParkingLot with valid input, received error {repr(err)}")

    def test_invalid_input(self):
        # Test if the input cannot cast to int.
        with self.assertRaises(ValueError) as err:
            ParkingLot('one')
        expected_errormessage = "The capacity of the parking lot should be castable to an int."
        self.assertIn(expected_errormessage, str(err.exception))

        # Test if the input is smaller than zero
        with self.assertRaises(ValueError) as err:
            ParkingLot(-1)
        expected_errormessage = "The capacity of the parking lot should be greater than zero(0)."
        self.assertIn(expected_errormessage, str(err.exception))

    def test_1_reserve_first_time_slot(self):

        # make a first reservation
        reservation_1 = self.my_parking_lot.reserve((1, 2))
        expected_message = (
            'Space-slot number 1 is avaliable '
            'for the time-slot (1, 2).'
        )
        self.assertIn(expected_message, reservation_1)

    def test_2_reserve_valid_time_slot(self):

        # make a second reservation that starts after the end of the first one
        reservation_2 = self.my_parking_lot.reserve((3, 4))
        expected_message = (
            'Space-slot number 1 is avaliable '
            'for the time-slot (3, 4).'
        )
        self.assertIn(expected_message, reservation_2)

    def test_3_reserve_occupied_time_slot(self):
        # make a third reservation that inteferes woth the reserved at space-slot 1
        reservation_3 = self.my_parking_lot.reserve((1, 3))
        expected_message = (
            'Space-slot number 2 is avaliable '
            'for the time-slot (1, 3).'
        )
        self.assertIn(expected_message, reservation_3)

    def test_4_reserve_all_space_slots_occupied(self):
        # make a forth reservation that inteferes with the time-slots of both space-slots
        reservation_4 = self.my_parking_lot.reserve((1, 3))
        expected_message = (
            'All space-slots are unavaliable for the epoch (1, 3)'
        )
        self.assertIn(expected_message, reservation_4)
