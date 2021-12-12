import { install } from "./install";

console.log("Installing packages...");

try {
  install(["@tensorflow/tfjs-node-gpu", "fs-extra", "axios"]);
} catch (err) {
  console.log(err);
}

console.log("Installation done!");

import * as tf from "@tensorflow/tfjs-node-gpu";
import path from "path";
import fs from "fs";

// const tfImg = readImg(`${datasetPath}/train/airplane/0001.png`);
// console.log(tfImg);
