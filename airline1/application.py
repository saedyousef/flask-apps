import os

from flask import Flask, render_template, request, jsonify
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.all()
    return render_template("index.html", flights=flights)
    
@app.route("/book", methods=['POST'])
def book():
    """Book a flight. """
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number.")
    
    flight = Flight.query.get(flight_id)
    if not flight:  
        return render_template("error.html", message="No such flight with that id.")
    flight.add_passenger(name)
    return render_template("success.html", message="Passenger added successfully!")

@app.route("/flights")
def flights():
    """Get all flights. """

    flights = Flight.query.all()
    if not flights:
        return render_template("error.html", message="No flights found.")
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    """List Details for a flight"""
    flight = Flight.query.get(flight_id)
    if not flight:
        return render_template("error.html", message="No such a flight.")
    #passengers = Passenger.query.filter_by(flight_id = flight_id).all()
    passengers = flight.passengers
    return render_template("flight.html", flight=flight, passengers=passengers)
    
@app.route("/api/flights/<int:flight_id>")
def flight_api(flight_id):
    """List Details for a flight"""
    # Make sure flight exists
    flight = Flight.query.get(flight_id)
    if flight is None:
        return jsonify({"error" : "Invalid flight_id"}), 422
    # Get all passengers
    passengers = flight.passengers
    names = []
    for passenger in passengers:
        names.append(passenger.name)
    return jsonify({
        "origin" : flight.origin,
        "destination" : flight.destination,
        "duration" : flight.duration,
        "passengers" : names
    })
    
