import React, { Component } from 'react';

import Sketcher from './sketch-canvas/Sketcher';
import Pie from './chart/Pie';
import './App.css';

class App extends Component {
  render() {
    return (
      
      <div className="app">
        <div className="app-body">
          <div className="app-sketcher">
            <Sketcher />
          </div> 
          <div className="app-chart-pie">
            <Pie></Pie>
          </div>
        </div>
      </div>
    );
  }
} 

export default App;
