import React from 'react';
import VehicleTable from '../components/VehicleTable';

const VehicleListPage = ({ vehicles }) => {
  return (
    <div>
      <h1>Vehicle List</h1>
      <VehicleTable vehicles={vehicles} />
    </div>
  );
};

export default VehicleListPage;
