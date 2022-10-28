from flask import Flask
from flask import request
from src.parking import ParkingLot

app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
def index():
    new_reservation = request.args.get("key", "")
    if new_reservation:
        new_reservation = tuple(map(int, new_reservation.split(', ')))
        returned_msg = parking.reserve(new_reservation)
    else:
        returned_msg = ""
    return (
        """<h1>Parking Lot<br></h1>
        </h2>Parking capacity: 5 space-slot<br></h2>
        <form action="" method="get">
                <b>Reserve a time-slot (in unix epoch): <input type="text" name="key">
                <input type="submit" value="Check availabilty"><br>
            </form>"""
        + "Booking status: "
        + returned_msg
    )
parking = ParkingLot(5)
app.run(host="127.0.0.1", port=8000, use_reloader=True, debug=True)

