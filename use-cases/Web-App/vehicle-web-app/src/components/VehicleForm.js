import React from "react";


const VehicleForm = ({ formData, handleSubmit, handleChange, buttonText }) => {
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>
          VIN:
          <input
            type="text"
            name="vin"
            value={formData.vin}
            onChange={handleChange}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Manufacturer Name:
          <input
            type="text"
            name="manufacturer_name"
            value={formData.manufacturer_name}
            onChange={handleChange}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Description:
          <input
            type="text"
            name="description"
            value={formData.description}
            onChange={handleChange}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Horse Power:
          <input
            type="number"
            name="horse_power"
            value={formData.horse_power}
            onChange={handleChange}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Model Name:
          <input
            type="text"
            name="model_name"
            value={formData.model_name}
            onChange={handleChange}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Model Year:
          <input
            type="number"
            name="model_year"
            value={formData.model_year}
            onChange={handleChange}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Purchase Price:
          <input
            type="number"
            name="purchase_price"
            value={formData.purchase_price}
            onChange={handleChange}
            required
          />
        </label>
      </div>
      <div>
        <label>
          Fuel Type:
          <input
            type="text"
            name="fuel_type"
            value={formData.fuel_type}
            onChange={handleChange}
            required
          />
        </label>
      </div>
      <button type="submit">{buttonText}</button>
    </form>
  );
};


export default VehicleForm;
