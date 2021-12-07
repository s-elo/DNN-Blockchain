const ImdbPerceptron = artifacts.require("./ImdbPerceptron");
const fs = require("fs");
const Web3 = require("web3");

const web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));

const transformInput = (content) => {
  const words = content.toLocaleLowerCase("en").split(/[\s+,]/);
  // relative to the root path!
  const wordIndex = JSON.parse(fs.readFileSync("./test/imdb.json", "utf8"));

  return words
    .map((word) => {
      let idx = wordIndex[word];
      if (idx === undefined) {
        return 1337;
      }
      return idx;
    })
    .map((v) => web3.utils.toHex(v));
};

contract("ImdbPerceptron", (account) => {
  it("...should predict as positive", async () => {
    const ImdbPerceptronInstance = await ImdbPerceptron.deployed();

    const data = transformInput(`this is a nice movie`);

    const prediction = await ImdbPerceptronInstance.predict.call(data);

    assert.equal(Number(prediction), 1, "The prediction is wrong...");
  });

  it("...should predict as negative", async () => {
    const ImdbPerceptronInstance = await ImdbPerceptron.deployed();

    const data = transformInput(`this is a bad movie`);

    const prediction = await ImdbPerceptronInstance.predict.call(data);

    assert.equal(Number(prediction), 0, "The prediction is wrong...");
  });
});
