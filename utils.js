const path = require('path');
const fs = require('fs-extra');

module.exports.saveModel = async (modelName, model) => {
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
};
