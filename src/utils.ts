import path from "path";
import fs from "fs-extra";
import * as tf from "@tensorflow/tfjs-node-gpu";

export async function saveModel(modelName: string, model: tf.LayersModel) {
  const modelSavePath = path.resolve(__dirname, ".", "models");
  if (!fs.existsSync(modelSavePath)) {
    fs.mkdirSync(modelSavePath);
  }

  const currentModelPath = path.resolve(modelSavePath, modelName);

  if (!fs.existsSync(currentModelPath)) {
    fs.mkdirSync(currentModelPath);
  } else {
    fs.emptyDirSync(currentModelPath);
  }

  await model.save(`file://${currentModelPath}`);
}
