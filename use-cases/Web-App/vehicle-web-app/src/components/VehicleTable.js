import React from 'react';
import './VehicleTable.css';

const VehicleTable = ({ vehicles }) => {
  return (
    <div className="vehicle-table-container">
      <table className="vehicle-table">
        <thead>
          <tr>
            <th>VIN</th>
            <th>Manufacturer</th>
            <th>Model</th>
            <th>Year</th>
            <th>Horsepower</th>
            <th>Price</th>
            <th>Fuel Type</th>
          </tr>
        </thead>
        <tbody>
          {vehicles.map((vehicle) => (
            <tr key={vehicle.vin}>
              <td>{vehicle.vin}</td>
              <td>{vehicle.manufacturer_name}</td>
              <td>{vehicle.model_name}</td>
              <td>{vehicle.model_year}</td>
              <td>{vehicle.horse_power}</td>
              <td>${vehicle.purchase_price}</td>
              <td>{vehicle.fuel_type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VehicleTable;
