import * as tf from "@tensorflow/tfjs-node-gpu";

import { saveModel } from "./utils";
import { convertToTensor, getData } from "./dataHandler";

function createModel() {
  // Create a sequential model
  const model = tf.sequential();

  // Add a single input layer
  // inputShape: only one feature
  // units: like how many neurons
  model.add(tf.layers.dense({ inputShape: [1], units: 1, useBias: true }));

  // add one more hidden layer with 50 neurons
  model.add(tf.layers.dense({ units: 50, activation: "sigmoid" }));
  model.add(tf.layers.dense({ units: 50, activation: "sigmoid" }));

  // Add an output layer
  model.add(tf.layers.dense({ units: 1, useBias: true }));

  return model;
}

async function trainModel(
  model: tf.Sequential,
  inputs: tf.Tensor<tf.Rank>,
  labels: tf.Tensor<tf.Rank>
) {
  // Prepare the model for training.
  model.compile({
    optimizer: tf.train.adam(),
    loss: tf.losses.meanSquaredError,
    metrics: ["mse"],
  });

  const batchSize = 32;
  const epochs = 50;

  return await model.fit(inputs, labels, {
    batchSize,
    epochs,
    shuffle: true,
    callbacks: tf.node.tensorBoard("./fit_logs_1"),
  });
}

(async () => {
  const dataset = await getData();
  //   console.log(dataset);

  // Create the model
  const model = createModel();

  // Convert the data to a form we can use for training.
  const tensorData = convertToTensor(dataset);
  const { inputs, labels } = tensorData;

  // Train the model
  await trainModel(model, inputs, labels);
  console.log("Done Training");

  saveModel("carPower", model);
})();
