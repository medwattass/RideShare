
import './App.css';
import Register from './components/Register';
import Login from './components/Login';
import { Route, Routes} from 'react-router-dom';
import CreatedRides from './components/CreatedRide';
import FormRide from './components/FormRide';
import FindRide from './components/FindRide';


function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Login/>} />
        <Route path="/register" element={<Register/>} />
        <Route path="/createdride" element={<CreatedRides/>} />
        <Route path="/api/rides" element={<FormRide/>}/>
        <Route path="/find/ride" element={<FindRide/>}/>        
        </Routes>
      
    </div>
  );
}

export default App;
