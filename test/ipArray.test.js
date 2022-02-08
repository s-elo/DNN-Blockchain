const IpArray = artifacts.require("./IpArray.sol");

contract("IpArray", (accounts) => {
  it("...should add to the array.", async () => {
    const ipArray = await IpArray.deployed();

    const prevNodes = await ipArray.getNodes.call();

    await ipArray.addNode("localhost", { from: accounts[0] });

    const curNodes = await ipArray.getNodes.call();

    console.log(prevNodes, curNodes);

    assert.equal(
      curNodes.length,
      prevNodes.length + 1,
      "The array length is not right."
    );
  });

  it("...it should clear the array", async () => {
    const ipArray = await IpArray.deployed();

    await ipArray.clearNodes({ from: accounts[0] });

    const curNodes = await ipArray.getNodes.call();
    console.log(curNodes);

    assert.equal(curNodes.length, 0, "The array has not been cleared");
  });
});
