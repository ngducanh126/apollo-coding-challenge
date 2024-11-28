import React from "react";
import AnalyticsCard from "../components/AnalyticsCard";
import AnalyticsChart from "../components/AnalyticsChart";

const AnalyticsPage = ({ vehicles }) => {
    // Calculate total vehicles
    const totalVehicles = vehicles.length;

    // Find the most common manufacturer
    const manufacturerCount = {};
    vehicles.forEach((vehicle) => {
    const manufacturer = vehicle.manufacturer_name;
    if (!manufacturerCount[manufacturer]) {
        manufacturerCount[manufacturer] = 0;
    }
    manufacturerCount[manufacturer] += 1;
    });

    let mostCommonManufacturer = "";
    let highestCount = 0;

    for (const manufacturer in manufacturerCount) {
    if (manufacturerCount[manufacturer] > highestCount) {
        highestCount = manufacturerCount[manufacturer];
        mostCommonManufacturer = manufacturer;
    }
    }

    // Calculate the average purchase price
    let totalPurchasePrice = 0;
    vehicles.forEach((vehicle) => {
    totalPurchasePrice += vehicle.purchase_price;
    });
    const avgPurchasePrice = totalPurchasePrice / totalVehicles;

    // Calculate fuel type distribution
    const fuelTypeDistribution = {};
    vehicles.forEach((vehicle) => {
    const fuelType = vehicle.fuel_type;
    if (!fuelTypeDistribution[fuelType]) {
        fuelTypeDistribution[fuelType] = 0;
    }
    fuelTypeDistribution[fuelType] += 1;
    });

    // Calculate average horsepower by manufacturer
    const horsepowerData = {};
    vehicles.forEach((vehicle) => {
    const manufacturer = vehicle.manufacturer_name;
    if (!horsepowerData[manufacturer]) {
        horsepowerData[manufacturer] = { totalHorsepower: 0, count: 0 };
    }
    horsepowerData[manufacturer].totalHorsepower += vehicle.horse_power;
    horsepowerData[manufacturer].count += 1;
    });

    const avgHorsepowerByManufacturer = [];
    for (const manufacturer in horsepowerData) {
    const stats = horsepowerData[manufacturer];
    avgHorsepowerByManufacturer.push({
        manufacturer,
        avgHorsepower: stats.totalHorsepower / stats.count,
    });
    }

  return (
    <div>
      <h1>Analytics</h1>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "20px" }}>
        <AnalyticsCard title="Total Vehicles" value={totalVehicles} />
        <AnalyticsCard title="Most Common Manufacturer" value={mostCommonManufacturer} />
        <AnalyticsCard
          title="Average Purchase Price"
          value={`$${avgPurchasePrice.toFixed(2)}`}
        />
      </div>
      <AnalyticsChart
        title="Fuel Type Distribution"
        data={fuelTypeDistribution}
        type="pie"
      />
      <AnalyticsChart
        title="Average Horsepower by Manufacturer"
        data={avgHorsepowerByManufacturer}
        type="bar"
      />
    </div>
  );
};

export default AnalyticsPage;
