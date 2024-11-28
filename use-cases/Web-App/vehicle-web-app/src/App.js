import {useState, useEffect} from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import Navbar from './components/Navbar';
import {fetchVehicles} from './api';
import HomePage from './pages/HomePage';
import VehicleListPage from './pages/VehicleListPage';
import AnalyticsPage from './pages/AnalyticsPage';
import AddVehiclePage from './pages/AddVehiclePage';
import EditVehiclePage from './pages/EditVehiclePage';

function App(){
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [vehicles, setVehicles] = useState([])

  useEffect(()=> {

    const loadVehicles = async () =>{
      try{
        let response = await fetchVehicles();
        setVehicles(response)
      }catch(err){
        setError('error fetching vehicles')
      }finally{
        setLoading(false)
      }
    }

    loadVehicles();

  }, [])


  return (
    <Router>
      <Navbar />
      <div>
        {
          loading ? (
            <p>loading vehicles</p>
          ) : error ? (
            <p>error!</p>
          ) : (
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/vehicles" element={<VehicleListPage vehicles={vehicles} />} />
            <Route path="/analytics" element={<AnalyticsPage vehicles={vehicles} />} />
            <Route path="/add-vehicle" element={<AddVehiclePage />} />
            <Route path="/edit-vehicle" element={<EditVehiclePage vehicles={vehicles} />} />
          </Routes>
          )
        }
      </div>
    </Router>
  );
  
}

export default App