import React, { Component, useState } from 'react';
// import logo from './logo.svg';
import './App.css';
import Home from './pages/Home/Home';
import Results from './pages/Results/Results';

function App() {
    const [fileName, setFileName] = useState("Upload New"); 
    return (
      <div className="App">
        <Home setFileName={setFileName}></Home>
        <Results fileName={fileName}></Results>
      </div>
    );
  }

export default App;
