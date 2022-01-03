var SingleModelStorage = artifacts.require("./SingleModelStorage.sol");

module.exports = function (deployer, network, accounts) {
  console.log(network);
  deployer.deploy(SingleModelStorage, { from: accounts[0] });
};
