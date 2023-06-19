import React, { useState } from 'react';
import axios from 'axios';

const FormRide = () => {
  const [formData, setFormData] = useState({
    from_location: '',
    to_location: '',
    when_time: '',
    seats: 1
  });
  const [errors, setErrors] = useState([]);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    // Validate form data
    const newErrors = [];
    if (!formData.from_location || formData.from_location.length < 2) {
      newErrors.push('From Location must be at least 2 characters');
    }
    if (!formData.to_location || formData.to_location.length < 2) {
      newErrors.push('Destination must be at least 2 characters');
    }
    if (!formData.when_time) {
      newErrors.push('Ride must have a date and time');
    }
    if (formData.seats < 1) {
      newErrors.push('Ride must have a positive number of seats');
    }

    if (newErrors.length > 0) {
      setErrors(newErrors);
      return;
    }

    axios
      .post("http://localhost:5000/api/rides", formData)
      .then((response) => {
        const data = response.data;
        if (data.errors && data.errors.length > 0) {
          setErrors(data.errors);
        } else {
          // Reset form data and display success message
          setFormData({
            from_location: '',
            to_location: '',
            when_time: '',
            seats: 1
          });
          setErrors(['Ride created successfully!']);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  };

  return (
    <section>
      <div className="px-4 py-5 px-md-5 text-center text-lg-start" style={{ backgroundColor: 'hsl(0, 0%, 96%)' }}>
        <div className="container">
          <div className="row gx-lg-5 align-items-center">
            <div className="col-lg-6 mb-5 mb-lg-0">
              <h1 className="my-5 display-3 fw-bold ls-tight">Create Ride</h1>
            </div>

            <div className="col-lg-6 mb-5 mb-lg-0">
              <div className="card">
                <div className="card-body py-5 px-md-5">
                  <div className="pb-3">
                    <h4 className="text-primary-emphasis">Ride Details</h4>
                  </div>
                  {errors.length > 0 && (
                    <div className="text-bg-danger text-center m-3">
                      <ul>
                        {errors.map((error) => (
                          <li key={error}>{error}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  <form onSubmit={handleSubmit}>
                    <div className="form-outline mb-4">
                      <label className="form-label" htmlFor="fromLocation">From :</label>
                      <input
                        type="text"
                        id="from_location"
                        name="from_location"
                        className="form-control"
                        value={formData.from_location}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                    <div className="form-outline mb-4">
                      <label className="form-label" htmlFor="toLocation">To :</label>
                      <input
                        type="text"
                        id="to_location"
                        name="to_location"
                        className="form-control"
                        value={formData.to_location}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                    <div className="form-outline mb-4">
                      <label className="form-label" htmlFor="whenTime">When:</label>
                      <input
                        type="datetime-local"
                        id="when_time"
                        name="when_time"
                        className="form-control"
                        value={formData.when_time}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                    <div className="form-outline mb-4">
                      <label className="form-label" htmlFor="seats">Seats:</label>
                      <input
                        type="number"
                        id="seats"
                        name="seats"
                        min="1"
                        className="form-control"
                        value={formData.seats}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                    <div className="d-flex justify-content-center">
                      <button type="submit" className="btn btn-primary btn-lg">
                        Create Ride
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FormRide;
