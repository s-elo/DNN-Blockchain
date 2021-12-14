import path from "path";
import * as tf from "@tensorflow/tfjs-node-gpu";

import { csvTransform } from "./dataHandler";

const MODEL_PATH = path.resolve(
  __dirname,
  ".",
  "models/model.json"
);

const TEST_DATA_PATH =
  "https://storage.googleapis.com/mlb-pitch-data/pitch_type_test_data.csv";
const TEST_DATA_LENGTH = 700;

// Load all test data in one batch to use for evaluation
const testValidationData = tf.data
  .csv(TEST_DATA_PATH, { columnConfigs: { pitch_code: { isLabel: true } } })
  .map(csvTransform)
  .batch(TEST_DATA_LENGTH);

(async () => {
  const model = await tf.loadLayersModel(`file://${MODEL_PATH}`);

  await testValidationData.forEachAsync((pitchTypeBatch) => {
    const values = (
      model.predict((pitchTypeBatch as any).xs) as tf.Tensor2D
    ).dataSync();

    console.log((pitchTypeBatch as any).ys);
    console.log(values.length);
  });
})();
