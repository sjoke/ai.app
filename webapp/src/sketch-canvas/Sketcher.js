import React, { Component } from "react";
import axios from "axios";
import SvgSketchCanvas from "react-sketch-canvas";
import { Button } from "antd";

import "antd/dist/antd.css";
//import 'antd/lib/button/style';
import "./sketcher.css";

class Sketcher extends Component {
  constructor(props) {
    super(props);

    this.canvas = React.createRef();
  }

  handleOK = () => {
    this.canvas.current
      .exportImage("png")
      .then(data => {
        const formData = new FormData();
        formData.append("file", data);
        axios
          .post("/ai/quickdraw/predict", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          .then(() => {
            console.log("上传成功");
          });
      })
      .catch(e => console.log(e));
  };

  reset = () => {
    this.canvas.current.clearCanvas();
  };

  render() {
    return (
      <div className="sketcher-area">
        <div className="sketcher-canvas">
          <SvgSketchCanvas
            ref={this.canvas}
            strokeWidth={4}
            allowOnlyPointerType="mouse"
            strokeColor="#000000"
          />
        </div>
        <div className="sketcher-operations">
          <Button onClick={this.reset}> Reset </Button>
          <Button
            className="sketcher-primary-btn"
            type="primary"
            onClick={this.handleOK}
          >
            OK
          </Button>
        </div>
      </div>
    );
  }
}

export default Sketcher;
