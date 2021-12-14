import * as tf from "@tensorflow/tfjs-node-gpu";

import { saveModel } from "./utils";
import { csvTransform } from "./dataHandler";

// data can be loaded from URLs or local file paths when running in Node.js.
const TRAIN_DATA_PATH =
  "https://storage.googleapis.com/mlb-pitch-data/pitch_type_training_data.csv";
const TEST_DATA_PATH =
  "https://storage.googleapis.com/mlb-pitch-data/pitch_type_test_data.csv";

const NUM_PITCH_CLASSES = 7;
const TRAINING_DATA_LENGTH = 7000;
const TEST_DATA_LENGTH = 700;

const trainingData = tf.data
  .csv(TRAIN_DATA_PATH, { columnConfigs: { pitch_code: { isLabel: true } } })
  .map(csvTransform)
  .shuffle(TRAINING_DATA_LENGTH)
  .batch(100);

// Load all training data in one batch to use for evaluation
const trainingValidationData = tf.data
  .csv(TRAIN_DATA_PATH, { columnConfigs: { pitch_code: { isLabel: true } } })
  .map(csvTransform)
  .batch(TRAINING_DATA_LENGTH);

// Load all test data in one batch to use for evaluation
const testValidationData = tf.data
  .csv(TEST_DATA_PATH, { columnConfigs: { pitch_code: { isLabel: true } } })
  .map(csvTransform)
  .batch(TEST_DATA_LENGTH);

const model = tf.sequential();
model.add(tf.layers.dense({ units: 250, activation: "relu", inputShape: [8] }));
model.add(tf.layers.dense({ units: 175, activation: "relu" }));
model.add(tf.layers.dense({ units: 150, activation: "relu" }));
model.add(tf.layers.dense({ units: NUM_PITCH_CLASSES, activation: "softmax" }));

model.compile({
  optimizer: tf.train.adam(),
  loss: "sparseCategoricalCrossentropy",
  metrics: ["accuracy"],
});

// Returns pitch class evaluation percentages for training data
// with an option to include test data
async function evaluate(useTestData: boolean) {
  let results = {};
  await trainingValidationData.forEachAsync((pitchTypeBatch) => {
    const values = (
      model.predict((pitchTypeBatch as any).xs) as tf.Tensor2D
    ).dataSync();
    const classSize = TRAINING_DATA_LENGTH / NUM_PITCH_CLASSES;
    for (let i = 0; i < NUM_PITCH_CLASSES; i++) {
      (results as any)[pitchFromClassNum(i)] = {
        training: calcPitchClassEval(i, classSize, values),
      };
    }
  });

  if (useTestData) {
    await testValidationData.forEachAsync((pitchTypeBatch) => {
      const values = (
        model.predict((pitchTypeBatch as any).xs) as tf.Tensor2D
      ).dataSync();
      const classSize = TEST_DATA_LENGTH / NUM_PITCH_CLASSES;
      for (let i = 0; i < NUM_PITCH_CLASSES; i++) {
        (results as any)[pitchFromClassNum(i)].validation = calcPitchClassEval(
          i,
          classSize,
          values
        );
      }
    });
  }
  return results;
}

async function predictSample(sample: number[]) {
  let result = (
    model.predict(tf.tensor(sample, [1, sample.length])) as tf.Tensor2D
  ).arraySync();
  var maxValue = 0;
  var predictedPitch = 7;
  for (var i = 0; i < NUM_PITCH_CLASSES; i++) {
    if (result[0][i] > maxValue) {
      predictedPitch = i;
      maxValue = result[0][i];
    }
  }
  return pitchFromClassNum(predictedPitch);
}

// Determines accuracy evaluation for a given pitch class by index
function calcPitchClassEval(
  pitchIndex: number,
  classSize: number,
  values: Float32Array | Int32Array | Uint8Array
) {
  // Output has 7 different class values for each pitch, offset based on
  // which pitch class (ordered by i)
  let index = pitchIndex * classSize * NUM_PITCH_CLASSES + pitchIndex;
  let total = 0;
  for (let i = 0; i < classSize; i++) {
    total += values[index];
    index += NUM_PITCH_CLASSES;
  }
  return total / classSize;
}

// Returns the string value for Baseball pitch labels
function pitchFromClassNum(classNum: number) {
  switch (classNum) {
    case 0:
      return "Fastball (2-seam)";
    case 1:
      return "Fastball (4-seam)";
    case 2:
      return "Fastball (sinker)";
    case 3:
      return "Fastball (cutter)";
    case 4:
      return "Slider";
    case 5:
      return "Changeup";
    case 6:
      return "Curveball";
    default:
      return "Unknown";
  }
}

const TIMEOUT_BETWEEN_EPOCHS_MS = 500;
// util function to sleep for a given ms
function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function train() {
  let numTrainingIterations = 10;
  for (var i = 0; i < numTrainingIterations; i++) {
    console.log(`Training iteration : ${i + 1} / ${numTrainingIterations}`);
    await model.fitDataset(trainingData, { epochs: 1 });
    // console.log("accuracyPerClass", await pitch_type.evaluate(true));
    await sleep(TIMEOUT_BETWEEN_EPOCHS_MS);
  }

  saveModel(model);
}

train();
