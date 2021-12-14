import * as tf from "@tensorflow/tfjs-node-gpu";
import path from "path";
import { plot, Plot } from "nodeplotlib";
import {
  convertToTensor,
  getData,
  InputData,
  NormalizedData,
} from "./dataHandler";

const MODEL_PATH = path.resolve(__dirname, ".", "models/model.json");

(async () => {
  const model = await tf.loadLayersModel(`file://${MODEL_PATH}`);
  const data = await getData();

  testModel(model, data, convertToTensor(data));
  // test(data, model);
})();

function test(dataset: Array<InputData>, model: tf.LayersModel) {
  const { inputs, inputMax, inputMin, labelMin, labelMax } =
    convertToTensor(dataset);

  const preds = model.predict(inputs);

  const unNormPreds = [
    ...(preds as tf.Tensor1D)
      .mul(labelMax.sub(labelMin))
      .add(labelMin)
      .dataSync(),
  ]; // get real data using dataSync tensor -> array

  const originalInputs = dataset.map((data) => data.horsepower);
  const originalLabels = dataset.map((data) => data.mpg);

  const data: Plot[] = [
    {
      x: originalInputs,
      y: originalLabels,
      mode: "markers",
      type: "scatter",
    },
    {
      x: originalInputs,
      y: unNormPreds,
      mode: "markers",
      type: "scatter",
    },
  ];

  plot(data);
}

function testModel(
  model: tf.LayersModel,
  inputData: Array<InputData>,
  normalizationData: NormalizedData
) {
  const { inputMax, inputMin, labelMin, labelMax } = normalizationData;

  // Generate predictions for a uniform range of numbers between 0 and 1;
  // We un-normalize the data by doing the inverse of the min-max scaling
  // that we did earlier.
  const [xs, preds] = tf.tidy(() => {
    // 0-1 100 points
    const xs = tf.linspace(0, 1, 100);
    const preds = model.predict(xs.reshape([100, 1]));

    const unNormXs = xs.mul(inputMax.sub(inputMin)).add(inputMin);

    const unNormPreds = (preds as tf.Tensor1D)
      .mul(labelMax.sub(labelMin))
      .add(labelMin);

    // Un-normalize the data
    return [unNormXs.dataSync(), unNormPreds.dataSync()];
  });

  const unNormXs = [...xs];
  const unNormPreds = [...preds];
  const originalInputs = inputData.map((data) => data.horsepower);
  const originalLabels = inputData.map((data) => data.mpg);

  const data: Plot[] = [
    {
      x: originalInputs,
      y: originalLabels,
      mode: "markers",
      type: "scatter",
    },
    {
      x: unNormXs,
      y: unNormPreds,
      mode: "markers",
      type: "scatter",
    },
  ];

  plot(data);
}
