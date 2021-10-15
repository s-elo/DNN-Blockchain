const path = require("path");
const HDWalletProvider = require("@truffle/hdwallet-provider");
// wallet private key, do not upload to the git
const mnemonic = require("./walletPrivateKey.js");

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  contracts_build_directory: path.join(__dirname, "client/src/contracts"),
  // can choose different network
  networks: {
    develop: {
      host: "http://127.0.0.1",
      port: 8545,
    },
    rinkeby: {
      provider: function () {
        return new HDWalletProvider(
          mnemonic,
          "https://rinkeby.infura.io/v3/54d59d27fdba4440a993e552028b900a"
        );
      },
      network_id: 4,
      gas: 4500000,
      gasPrice: 10000000000,
    },
    ropsten: {
      provider: function () {
        return new HDWalletProvider(
          mnemonic,
          "https://ropsten.infura.io/v3/ab53629910c440089fda82f82af645f7"
        );
      },
      network_id: 3,
      gas: 4500000,
      gasPrice: 10000000000,
    },
    kovan: {
      provider: function () {
        return new HDWalletProvider(
          mnemonic,
          "https://kovan.infura.io/v3/f14d62f059e54d38be636f755bca00e4"
        );
      },
      network_id: 42,
      gas: 4500000,
      gasPrice: 10000000000,
    },
  },
};
