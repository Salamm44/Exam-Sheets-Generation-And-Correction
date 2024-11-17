import React from 'react';
import MainPage from './MainPage';
import './App.css';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <div className="App">
      <ToastContainer />
      <MainPage />
    </div>
  );
}

export default App;
