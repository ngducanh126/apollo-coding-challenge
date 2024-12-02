import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; 

const Navbar = () => {
  return (
    <nav className="navbar">
      <ul className="navbar-list">
        <li className="navbar-item">
          <Link to="/" className="navbar-link">Home</Link>
        </li>
        <li className="navbar-item">
          <Link to="/vehicles" className="navbar-link">Vehicles</Link>
        </li>
        <li className="navbar-item">
          <Link to="/analytics" className="navbar-link">Analytics</Link>
        </li>
        <li className="navbar-item">
          <Link to="/add-vehicle" className="navbar-link">Add Vehicle</Link>
        </li>
        <li className="navbar-item">
          <Link to="/edit-vehicle" className="navbar-link">Edit Vehicle</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
