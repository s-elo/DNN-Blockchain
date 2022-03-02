const PureDnn = artifacts.require("./PureDnn.sol");

module.exports = function (deployer, network, accounts) {
  deployer.deploy(PureDnn, { from: accounts[0], overwrite: true });
};
