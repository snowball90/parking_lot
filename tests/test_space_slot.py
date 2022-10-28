import unittest

from src.space_slot import SpaceSlot


class SpaceSlotTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.space_slot_1 = SpaceSlot(1)
        cls.space_slot_2 = SpaceSlot(2)
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()

    def test_valid_input(self):
        try:
            SpaceSlot(1)
        except Exception as err:
            self.fail(
                f"unable to initialize SpaceSLot with valid input, received error {repr(err)}")

    def test_invalid_input(self):
        # Test if the input cannot cast to int.
        with self.assertRaises(ValueError) as err:
            SpaceSlot('one')
        expected_errormessage = "The id of the space slot should be castable to an int."
        self.assertIn(expected_errormessage, str(err.exception))

        # Test if the input is smaller than zero
        with self.assertRaises(ValueError) as err:
            SpaceSlot(-1)
        expected_errormessage = "The id of the space slot should be bigger than zero(0)."
        self.assertIn(expected_errormessage, str(err.exception))

    def test_add_reservations_valid(self):

        # reservation = SpaceSlot(1).add_reservation((1545925785, 1545925789))
        first_reservation = self.space_slot_1.add_reservation((4, 5))
        self.assertEqual(first_reservation, True)
        self.assertEqual(len(self.space_slot_1.reservations), 1)

        # check -> trying to reserve the same space-slot at the same time-slot
        second_reservation = self.space_slot_1.add_reservation((4, 5))
        self.assertEqual(second_reservation, False)

        # check -> reserve the same time-slote in a different space-slot
        third_reservation = self.space_slot_2.add_reservation((4, 5))
        self.assertEqual(third_reservation, True)

        # check -> add ealry reservation at the start of the resrvations list
        forth_reservation = self.space_slot_2.add_reservation((0, 1))
        self.assertEqual(self.space_slot_2.reservations[0], (0, 1))

        # check -> add a reservation at the end of the reservation list
        fifth_reservation = self.space_slot_2.add_reservation((6, 7))
        self.assertEqual(self.space_slot_2.reservations[-1], (6, 7))

    def test_add_reservation_invalid_type_epoch(self):

        # check if the argument epoch is not of tuple type
        with self.assertRaises(TypeError) as err:
            self.space_slot_1.add_reservation(1)
        expected_errormessage = f"The argument epoch should be of type tuple. Type <class 'int'> given instead."
        self.assertIn(expected_errormessage, str(err.exception))

        # check if the argument epoch isn't castable to integer
        with self.assertRaises(TypeError) as err:
            self.space_slot_1.add_reservation(([], 'two'))
        expected_errormessage = f"The epoch should be castavle to int."
        self.assertIn(expected_errormessage, str(err.exception))
        pass

    def test_avaliable_time_slots(self):

        # reserve various time-slots
        self.space_slot_1.add_reservation((0, 1))
        self.space_slot_1.add_reservation((4, 5))
        self.space_slot_1.add_reservation((6, 7))

        # check the avaliability of the space_slot 1
        free_time_slots = self.space_slot_1.avaliable_time_slots()
        self.assertEqual(free_time_slots, [(2, 3)])

    def test_clear_expired_time_slots(self):

        # clear the expired reservations
        self.space_slot_1.clear_expired_time_slots()
        # check if the reservations list is empty
        self.assertEqual(len(self.space_slot_1.reservations), 0)

        # reserve a time-slot for the far future
        self.space_slot_1.add_reservation((15459257700, 15459257710))
        # clear the expired reservations
        self.space_slot_1.clear_expired_time_slots()
        # check if the reservations list is empty
        self.assertEqual(len(self.space_slot_1.reservations), 1)
