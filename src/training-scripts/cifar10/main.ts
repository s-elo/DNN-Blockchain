import { install } from "./install";

console.log("Installing packages...");

install(["@tensorflow/tfjs-node-gpu", "fs-extra", "axios"]);

console.log("Installation done!");

import * as tf from "@tensorflow/tfjs-node-gpu";
import path from "path";
import fs from "fs";

const datasetPath = path.resolve(__dirname, ".", "dataset");

function readImg(path: string) {
  const imgBuffer = fs.readFileSync(path);

  return tf.node.decodeImage(imgBuffer);
}

// const tfImg = readImg(`${datasetPath}/train/airplane/0001.png`);
// console.log(tfImg);
