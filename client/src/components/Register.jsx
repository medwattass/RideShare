import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
    const [formData, setFormData] = useState({
        first_name: '',
        last_name: '',
        email: '',
        password: '',
        confirm_password: ''
    });

    const [error, setError] = useState('');

    const { first_name, last_name, email, password, confirm_password } = formData;

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        axios
            .post('http://localhost:5000/api/users/register', {
                first_name,
                last_name,
                email,
                password,
                confirm_password
            })
            .then((response) => {
                console.log(response.data);
                
            })
            .catch((error) => {
                setError(error.response.data.message);
                console.error(error.response.data);
            });
    };

    return (
        <section>
            <div className="px-4 py-5 px-md-5 text-center text-lg-start" style={{ backgroundColor: 'hsl(0, 0%, 96%)' }}>
                <div className="container">
                    <div className="row gx-lg-5 align-items-center">
                        <div className="col-lg-6 mb-5 mb-lg-0">
                            <h1 className="my-5 display-3 fw-bold ls-tight">Join the Carpool Revolution</h1>
                            <h4 className="text-primary fst-italic">
                                Save money, reduce your carbon footprint, and meet new people by joining a carpool. With our easy-to-use platform, find a carpool that fits your schedule and lifestyle.
                            </h4>
                        </div>

                        <div className="col-lg-6 mb-5 mb-lg-0">
                            <div className="card">
                                <div className="card-body py-5 px-md-5">
                                    <div className="pb-3">
                                        <h4 className="text-primary-emphasis">Register</h4>
                                    </div>
                                    {error && <div id="regErrorMessage" className="text-bg-danger text-center m-3">{error}</div>}
                                    <form onSubmit={handleSubmit}>
                                        <div className="row">
                                            <div className="col-md-6 mb-4">
                                                <div className="form-outline">
                                                    <input
                                                        type="text"
                                                        name="first_name"
                                                        id="first_name"
                                                        className="form-control"
                                                        placeholder="First Name"
                                                        value={first_name}
                                                        onChange={handleChange}
                                                        required
                                                    />
                                                </div>
                                            </div>
                                            <div className="col-md-6 mb-4">
                                                <div className="form-outline">
                                                    <input
                                                        type="text"
                                                        name="last_name"
                                                        id="last_name"
                                                        className="form-control"
                                                        placeholder="Last Name"
                                                        value={last_name}
                                                        onChange={handleChange}
                                                        required
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        <div className="form-outline mb-4">
                                            <input
                                                type="email"
                                                name="email"
                                                id="email"
                                                className="form-control"
                                                placeholder="Valid Email address"
                                                value={email}
                                                onChange={handleChange}
                                                required
                                            />
                                        </div>

                                        <div className="form-outline mb-4">
                                            <input
                                                type="password"
                                                name="password"
                                                id="password"
                                                className="form-control"
                                                placeholder="Password"
                                                value={password}
                                                onChange={handleChange}
                                                required
                                            />
                                        </div>
                                        <div className="form-outline mb-4">
                                            <input
                                                type="password"
                                                name="confirm_password"
                                                id="confirm_password"
                                                className="form-control"
                                                placeholder="Confirm Password"
                                                value={confirm_password}
                                                onChange={handleChange}
                                                required
                                            />
                                        </div>

                                        <div className="d-flex justify-content-between">
                                            <button type="submit" className="btn btn-primary btn-block mb-4">
                                                Sign Up
                                            </button>
                                            <p className="small fw-bold mt-2 pt-1 mb-0">
                                                Already have an account? <a href="/" className="link-primary">Sign In</a>
                                            </p>
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

export default Register;