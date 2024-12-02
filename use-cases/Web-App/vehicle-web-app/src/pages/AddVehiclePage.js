import { useState } from "react";
import { useNavigate } from "react-router-dom";
import VehicleForm from "../components/VehicleForm";
import "./VehiclePage.css";

const AddVehiclePage = () => {
  const [error, setError] = useState(null);
  const navigate = useNavigate();
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

  const handleChange = (e) => {
    let newForm = { ...formData };
    let newField = e.target.name;
    let newValue = e.target.value;
    newForm[newField] = newValue;
    setFormData(newForm);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      let response = await fetch("http://127.0.0.1:5000/vehicle", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        navigate("/vehicles");
      } else {
        let errorData = await response.json();
        setError("error : " + errorData.error);
      }
    } catch (e) {
      setError("error connecting to server : " + e);
    }
  };

  return (
    <div className="vehicle-page">
      <h1>Adding Vehicle</h1>
      {error && <p>error: {error}</p>}
      <VehicleForm
        formData={formData}
        handleSubmit={handleSubmit}
        handleChange={handleChange}
        buttonText="Add Vehicle"
      />
    </div>
  );
};

export default AddVehiclePage;
