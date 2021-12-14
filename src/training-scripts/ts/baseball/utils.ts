import path from "path";
import fs from "fs-extra";
import * as tf from "@tensorflow/tfjs-node-gpu";

export async function saveModel(model: tf.LayersModel) {
  const modelSavePath = path.resolve(__dirname, ".", "models");
  if (!fs.existsSync(modelSavePath)) {
    fs.mkdirSync(modelSavePath);
  } else {
    fs.emptyDirSync(modelSavePath);
  }

  await model.save(`file://${modelSavePath}`);
}
