const IpArray = artifacts.require("./IpArray.sol");

module.exports = function (deployer, network, accounts) {
  deployer.deploy(IpArray, { from: accounts[0] });
};
