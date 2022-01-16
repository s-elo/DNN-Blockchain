const StrStorage = artifacts.require("./StrStorage.sol");

module.exports = function (deployer, network, accounts) {
  deployer.deploy(StrStorage, { from: accounts[0], overwrite: false });
};
