const PureDnn = artifacts.require("./PureDnn.sol");

contract("PureDnn", (accounts) => {
  it("...should work", async () => {
    const dnn = await PureDnn.deployed();

    await dnn.addNewModel("cifar10", "ipfs hash", "testset hash", "50%");

    const modelInfo = await dnn.getModelInfo.call("cifar10");

    const expRet = ["ipfs hash", "testset hash", "50%"];

    for (const [idx, info] of modelInfo.entries()) {
      assert.equal(info, expRet[idx], "The model info is not right.");
    }

    const modelHash = await dnn.getModelHash.call('cifar10');
    const testsetHash = await dnn.getTestsetHash.call('cifar10');

    assert.equal(modelHash, 'ipfs hash', 'model hash not right');
    assert.equal(testsetHash, 'testset hash', 'testset has not right');

    await dnn.addNode('cifar10', 'node1_addr');
    await dnn.addNode('cifar10', 'node2_addr');

    // add one more time see if it is convered (shouldnt convered)
    await dnn.addNewModel("cifar10", "ipfs hash", "testset hash", "50%");

    const nodes = await dnn.getNodes.call('cifar10');

    assert.equal(nodes[0], 'node1_addr', "failed to add a node.");
    assert.equal(nodes[1], 'node2_addr', "failed to add a node.");

    await dnn.clearNodes('cifar10');

    const afterClearNodes = await dnn.getNodes.call('cifar10');

    assert.equal(afterClearNodes.length, 0, "failed to clear nodes.");

    await dnn.updateModel('cifar10', 'new model hash');

    await dnn.updateTestset('cifar10', 'new testset hash');

    const newModelInfo = await dnn.getModelInfo.call("cifar10");

    assert.equal(newModelInfo[0], 'new model hash', 'can not update model');
    assert.equal(newModelInfo[1], 'new testset hash', 'can not update testset');
  });
});
