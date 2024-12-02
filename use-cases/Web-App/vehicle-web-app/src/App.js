import {useState, useEffect} from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Navbar from './components/Navbar';
import HomePage from './pages/HomePage';
import VehicleListPage from './pages/VehicleListPage';
import AnalyticsPage from './pages/AnalyticsPage';
import AddVehiclePage from './pages/AddVehiclePage';
import EditVehiclePage from './pages/EditVehiclePage';

function App(){
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [vehicles, setVehicles] = useState([]);

  useEffect( ()=>{
    const loadVehicles = async()=>{
      try {
        let response = await fetch('http://127.0.0.1:5000/vehicle')
        let data_got_back = await response.json()
        setVehicles(data_got_back)
      }catch(e){
        setError(e)
      }finally{
        setLoading(false)
      }
    }
    loadVehicles()
    }
    , [])


  return (
    <Router>
      <Navbar />
      <div>
        {loading && <p>Loading... </p>}
        {error && <p>error...</p>}

          <div>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/vehicles" element={<VehicleListPage vehicles={vehicles} />} />
            <Route path="/analytics" element={<AnalyticsPage vehicles={vehicles} />} />
            <Route path="/add-vehicle" element={<AddVehiclePage />} />
            <Route path="/edit-vehicle" element={<EditVehiclePage vehicles={vehicles} />} />
          </Routes>
          </div>
          
      </div>
    </Router>
  );
  
}

export default App