import React, { Component } from "react";
import axios from "axios";
import SvgSketchCanvas from "react-sketch-canvas";
import { Button } from "antd";

import "antd/dist/antd.css";
//import 'antd/lib/button/style';
import "./sketcher.css";

/**
 *Base64字符串转二进制
 */
function dataURLtoBlob(dataurl) {
  var arr = dataurl.split(","),
    mime = arr[0].match(/:(.*?);/)[1],
    bstr = atob(arr[1]),
    n = bstr.length,
    u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], {
    type: mime
  });
}

class Sketcher extends Component {
  constructor(props) {
    super(props);

    this.canvas = React.createRef();
  }

  handleOK = () => {
    const { onSubmit } = this.props;

    this.canvas.current
      .exportImage("png")
      .then(data => {
        var blob = dataURLtoBlob(data);
        const formData = new FormData();
        formData.append("file", blob);
        axios
          .post("/ai/quickdraw/predict", formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            }
          })
          .then(response => {
            onSubmit(response.data);
          })
          .catch(function(error) {
            console.error(error);
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
