export const fetchVehicles = async () => {
    const response = await fetch('http://127.0.0.1:5000/vehicle');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return await response.json();
  };
  