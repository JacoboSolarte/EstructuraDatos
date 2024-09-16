from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory data structures
rooms = [
    {'room_number': 101, 'room_type': 'Single', 'status': 'Available'},
    {'room_number': 102, 'room_type': 'Double', 'status': 'Available'},
    {'room_number': 103, 'room_type': 'Suite', 'status': 'Available'},
    {'room_number': 201, 'room_type': 'Single', 'status': 'Available'},
    {'room_number': 202, 'room_type': 'Double', 'status': 'Available'},
    {'room_number': 203, 'room_type': 'Suite', 'status': 'Available'},
    {'room_number': 301, 'room_type': 'Single', 'status': 'Available'},
    {'room_number': 302, 'room_type': 'Double', 'status': 'Available'},
    {'room_number': 303, 'room_type': 'Suite', 'status': 'Available'},
    {'room_number': 401, 'room_type': 'Single', 'status': 'Available'}
]

reservations = []
undo_stack = []

class Reservation:
    def __init__(self, hotel, room, customer_name, identification, phone, reservation_date, time_slot):
        self.hotel = hotel
        self.room = room
        self.customer_name = customer_name
        self.identification = identification
        self.phone = phone
        self.reservation_date = reservation_date
        self.time_slot = time_slot

@app.route('/')
def index():
    return render_template('index.html', rooms=rooms)

@app.route('/reserve/<int:room_number>', methods=['POST'])
def reserve(room_number):
    room = next((r for r in rooms if r['room_number'] == room_number), None)
    if room and room['status'] == 'Available':
        hotel = request.form['hotel']
        customer_name = request.form['customer_name']
        identification = request.form['identification']
        phone = request.form['phone']
        reservation_date = request.form['reservation_date']
        time_slot = request.form['time_slot']

        reservation = Reservation(hotel, room, customer_name, identification, phone, reservation_date, time_slot)
        reservations.append(reservation)
        undo_stack.append(reservation)  # Save to undo stack

        room['status'] = 'Reserved'
    return redirect(url_for('index'))

@app.route('/reservations')
def view_reservations():
    return render_template('reservations.html', reservations=reservations)

@app.route('/undo')
def undo_reservation():
    if undo_stack:
        last_reservation = undo_stack.pop()
        for room in rooms:
            if room['room_number'] == last_reservation.room['room_number']:
                room['status'] = 'Available'
                reservations.remove(last_reservation)
                break
    return redirect(url_for('view_reservations'))

if __name__ == '__main__':
    app.run(debug=True)
