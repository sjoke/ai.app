import React, { Component } from "react";

import Sketcher from "./sketch-canvas/Sketcher";
import Pie from "./chart/Pie";
import "./App.css";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      predictions: []
    };
  }

  onSubmit = predictions => {
    this.setState({ predictions });
  };

  render() {
    const { predictions } = this.state;
    return (
      <div className="app">
        <div className="app-body">
          <div className="app-sketcher">
            <Sketcher onSubmit={this.onSubmit} />
          </div>
          <div className="app-chart-pie">
            <Pie predictions={predictions} />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
