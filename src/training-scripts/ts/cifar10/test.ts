import { getSingleImgTensor } from "./dataHandler";
import * as tf from "@tensorflow/tfjs-node-gpu";

async function timeEvaluator(fn: any, ...args: any) {
  const startTime = Date.now();
  const ret = await fn(...args);
  const endTime = Date.now();
  console.log(`Run time: ${(endTime - startTime) / 1000} S`);

  return ret;
}

(async () => {
  // const {imgs: testData, labels: testLabel} = await timeEvaluator(getDataSet, 'TEST');

  // console.log(testLabel.length);

  // const {imgs: trainData, labels: trainLabel} = await timeEvaluator(getDataSet, 'TRAIN');

  // console.log(trainLabel.length);
  test2();
})();

async function test() {
  const xArray = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
  ];
  const yArray = [1, 1, 1, 1];
  // Create a dataset from the JavaScript array.
  const xDataset = tf.data.array(xArray);
  const yDataset = tf.data.array(yArray);
  // Zip combines the `x` and `y` Datasets into a single Dataset, the
  // iterator of which will return an object containing of two tensors,
  // corresponding to `x` and `y`.  The call to `batch(4)` will bundle
  // four such samples into a single object, with the same keys now pointing
  // to tensors that hold 4 examples, organized along the batch dimension.
  // The call to `shuffle(4)` causes each iteration through the dataset to
  // happen in a different order.  The size of the shuffle window is 4.
  const xyDataset = tf.data
    .zip({ xs: xDataset, ys: yDataset })
    .batch(4)
    .shuffle(4);
  const model = tf.sequential({
    layers: [tf.layers.dense({ units: 1, inputShape: [9] })],
  });
  model.compile({ optimizer: "sgd", loss: "meanSquaredError" });
  const history = await model.fitDataset(xyDataset, {
    epochs: 4,
    callbacks: { onEpochEnd: (epoch, logs) => console.log(logs?.loss) },
  });
}

async function test2() {
  const c = tf.data
    .array([
      { a: 1, b: 11 },
      { a: 2, b: 12 },
      { a: 3, b: 13 },
      { a: 4, b: 14 },
      { a: 5, b: 15 },
      { a: 6, b: 16 },
      { a: 7, b: 17 },
      { a: 8, b: 18 },
    ])
    .batch(4);
  await c.forEachAsync((e) => {
    console.log("{");
    for (var key in e as any) {
      console.log(key + ":");
      (e as any)[key].print();
    }
    console.log("}");
  });
}
