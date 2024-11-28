import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import VehicleForm from "../components/VehicleForm";

const AddVehiclePage = () => {
  const [formData, setFormData] = useState({
    vin: "",
    manufacturer_name: "",
    description: "",
    horse_power: "",
    model_name: "",
    model_year: "",
    purchase_price: "",
    fuel_type: "",
  });
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const updatedFormData = { ...formData }; 
    const fieldName = e.target.name; 
    const fieldValue = e.target.value;
    updatedFormData[fieldName] = fieldValue;
    setFormData(updatedFormData); 
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://127.0.0.1:5000/vehicle", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        navigate("/vehicles");
      } else {
        const errorData = await response.json();
        setError(errorData.error || "Failed to add vehicle");
      }
    } catch (err) {
      setError("Error connecting to the server");
    }
  };

  return (
    <div>
      <h1>Add Vehicle</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <VehicleForm
        formData={formData}
        handleChange={handleChange}
        handleSubmit={handleSubmit}
        buttonText="Add Vehicle"
      />
    </div>
  );
};

export default AddVehiclePage;
