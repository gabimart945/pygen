import {React, useState} from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';




import OwnerTable from './components/OwnerTable';
import OwnerForm from './components/OwnerForm';
import OwnerView from './views/OwnerView';

import PetTable from './components/PetTable';
import PetForm from './components/PetForm';
import PetView from './views/PetView';

import VetTable from './components/VetTable';
import VetForm from './components/VetForm';
import VetView from './views/VetView';

import VisitTable from './components/VisitTable';
import VisitForm from './components/VisitForm';
import VisitView from './views/VisitView';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(Boolean(localStorage.getItem("token"))); // Check if token exists

  const handleLogout = () => {
    localStorage.removeItem("token"); // Remove token
    window.location.href = "/login"; // Redirect to login page
  };

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  return (
    <Router>
      <div className="App">
        {/* Navigation Bar */}
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">Home</Link>
            <button
              className="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav">
                
                <li className="nav-item">
                  <Link className="nav-link" to="/owner/view">Owner</Link>
                </li>
                
                <li className="nav-item">
                  <Link className="nav-link" to="/pet/view">Pet</Link>
                </li>
                
                <li className="nav-item">
                  <Link className="nav-link" to="/vet/view">Vet</Link>
                </li>
                
                <li className="nav-item">
                  <Link className="nav-link" to="/visit/view">Visit</Link>
                </li>
                

              </ul>
              <ul className="navbar-nav ms-auto">
                
              </ul>
            </div>
          </div>
        </nav>
        <Routes>
          
          {/* Public Routes */}
          
          <Route path="/owner/view" element={<OwnerView />} />
          <Route path="/owner/table" element={<OwnerTable />} />
          <Route path="/owner/form" element={<OwnerForm id={null} />} />
          <Route path="/owner/form/:id" element={<OwnerForm />} />
          
          <Route path="/pet/view" element={<PetView />} />
          <Route path="/pet/table" element={<PetTable />} />
          <Route path="/pet/form" element={<PetForm id={null} />} />
          <Route path="/pet/form/:id" element={<PetForm />} />
          
          <Route path="/vet/view" element={<VetView />} />
          <Route path="/vet/table" element={<VetTable />} />
          <Route path="/vet/form" element={<VetForm id={null} />} />
          <Route path="/vet/form/:id" element={<VetForm />} />
          
          <Route path="/visit/view" element={<VisitView />} />
          <Route path="/visit/table" element={<VisitTable />} />
          <Route path="/visit/form" element={<VisitForm id={null} />} />
          <Route path="/visit/form/:id" element={<VisitForm />} />
          
          
        </Routes>
      </div>
    </Router>
  );
}

export default App;