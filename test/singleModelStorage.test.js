const SingleModelStorage = artifacts.require("./SingleModelStorage.sol");
const fs = require("fs");

contract("SingleModelStorage", (accounts) => {
  const new_model = fs.readFileSync("./test/imdb.json");

  console.log(new_model.length);

  it(`...should store the model.`, async () => {
    const singleModelStorageInstance = await SingleModelStorage.deployed();

    const len = 5000;
    const multiNum = 1;

    const multiModel = (model) =>
      Array(multiNum)
        .fill(0)
        .reduce((sumModel) => sumModel + model, "");

    const multied = multiModel(new_model);
    console.log("multied len: ", multied.length);

    // await singleModelStorageInstance.initModel(multied.length);

    console.log('initialized...');

    const setNum = multied.length / len;
    console.log(setNum);
    for (let i = 0; i < setNum; i++) {
      const chunk = multied.slice(i * len, i * len + len);

      const bytes = [...new TextEncoder("utf-8").encode(chunk)];

      console.log("chunk len: ", bytes.length, bytes.slice(0, 5));

      // Set model
      await singleModelStorageInstance.set(chunk, i, {
        from: accounts[0],
        // gasLimit: 80000000000000000000000,
      });
    }

    // Get model
    let model = await singleModelStorageInstance.get.call();
    console.log(model.length);

    assert.equal(model, multied, "length not match");
  });
});
