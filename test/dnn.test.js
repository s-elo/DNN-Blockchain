const Dnn = artifacts.require("./Dnn.sol");

contract("Dnn", (accounts) => {
  it("...should add a new model", async () => {
    const dnn = await Dnn.deployed();

    await dnn.addNewModel("cifar10", "ipfs hash", "testset hash", "50%", 5);

    const modelInfo = await dnn.getModelInfo.call("cifar10");

    const expRet = ["ipfs hash", "testset hash", "50%"];

    for (const [idx, info] of modelInfo.entries()) {
      assert.equal(info, expRet[idx], "The model info is not right.");
    }
  });
});
