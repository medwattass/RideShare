import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function FindRide() {
  const [fromLocation, setFromLocation] = useState('');
  const [toLocation, setToLocation] = useState('');
  const [whenTime, setWhenTime] = useState('');
  const [rides, setRides] = useState([]);
  const [errors, setErrors] = useState([]);
  const [countMessages, setCountMessages] = useState(0);

  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = {
      from_location: fromLocation,
      to_location: toLocation,
      when_time: whenTime,
    };

    axios
      .post('/api/rides/find', formData)
      .then((response) => {
        const data = response.data;
        if (data.errors.length === 0) {
          setRides(data.rides);
          setErrors([]);
        } else {
          setRides([]);
          setErrors(data.errors);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  const takeSeat = (rideIndex) => {
    const updatedRides = [...rides];
    updatedRides[rideIndex].seats -= 1;
    setRides(updatedRides);
  };

  return (
    <div>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container-fluid">
          <div>
            <img src="/static/img/car-front-fill.svg" className="navbar-brand img-fluid" alt="Logo" />
            <Link to="/home" className="navbar-brand fst-italic fw-medium">RideShare</Link>
          </div>

          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarSupportedContent">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <Link className="nav-link" to="/api/rides">Create a Ride</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/api/rides/find">Find a Ride</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/api/my_created_rides">Created Rides</Link>
              </li>
              <li className="nav-item">
                <button type="button" className="btn btn-dark" data-bs-toggle="offcanvas" data-bs-target="#staticBackdrop"
                  aria-controls="staticBackdrop">
                  Messages <span className="badge badge-danger">{countMessages}</span>
                </button>
              </li>
              <li className="nav-item dropdown">
                <Link className="nav-link dropdown-toggle active" to="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            

                </Link>
                <ul className="dropdown-menu text-center bg-secondary-subtle text-info-emphasis fw-medium">
                  <li>
                    <p className="dropdown-item">
                

  
                    </p>
                  </li>
                  <li>
                    <Link className="dropdown-item" to="/api/my_account">
                      My Account
                    </Link>
                  </li>
                  <li>
                    <Link className="dropdown-item" to="/api/logout">
                      Logout
                    </Link>
                  </li>
                </ul>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <div className="container mt-4">
        <div id="findRideErrorMessage" className={`alert alert-danger ${errors.length > 0 ? '' : 'd-none'}`} role="alert">
          {errors.map((error, index) => (
            <div key={index}>{error}</div>
          ))}
        </div>
        <div id="findRideSuccessMessage" className={`alert alert-success ${rides.length > 0 ? '' : 'd-none'}`} role="alert">
          Rides Found:
          {rides.map((ride, index) => (
            <div key={index}>
              <span>From: {ride.from_location}</span>
              <span>To: {ride.to_location}</span>
              <span>When: {ride.when_time}</span>
              <span>Seats: {ride.seats}</span>
              <button onClick={() => takeSeat(index)}>Take a Seat</button>
            </div>
          ))}
        </div>
        <form id="findRideForm" onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="from_location" className="form-label">From</label>
            <input
              type="text"
              className="form-control"
              id="from_location"
              name="from_location"
              value={fromLocation}
              onChange={(e) => setFromLocation(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="to_location" className="form-label">To</label>
            <input
              type="text"
              className="form-control"
              id="to_location"
              name="to_location"
              value={toLocation}
              onChange={(e) => setToLocation(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="when_time" className="form-label">When</label>
            <input
              type="datetime-local"
              className="form-control"
              id="when_time"
              name="when_time"
              value={whenTime}
              onChange={(e) => setWhenTime(e.target.value)}
            />
          </div>
          <button type="submit" className="btn btn-primary">Find Rides</button>
        </form>
      </div>
    </div>
  );
}

export default FindRide;
