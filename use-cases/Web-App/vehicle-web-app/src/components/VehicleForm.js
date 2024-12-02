import React from "react";
import "./VehicleForm.css"; 

const VehicleForm = ({ formData, handleSubmit, handleChange, buttonText }) => {
  return (
    <form className="vehicle-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label>VIN:</label>
        <input
          type="text"
          name="vin"
          value={formData.vin}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label>Manufacturer Name:</label>
        <input
          type="text"
          name="manufacturer_name"
          value={formData.manufacturer_name}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label>Description:</label>
        <input
          type="text"
          name="description"
          value={formData.description}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label>Horse Power:</label>
        <input
          type="number"
          name="horse_power"
          value={formData.horse_power}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label>Model Name:</label>
        <input
          type="text"
          name="model_name"
          value={formData.model_name}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label>Model Year:</label>
        <input
          type="number"
          name="model_year"
          value={formData.model_year}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label>Purchase Price:</label>
        <input
          type="number"
          name="purchase_price"
          value={formData.purchase_price}
          onChange={handleChange}
          required
        />
      </div>
      <div className="form-group">
        <label>Fuel Type:</label>
        <input
          type="text"
          name="fuel_type"
          value={formData.fuel_type}
          onChange={handleChange}
          required
        />
      </div>
      <button className="form-button" type="submit">{buttonText}</button>
    </form>
  );
};

export default VehicleForm;
