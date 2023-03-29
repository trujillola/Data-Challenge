import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import Home from './pages/Home/Home';
import Results from './pages/Results/Results';

class App extends Component {
  render() {
    return (
      <div className="App">
        <Home></Home>
        <Results></Results>
      </div>
    );
  }
}

export default App;
