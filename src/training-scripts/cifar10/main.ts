import { install } from "./install";

// console.log("Installing packages...");

// try {
//   install(["@tensorflow/tfjs-node-gpu", "fs-extra", "axios"]);
// } catch (err) {
//   console.log(err);
// }

// console.log("Installation done!");

import * as tf from "@tensorflow/tfjs-node-gpu";
import path from "path";
import fs from "fs";
import {
  getDataSet,
  CLASS_NAMES,
  IMAGE_WIDTH,
  IMAGE_HEIGHT,
  IMAGE_CHANNELS,
  BATCH_SIZE,
} from "./dataHandler";

function getModel() {
  const model = tf.sequential();

  // In the first layer of our convolutional neural network we have
  // to specify the input shape. Then we specify some parameters for
  // the convolution operation that takes place in this layer.
  model.add(
    tf.layers.conv2d({
      inputShape: [IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS],
      kernelSize: 5,
      filters: 8,
      strides: 1,
      activation: "relu",
      kernelInitializer: "varianceScaling",
    })
  );

  // The MaxPooling layer acts as a sort of downsampling using max values
  // in a region instead of averaging.
  model.add(tf.layers.maxPooling2d({ poolSize: [2, 2], strides: [2, 2] }));

  // Repeat another conv2d + maxPooling stack.
  // Note that we have more filters in the convolution.
  model.add(
    tf.layers.conv2d({
      kernelSize: 5,
      filters: 16,
      strides: 1,
      activation: "relu",
      kernelInitializer: "varianceScaling",
    })
  );
  model.add(tf.layers.maxPooling2d({ poolSize: [2, 2], strides: [2, 2] }));

  // Now we flatten the output from the 2D filters into a 1D vector to prepare
  // it for input into our last layer. This is common practice when feeding
  // higher dimensional data to a final classification output layer.
  model.add(tf.layers.flatten());

  // Our last layer is a dense layer which has 10 output units, one for each
  // output class (i.e. 0, 1, 2, 3, 4, 5, 6, 7, 8, 9).
  model.add(
    tf.layers.dense({
      units: CLASS_NAMES.length,
      kernelInitializer: "varianceScaling",
      activation: "softmax",
    })
  );

  // Choose an optimizer, loss function and accuracy metric,
  // then compile and return the model
  const optimizer = tf.train.adam();
  model.compile({
    optimizer: optimizer,
    loss: "categoricalCrossentropy",
    metrics: ["accuracy"],
  });

  return model;
}

async function train() {
  console.log(`Loading data...`);

  const { imgs: trainData, labels: trainLabel } = await getDataSet("TRAIN");
  const { imgs: testData, labels: testLabel } = await getDataSet("TEST");

  console.log(`data Loaded`);
  console.log(trainData, trainLabel);

  const model = getModel();

  return model.fit(trainData, trainLabel, {
    batchSize: BATCH_SIZE,
    validationData: [testData, testLabel],
    epochs: 10,
    shuffle: true,
    // callbacks: fitCallbacks
  });
}

train();


// const evalOutput = model.evaluate(testImages, testLabels);