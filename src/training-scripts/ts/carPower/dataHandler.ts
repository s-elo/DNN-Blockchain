import * as tf from "@tensorflow/tfjs-node-gpu";
import axios from "axios";

export interface InputData {
  horsepower: number;
  mpg: number;
}

interface RemoteData {
  Miles_per_Gallon: number;
  Horsepower: number;
}

export interface NormalizedData {
  inputs: tf.Tensor<tf.Rank>;
  labels: tf.Tensor<tf.Rank>;
  inputMax: tf.Tensor<tf.Rank>;
  inputMin: tf.Tensor<tf.Rank>;
  labelMax: tf.Tensor<tf.Rank>;
  labelMin: tf.Tensor<tf.Rank>;
}
/**
 * Convert the input data to tensors that we can use for machine
 * learning. We will also do the important best practices of _shuffling_
 * the data and _normalizing_ the data
 * MPG on the y-axis.
 */
export function convertToTensor(data: Array<InputData>) {
  // Wrapping these calculations in a tidy will dispose any
  // intermediate tensors.

  return tf.tidy(() => {
    // Step 1. Shuffle the data
    tf.util.shuffle(data);

    // Step 2. Convert data to Tensor
    const inputs = data.map((d) => d.horsepower);
    const labels = data.map((d) => d.mpg);

    // inputTensor: (sample_num, feature_num)
    const inputTensor = tf.tensor2d(inputs, [inputs.length, 1]);
    const labelTensor = tf.tensor2d(labels, [labels.length, 1]);

    //Step 3. Normalize the data to the range 0 - 1 using min-max scaling
    const inputMax = inputTensor.max();
    const inputMin = inputTensor.min();
    const labelMax = labelTensor.max();
    const labelMin = labelTensor.min();

    const normalizedInputs = inputTensor
      .sub(inputMin)
      .div(inputMax.sub(inputMin));
    const normalizedLabels = labelTensor
      .sub(labelMin)
      .div(labelMax.sub(labelMin));

    return {
      inputs: normalizedInputs,
      labels: normalizedLabels,
      // Return the min/max bounds so we can use them later.
      inputMax,
      inputMin,
      labelMax,
      labelMin,
    };
  });
}

export async function getData() {
  const carsDataResponse = await axios.get(
    "https://storage.googleapis.com/tfjs-tutorials/carsData.json"
  );

  const carsData = carsDataResponse.data as Array<RemoteData>;

  const cleaned = carsData
    .map((car) => ({
      mpg: car.Miles_per_Gallon,
      horsepower: car.Horsepower,
    }))
    .filter((car) => car.mpg != null && car.horsepower != null);

  return cleaned;
}
