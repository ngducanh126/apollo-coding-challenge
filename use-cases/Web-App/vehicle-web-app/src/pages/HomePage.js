import React from 'react';
import './HomePage.css';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="homepage">
      <h1>Welcome to the Vehicle Management System</h1>
      <p>
        Manage your vehicles, analyze data, and explore insights with our easy-to-use platform.
      </p>
      <Link to="/vehicles" className="homepage-button">
        View Vehicles
      </Link>
    </div>
  );
};

export default HomePage;
