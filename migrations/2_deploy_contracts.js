var SimpleStorage = artifacts.require("./SimpleStorage.sol");

module.exports = function (deployer, network, accounts) {
  console.log(network);
  deployer.deploy(SimpleStorage, { from: accounts[0], overwrite: false });
};
