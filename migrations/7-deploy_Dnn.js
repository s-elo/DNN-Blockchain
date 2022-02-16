const Dnn = artifacts.require("./Dnn.sol");

module.exports = function (deployer, network, accounts) {
  deployer.deploy(Dnn, { from: accounts[0], overwrite: true });
};
