import React from "react";
import {
  Chart as ChartJS,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  PointElement,
  LineElement
} from "chart.js";
import { Pie, Bar, Line } from "react-chartjs-2";
ChartJS.register(ArcElement, CategoryScale, LinearScale, BarElement, Tooltip, Legend, PointElement, LineElement);

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
  
    let chartData = {}
    if (type === "pie"){
      chartData =
         {
            labels: Object.keys(data),
            datasets: [
              {
                data: Object.values(data),
                backgroundColor: generateColors(Object.keys(data).length),
              },
            ],
          }
    }
    else if (type==='bar'){
      chartData = {
            labels: Object.keys(data),
            datasets: [
              {
                label: "Average Horsepower",
                data: Object.values(data),
                backgroundColor: generateColors(Object.keys(data).length),
              },
            ],
          };
        }
        else if (type==='line'){
          chartData = {
                labels: Object.keys(data),
                datasets: [
                  {
                    label: "Average Purchase Price by year",
                    data: Object.values(data),
                    backgroundColor: generateColors(Object.keys(data).length),
                  },
                ],
              };
            }

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
          {type === "bar" && <Bar data={chartData}  />}
          {type === "line" && <Line data={chartData}  />}
        </div>
      </div>
    );
  };
  
export default AnalyticsChart;
  


