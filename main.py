from src.parking import ParkingLot


if __name__ == "__main__":
    # intialize the object ParkingLot with 4 slots
    parking = ParkingLot(4)
    # # Dummie test data
    # it should be reserved in slot 1 since all slots are empty
    parking.reserve((1, 2))
    # it should be reserved in slot 1 since it does not overlaps with old reservations
    parking.reserve((3, 4))
    # it should be reserved in slot 2 since it overlaps with slot's 1 old reservation
    parking.reserve((1, 2))
    # it should be reserved in slot 3 since it overlaps with slots 1,2 old reservations
    parking.reserve((1, 2))
    # it should be reserved in slot 4 since it overlaps with slots 1,2,3 old reservations
    parking.reserve((1, 2))
    parking.reserve((1, 2))  # all slots are unavaliable for this time-slot
    # it should be reserved in slot 1 since it does not overlaps with old reservations
    parking.reserve((5, 6))
    # it should be reserved in slot 2 since it overlaps with slot's 1 old reservations
    parking.reserve((5, 6))
    # it should be reserved in slot 2 since it overlaps with slot's 1 old reservations.
    parking.reserve((3, 4))
