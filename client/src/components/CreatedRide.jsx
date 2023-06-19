import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';


function CreatedRides() {
  const [createdRides, setCreatedRides] = useState([]);
  const [user, setUser] = useState({});

  useEffect(() => {
    axios.get('/api/my_created_rides')
      .then(response => {
        const { data } = response;
        setCreatedRides(data.rides);
        setUser(data.user);
      })
      .catch(error => console.error('Error:', error));
  }, []);

  const handleDelete = (rideId) => {
    axios.delete(`/api/rides/${rideId}`)
      .then(response => {
        // Remove the deleted ride from the state
        setCreatedRides(createdRides.filter(ride => ride.id !== rideId));
      })
      .catch(error => console.error('Error:', error));
  };


      return (
        <div className="container p-2 m-auto">
          <div className="row col-12 mx-auto my-5">
            <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
              <div className="container-fluid">
                <div className="d-flex align-items-center">
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
                      <Link className="nav-link" aria-current="page" to="/api/rides">Create a Ride</Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" aria-current="page" to="/api/rides/find">Find a Ride</Link>
                    </li>
                    <li className="nav-item">
                      <Link className="nav-link" to="/api/my_created_rides">Created Rides</Link>
                    </li>
                    <li className="nav-item">
                      <button className="nav-link" data-bs-toggle="offcanvas" data-bs-target="#staticBackdrop"
                        aria-controls="staticBackdrop">
                        Next Trips
                      </button>
                    </li>
                    <li className="nav-item dropdown">
                      <Link className="nav-link dropdown-toggle" to="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        {user.first_name}
                      </Link>
                      <ul className="dropdown-menu text-center bg-secondary-subtle text-info-emphasis fw-medium">
                        <li>
                          <p className="dropdown-item">
                            {user.first_name} {user.last_name}
                          </p>
                        </li>
                        <li>
                          <p className="dropdown-item text-center bg-secondary-subtle text-info-emphasis fw-medium ">
                            {user.email}
                          </p>
                        </li>
                        <li>
                          <p className="dropdown-item text-center bg-secondary-subtle text-info-emphasis fw-medium">
                            You Created <span id="count">xxx</span> Ride(s)
                          </p>
                        </li>
                        <li>
                          <hr className="dropdown-divider" />
                        </li>
                        <li>
                          <Link to="/logout" className="dropdown-item text-center bg-secondary-subtle text-dark fw-bold">Logout</Link>
                        </li>
                      </ul>
                    </li>
                  </ul>
                  <form className="d-flex" method="POST" action="/search">
                    <select id="filter" name="filter" className="form-control form-control-sm me-2">
                      <option value="from_location">From</option>
                      <option value="to_location">To</option>
                      <option value="when_time">When</option>
                      <option value="driver">Driver</option>
                    </select>
                    <input name="search" className="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
                    <button className="btn btn-outline-light" type="submit">Search</button>
                  </form>
                </div>
              </div>
            </nav>
          </div>
          <div className="row col-12 mx-auto my-5 d-flex justify-content-between">
            {createdRides.length > 0 ? (
              <table className="table table-striped table-bordered text-center">
                <thead className="bg-dark text-light">
                  <tr>
                    <th>From</th>
                    <th>To</th>
                    <th>When</th>
                    <th>Seats</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {createdRides.map(ride => (
                    <tr key={ride.id}>
                      <td>{ride.from_location}</td>
                      <td>{ride.to_location}</td>
                      <td>{ride.when_time}</td>
                      <td>{ride.seats}</td>
                      <td>
                        <div className="d-flex justify-content-evenly">
                          <Link to={`/rides/${ride.id}/edit`} className="btn btn-sm btn-success">Edit</Link>
                          <button onClick={() => handleDelete(ride.id)}>Delete</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <div className="row col-6 mx-auto my-5 d-flex justify-content-center text-center">
                <div className="card">
                  <h5 className="card-header">Created Rides</h5>
                  <div className="card-body">
                    <h5 className="card-title">No Rides Created Yet</h5>
                    <p className="card-text">Dear, {user.first_name}:</p>
                    <p className="card-text">
                      You don't have any created rides yet, you can do it <Link to="/api/rides" className="btn btn-primary btn-sm">Here</Link>
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>
          <div className="offcanvas offcanvas-start" data-bs-backdrop="static" tabIndex="-1" id="staticBackdrop"
            aria-labelledby="staticBackdropLabel">
            <div className="offcanvas-header">
              <h5 className="offcanvas-title" id="staticBackdropLabel">{user.first_name}</h5>
            </div>
            <div className="offcanvas-body">
              <div>
                <ol>
                  Nothing Here Yet
                </ol>
              </div>
            </div>
          </div>
        </div>
      );
    }
    
export default CreatedRides;
