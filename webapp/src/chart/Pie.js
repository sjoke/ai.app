import React, { Component } from "react";
import ReactEcharts from "echarts-for-react";

import "./pie.css";

class Pie extends Component {
  getOption = () => {
    const { predictions } = this.props;

    const data = predictions.map(({ label, prob }) => ({
      value: prob,
      name: label
    }));

    const option = {
      title: { text: "Top-5 accurracy", x: "center" },
      tooltip: { trigger: "item", formatter: "{a} <br/>{b} : {c} ({d}%)" },
      calculable: true,
      label: {
        formatter: function(params) {
          return params.name + ", " + (params.percent - 0).toFixed(0) + "%";
        }
      },
      series: [
        {
          name: "rank-pie",
          type: "pie",
          radius: [20, 100],
          roseType: "area",
          data: data
        }
      ]
    };

    return option;
  };

  render() {
    return <ReactEcharts option={this.getOption()} />;
  }
}

export default Pie;
