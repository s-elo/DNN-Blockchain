import React, { Component } from "react";
import params from "./weights.json";
import wordIndex from "./word_index.json";
import "./test.less";

export default class Test extends Component {
  state = {
    content: "",
    result: ''
  };

  handleChange = (e) => {
    this.setState({
      content: e.target.value,
    });
  };

  predict = () => {
    const { w, b } = params;
    const rawData = this.state.content.split(/[\s\,]/);

    const data = this.processWords(rawData);

    let sum = 0;
    for (let i = 0; i < data.length; i++) {
      sum += w[i] * data[i];
    }

    sum += b;   
    console.log(sum);
    if (sum > 0.5) {
      this.setState({result: 'positive'});
    } else {
      this.setState({result: 'negative'});
    }
  };

  processWords(words) {
    const processData = new Array(1000).fill(0);

    for (const word of words) {
      const index = wordIndex[word];
      if (index && index < 1000) {
        processData[index] = 1;
      }
    }

    return processData;
  }

  render() {
    return (
      <div className="test-body">
        <textarea type="text" onChange={(e) => this.handleChange(e)} />
        <button onClick={this.predict}>Predict</button>
        <div className="result">{this.state.result}</div>
      </div>
    );
  }
}
