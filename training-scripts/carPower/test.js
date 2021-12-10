const tf = require("@tensorflow/tfjs-node-gpu");
const path = require("path");
const plotly = require("plotly")("leo666", "9TTpbOGbgjSt7Q7zooIi");

const { getData, convertToTensor } = require("./dataHandler.js");

const MODEL_PATH = path.resolve(
  __dirname,
  "../../",
  "models/carPower/model.json"
);

(async () => {
  const model = await tf.loadLayersModel(`file://${MODEL_PATH}`);
  const data = await getData();

  testModel(model, data, convertToTensor(data));
  // test(data, model);
})();

function test(dataset, model) {
  const { inputs, inputMax, inputMin, labelMin, labelMax } =
    convertToTensor(dataset);

  const preds = model.predict(inputs);

  const unNormPreds = [
    ...preds.mul(labelMax.sub(labelMin)).add(labelMin).dataSync(),
  ]; // get real data using dataSync tensor -> array
  console.log(unNormPreds);
  const originalInputs = dataset.map((data) => data.horsepower);
  const originalLabels = dataset.map((data) => data.mpg);
}

function testModel(model, inputData, normalizationData) {
  const { inputMax, inputMin, labelMin, labelMax } = normalizationData;

  // Generate predictions for a uniform range of numbers between 0 and 1;
  // We un-normalize the data by doing the inverse of the min-max scaling
  // that we did earlier.
  const [xs, preds] = tf.tidy(() => {
    // 0-1 100 points
    const xs = tf.linspace(0, 1, 100);
    const preds = model.predict(xs.reshape([100, 1]));

    const unNormXs = xs.mul(inputMax.sub(inputMin)).add(inputMin);

    const unNormPreds = preds.mul(labelMax.sub(labelMin)).add(labelMin);

    // Un-normalize the data
    return [unNormXs.dataSync(), unNormPreds.dataSync()];
  });

  const unNormXs = [...xs];
  const unNormPreds = [...preds];
  const originalInputs = inputData.map((data) => data.horsepower);
  const originalLabels = inputData.map((data) => data.mpg);

  plot(originalInputs, originalLabels, unNormXs, unNormPreds);
  //   tfvis.render.scatterplot(
  //     { name: "Model Predictions vs Original Data" },
  //     {
  //       values: [originalPoints, predictedPoints],
  //       series: ["original", "predicted"],
  //     },
  //     {
  //       xLabel: "Horsepower",
  //       yLabel: "MPG",
  //       height: 300,
  //     }
  //   );
}

function plot(originalInputs, originalLabels, unNormXs, unNormPreds) {
  const trace1 = {
    x: originalInputs,
    y: originalLabels,
    mode: "markers",
    name: "original points",
    // text: ["United States", "Canada"],
    marker: {
      color: "rgb(164, 194, 244)",
      size: 12,
      line: {
        color: "white",
        width: 0.5,
      },
    },
    type: "scatter",
  };

  const trace2 = {
    x: unNormXs,
    y: unNormPreds,
    mode: "markers",
    name: "predictive points",
    // text: ["United States", "Canada"],
    marker: {
      color: "rgb(255, 217, 102)",
      size: 12,
      line: {
        color: "white",
        width: 0.5,
      },
    },
    type: "scatter",
  };

  const data = [trace1, trace2];
  const layout = {
    title: "Car power prediction",
    xaxis: {
      title: "horsepower",
      showgrid: false,
      zeroline: false,
    },
    yaxis: {
      title: "mpg",
      showline: false,
    },
  };
  const graphOptions = {
    layout: layout,
    filename: "car power",
    fileopt: "overwrite",
  };

  plotly.plot(data, graphOptions, function (err, msg) {
    console.log(msg);
  });
}
