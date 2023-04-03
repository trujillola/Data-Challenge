import React, { Component, useState } from 'react';
// import logo from './logo.svg';
import './App.css';
import Home from './pages/Home/Home';
import Results from './pages/Results/Results';

function App() {
    const [fileName, setFileName] = useState("");//15_2-1__WELL__15-02-01_PB-706-0386.pdf
    const [startScrapping, setStartScrapping] = useState(false);
    if(startScrapping){
      console.log('yo')
    }else{
      console.log('pappapa')
    }
    return (
      <div className="App">
        <Home setFileName={setFileName} setStartScrapping={setStartScrapping} startScrapping={startScrapping}></Home>
        <Results fileName={fileName} startScrapping={startScrapping}></Results>
      </div>
    );
  }

export default App;
