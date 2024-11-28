import React from "react";
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Pie, Bar } from "react-chartjs-2";
ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Tooltip, Legend);

const AnalyticsChart = ({ title, data, type }) => {
    // dynamic colors for the chart
    const generateColors = (numColors) => {
      const colors = [];
      for (let i = 0; i < numColors; i++) {
        const hue = (i * 360) / numColors; 
        colors.push(`hsl(${hue}, 70%, 50%)`);
      }
      return colors;
    };
  
    const chartData =
      type === "pie"
        ? {
            labels: Object.keys(data),
            datasets: [
              {
                data: Object.values(data),
                backgroundColor: generateColors(Object.keys(data).length),
              },
            ],
          }
        : {
            labels: data.map((item) => item.manufacturer),
            datasets: [
              {
                label: "Average Horsepower",
                data: data.map((item) => item.avgHorsepower),
                backgroundColor: generateColors(data.length),
              },
            ],
          };
  
    return (
      <div style={{ marginBottom: "40px", textAlign: "center" }}>
        <h3>{title}</h3>
        <div
          style={{
            maxWidth: "600px", 
            margin: "0 auto",
          }}
        >
          {type === "pie" && <Pie data={chartData} />}
          {type === "bar" && <Bar data={chartData} options={{ maintainAspectRatio: true }} />}
        </div>
      </div>
    );
  };
  
export default AnalyticsChart;
  


