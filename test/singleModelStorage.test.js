const SingleModelStorage = artifacts.require("./SingleModelStorage.sol");

contract("SingleModelStorage", (accounts) => {
  const new_model = "test";

  it(`...should store the model ${new_model}.`, async () => {
    const singleModelStorageInstance = await SingleModelStorage.deployed();

    // Set model
    await singleModelStorageInstance.set(new_model, { from: accounts[0] });

    // Get model
    const model = await singleModelStorageInstance.get.call();
    console.log(model);
    assert.equal(model, new_model, `The model ${new_model} was not stored.`);
  });
});
