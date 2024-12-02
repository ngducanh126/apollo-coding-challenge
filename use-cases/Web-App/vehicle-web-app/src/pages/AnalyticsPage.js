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
    let totalHorsePowerbyManufacturer = {}
    for (let i=0;i<totalVehicles;i++){
      let hp = vehicles[i]['horse_power']
      let manu = vehicles[i]['manufacturer_name']

      if (!(manu in totalHorsePowerbyManufacturer)){
        totalHorsePowerbyManufacturer[manu] = hp
      }else{
        totalHorsePowerbyManufacturer[manu] += hp
      }
    }

    let avgHorsepowerByManufacturer = {}
    for (let i=0;i<totalVehicles;i++){
      let manu = vehicles[i]['manufacturer_name']
      let avgHorsepower = totalHorsePowerbyManufacturer[manu] / manufacturerCount[manu]
      avgHorsepowerByManufacturer[manu] = avgHorsepower
    }

    console.log('avg HP is ')
    for (let manu in avgHorsepowerByManufacturer){
      console.log(manu + ' has avg: ' + avgHorsepowerByManufacturer[manu])
    }

    // avg purchase price by year
    let totalPurchasePriceByYear = {}
    let avgPurchasePriceByYear = {}
    let yearCount = {}
    for (let i =0;i < totalVehicles; i++){
      let year = vehicles[i]['model_year']
      let purchase_price = vehicles[i]['purchase_price']
      if (! (year in totalPurchasePriceByYear)){
        totalPurchasePriceByYear[year] = purchase_price
      }else{
        totalPurchasePriceByYear[year] += purchase_price
      }
      if (! (year in yearCount)){
        yearCount[year] = 1
      }else{
        yearCount[year] += 1
      }
    }
    for (let year in totalPurchasePriceByYear){
      console.log(year + ' has total PP '+ totalPurchasePriceByYear[year])
    }
    for (let year in totalPurchasePriceByYear){
      let avgPurchasePrice = totalPurchasePriceByYear[year] / yearCount[year]
      avgPurchasePriceByYear[year] = avgPurchasePrice
    }

    console.log('avg purchase price by year :')
    for (let year in avgPurchasePriceByYear){
      console.log(year + ' has avg purchase price '+ avgPurchasePriceByYear[year])
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
        <AnalyticsChart
        title="Average Purchase Price by Year"
        data={avgPurchasePriceByYear}
        type="line"
      />
    </div>
  );
};


export default AnalyticsPage;