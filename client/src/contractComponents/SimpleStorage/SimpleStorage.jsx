import React, { Component } from "react";
import SimpleStorageContract from "@/contracts/SimpleStorage.json";
import getWeb3 from "@/utils/getWeb3";
import "./SimpleStorage.less";

class SimpleStorage extends Component {
  state = {
    storageValue: "Loading...",
    web3: null,
    accounts: null,
    contract: null,
    isLoad: false,
  };

  inputValue = 0;

  componentDidMount = async () => {
    try {
      // Get network provider and web3 instance.
      const web3 = await getWeb3();

      // Use web3 to get the user's accounts.
      const accounts = await web3.eth.getAccounts();
      // console.log("current accounts:", accounts);

      // Get the contract instance.
      const networkId = await web3.eth.net.getId();
      // console.log("current networkId:", networkId);

      const deployedNetwork = SimpleStorageContract.networks[networkId];

      const instance = new web3.eth.Contract(
        SimpleStorageContract.abi,
        deployedNetwork && deployedNetwork.address
      );

      // Set web3, accounts, and contract to the state, and then proceed with an
      // example of interacting with the contract's methods.
      this.setState({ web3, accounts, contract: instance }, async () => {
        // Get the value from the contract to prove it worked.
        const response = await instance.methods.get().call();

        this.inputValue = response;

        // Update state with the result.
        this.setState({ storageValue: response, isLoad: true });
      });
    } catch (error) {
      // Catch any errors for any of the above operations.
      alert(
        `Failed to load web3, accounts, or contract. Check console for details.`
      );
      console.error(error);
    }
  };

  setValue = () => {
    if (!window.confirm("sure to set the value?")) return;

    const { accounts, contract } = this.state;

    // Stores a given value
    this.inputValue !== ""
      ? contract.methods
          .set(this.inputValue)
          .send({ from: accounts[0] })
          .then(async () => {
            // Get the value from the contract to prove it worked.
            const response = await contract.methods.get().call();

            this.inputValue = response;

            // Update state with the result.
            this.setState({ storageValue: response });
          })
      : alert("cannot be blank");

    this.setState({ storageValue: "Setting..." });
  };

  valueChange = (e) => {
    this.inputValue = e.target.value.trim();
  };

  render() {
    if (!this.state.web3) {
      return <div>Loading Web3, accounts, and contract...</div>;
    }
    return (
      <div className="simple-storage-body">
        <input type="text" onChange={(e) => this.valueChange(e)} />
        <button onClick={this.setValue}>Set value</button>
        <div className="show-value">
          Current value: {this.state.storageValue}
        </div>
      </div>
    );
  }
}

export default SimpleStorage;
