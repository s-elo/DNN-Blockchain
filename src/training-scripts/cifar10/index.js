const tf = require("@tensorflow/tfjs-node-gpu");
const path = require("path");
const fs = require("fs-extra");

const datasetPath = path.resolve(__dirname, '.', 'dataset');

function readImg(path) {
  const imgBuffer = fs.readFileSync(path);

  return tf.node.decodeImage(imgBuffer);
}

const tfImg = readImg(`${datasetPath}/train/airplane/0001.png`);

