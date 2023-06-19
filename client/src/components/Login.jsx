import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Login = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });
    const [error, setError] = useState([]);
    const { email, password } = formData;
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [imageUrls] = useState([
        'https://images.pexels.com/photos/620335/pexels-photo-620335.jpeg?auto=compress&cs=tinysrgb&w=1200',
        'https://images.pexels.com/photos/2224/road-people-street-smartphone.jpg?auto=compress&cs=tinysrgb&w=1200',
        'https://images.pexels.com/photos/1386649/pexels-photo-1386649.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
        'https://images.pexels.com/photos/4606345/pexels-photo-4606345.jpeg?auto=compress&cs=tinysrgb&w=1200',
    ]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        axios
            .post('http://localhost:5000/api/users/login', {
                email,
                password,
            })
            .then((response) => {
                console.log(response.data);
            })
            .catch((error) => {
                setError(error.response.data);
                console.error(error.response.data);
            });
    };

    useEffect(() => {
        const interval = setInterval(() => {
            setCurrentImageIndex((prevIndex) => (prevIndex + 1) % imageUrls.length);
        }, 3000); // Change image every 3 seconds

        return () => clearInterval(interval);
    }, [imageUrls.length]);

    return (
        <div className="container-fluid vh-100 pt-5" style={{ backgroundColor: 'hsl(0, 0%, 96%)' }}>
            <div className="row d-flex justify-content-center align-items-center h-100">
                <div className="col-md-9 col-lg-6 col-xl-5">
                    <div className="image-container">
                        <img
                            className="d-block w-100"
                            src={imageUrls[currentImageIndex]}
                            alt={`Image ${currentImageIndex + 1}`}
                        />
                    </div>
                </div>
                <div className="col-md-8 col-lg-6 col-xl-4 offset-xl-1">
                    <div className="pb-3">
                        <h4 className="text-primary-emphasis">Welcome Back</h4>
                    </div>
                    {error && (
                        <div id="logErrorMessage" className="text-bg-danger text-center mb-3">
                            {error.message}
                        </div>
                    )}
                    <form onSubmit={handleSubmit}>
                        <div className="form-outline mb-4">
                            <input
                                type="email"
                                name="email"
                                value={email}
                                onChange={handleChange}
                                className="form-control form-control-lg"
                                placeholder="Enter a valid email address"
                                required
                            />
                            <label className="form-label" htmlFor="email">
                                Email address
                            </label>
                        </div>

                        <div className="form-outline mb-3">
                            <input
                                type="password"
                                name="password"
                                value={password}
                                onChange={handleChange}
                                className="form-control form-control-lg"
                                placeholder="Enter password"
                                required
                            />
                            <label className="form-label" htmlFor="password">
                                Password
                            </label>
                        </div>

                        <div className="text-center text-lg-start mt-4 pt-2">
                            <button
                                type="submit"
                                className="btn btn-primary btn-lg"
                                style={{ paddingLeft: '2.5rem', paddingRight: '2.5rem' }}
                            >
                                Sign In
                            </button>
                            <p className="small fw-bold mt-2 pt-1 mb-0">
                                Don't have an account? <a href="/register" className="link-primary">Sign Up</a>
                            </p>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
