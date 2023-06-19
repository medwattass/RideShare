from flask_app import app
from flask import redirect, session, jsonify
from flask_app.models.ride import Ride
from flask_app.models.message import Message
from flask_app.models.join_ride import Join_ride


@app.route('/join_rides/<int:ride_id>/create')
def add_join_ride(ride_id):
    if 'user_id' in session:
        data = {
            'user_id' : session['user_id'],
            'ride_id' : ride_id
        }
        Join_ride.save(data)
        Ride.updateSeats({'id' : ride_id})
        return jsonify({'message' : "success"})
    return redirect('/')

@app.route('/join_rides/<int:ride_id>/delete')
def delete(ride_id):
    if 'user_id' in session:
        data = {
            'user_id' : session['user_id'],
            'ride_id' : ride_id
        }
        Join_ride.cancel(data)
        Ride.addSeat({'id' : ride_id})
        return jsonify({'message' : "success"})
    return redirect('/')


#added this method to delete a passenger from the ride
@app.route('/join_rides/<int:user_id>/<int:ride_id>/delete')
def delete_from_ride(user_id, ride_id):
    if 'user_id' in session:
        ride = Ride.get_by_id({'id' : ride_id})
        data = {
            'user_id' : user_id,
            'ride_id' : ride_id
        }
        message_to_send = f"""This Ride Has Been Cancelled For You :
        From : {ride.from_location}
        To : {ride.to_location}
        At : {ride.when_time}
        """
        message_data = {
                    'sender_id' : session['user_id'],
                    'receiver_id' : user_id,
                    'message' : message_to_send,
                    'ride_id' : ride_id
                    }
        Message.send(message_data)
        Join_ride.cancel(data)
        Ride.addSeat({'id' : ride_id})
        # return jsonify({'message' : "success"})
        return redirect('/rides/'+ str(ride_id) +'/edit')
    return redirect('/')
