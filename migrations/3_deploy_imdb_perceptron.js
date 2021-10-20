const fs = require("fs");
const { convertNum, convertData } = require("../client/src/utils/float.js");
const ImdbPerceptron = artifacts.require("./ImdbPerceptron.sol");

module.exports = function (deployer, accounts) {
  const toFloat = 1e9;

  // the path should be relative to the root path of the project
  const data = fs.readFileSync("./models/imdb-sentiment-model.json", "utf8");
  const model = JSON.parse(data);
  const weights = convertData(model.weights, web3, toFloat);
  const initNumWords = 250;
  const numWordsPerUpdate = 250;

  console.log(`Deploying IMDB model with ${weights.length} weights.`);
  const intercept = convertNum(model.intercept || model.bias, web3, toFloat);
  const learningRate = convertNum(model.learningRate, web3, toFloat);

  deployer
    .deploy(
      ImdbPerceptron,
      weights.slice(0, initNumWords),
      intercept,
      learningRate,
      { gas: 7.9e6, overwrite: false }
    )
    .then(async (classifier) => {
      console.log(`  Deployed classifier to ${classifier.address}.`);
      for (let i = initNumWords; i < weights.length; i += numWordsPerUpdate) {
        await classifier.initializeWeights(
          i,
          weights.slice(i, i + numWordsPerUpdate),
          { gas: 7.9e6 }
        );
        console.log(`  Added ${i + numWordsPerUpdate} weights.`);
      }
    });
};
