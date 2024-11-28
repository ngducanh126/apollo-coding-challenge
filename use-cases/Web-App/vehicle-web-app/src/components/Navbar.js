import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav>
    <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/vehicles">Vehicles</Link></li>
        <li><Link to="/analytics">Analytics</Link></li>
        <li><Link to="/add-vehicle">Add Vehicle</Link></li>
        <li><Link to="/edit-vehicle">Edit Vehicle</Link></li>
    </ul>
    </nav>

  );
};

export default Navbar;
