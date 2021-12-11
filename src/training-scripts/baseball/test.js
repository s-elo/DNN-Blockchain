const path = require("path");
const tf = require("@tensorflow/tfjs-node-gpu");

const { csvTransform } = require("./dataHandler.js");

const MODEL_PATH = path.resolve(
  __dirname,
  "../../",
  "models/baseball/model.json"
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
    const values = model.predict(pitchTypeBatch.xs).dataSync();
   
    console.log(pitchTypeBatch.ys);
    console.log(values.length);
  });
})();
