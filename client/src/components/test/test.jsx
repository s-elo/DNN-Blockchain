import React, { Component } from "react";
import getWeb3 from "@/utils/getWeb3";
import ImdbModelContract from "../../contracts/ImdbPerceptron.json";
import wordIndex from "./imdb.json";
import "./test.less";

export default class Test extends Component {
  state = {
    content: "",
    result: "",
    classification: 0
  };

  componentDidMount = async () => {
    this.web3 = await getWeb3();

    this.accounts = await this.web3.eth.getAccounts();

    const networkId = await this.web3.eth.net.getId();

    const deployedNetwork = ImdbModelContract.networks[networkId];

    this.model = new this.web3.eth.Contract(
      ImdbModelContract.abi,
      deployedNetwork && deployedNetwork.address
    );
  };

  handleChange = (e) => {
    this.setState({
      content: e.target.value,
    });
  };

  predict = async () => {
    const rawData = this.state.content;

    const data = this.transformInput(rawData);
    // console.log(data);

    const result = await this.model.methods.predict(data).call();
    // console.log(result);
    if (Number(result) === 0) {
      this.setState({ result: "negative" });
    } else {
      this.setState({ result: "positive" });
    }
  };

  train = async () => {
    const { classification } = this.state;

    const rawData = this.state.content;
    const data = this.transformInput(rawData);

    await this.model.methods
      .update(data, classification)
      .send({ from: this.accounts[0] });

    alert("sent");
  };

  transformInput = (content) => {
    const words = content.toLocaleLowerCase("en").split(/[\s+,]/);

    return words
      .map((word) => {
        let idx = wordIndex[word];
        if (idx === undefined) {
          return 1337;
        }
        return idx;
      })
      .map((v) => this.web3.utils.toHex(v));
  };

  selectionChange = (e) => {
    this.setState({
      classification: Number(e.target.value),
    });
  };

  render() {
    return (
      <div className="test-body">
        <div className="interact-area">
          <textarea type="text" onChange={(e) => this.handleChange(e)} />
          <div className="btn">
            <button onClick={this.predict}>Predict</button>
            <select onChange={(e) => this.selectionChange(e)}>
              <option value="1">positive</option>
              <option value="0">negative</option>
            </select>
            <button onClick={this.train}>Train</button>
          </div>
        </div>
        <div className="result">{this.state.result}</div>
      </div>
    );
  }
}
