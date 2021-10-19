import React, { Component } from "react";
import getWeb3 from "@/utils/getWeb3";
import { convertNum, convertData } from "@/utils/float";
import model from "./imdb-sentiment-model.json";
import wordIndex from "./imdb.json";
import "./test.less";

export default class Test extends Component {
  state = {
    content: "",
    result: "",
  };

  // componentDidMount = async () => {
  //   this.web3 = await getWeb3();

  //   // this.bias = convertNum(model.intercept, this.web3, 1e9);
  //   // this.weights = convertData(model.weights, this.web3, 1e9);

  //   this.weights = model.weights;
  //   this.bias = model.intercept;
  //   this.learningRate = model.learningRate;
  // };

  handleChange = (e) => {
    this.setState({
      content: e.target.value,
    });
  };

  predict = () => {
    const { weights, intercept: bias } = model;

    const rawData = this.state.content;

    const data = this.transformInput(rawData);
    console.log(data);
    let sum = bias;
    for (let i = 0; i < data.length; i++) {
      if (data[i] > 1000) {
        continue;
      }
      sum += weights[data[i]];
    }

    console.log(sum);

    if (sum <= 0) {
      this.setState({ result: "negative" });
    } else {
      this.setState({ result: "positive" });
    }
  };

  // initializeWeights = (startIndex, _weights) => {
  //   for (let i = 0; i < _weights.length; ++i) {
  //     this.weights[startIndex + i] = _weights[i];
  //   }
  // };

  transformInput = (content) => {
    const words = content.toLocaleLowerCase("en").split(/[\s+,]/);
    console.log(words);
    return words.map((word) => {
      let idx = wordIndex[word];
      if (idx === undefined) {
        return 1337;
      }
      return idx;
    });
    // .map((v) => this.web3.utils.toHex(v));
  };

  render() {
    return (
      <div className="test-body">
        <div className="interact-area">
        <textarea type="text" onChange={(e) => this.handleChange(e)} />
        <button onClick={this.predict}>Predict</button>
        </div>
        <div className="result">{this.state.result}</div>
      </div>
    );
  }
}
