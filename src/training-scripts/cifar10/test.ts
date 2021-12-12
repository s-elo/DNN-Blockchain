import { getDataSet, getSingleImgTensor } from "./dataHandler";
import * as tf from "@tensorflow/tfjs-node-gpu";

async function timeEvaluator(fn: any, ...args: any) {
  const startTime = Date.now();
  const ret = await fn(...args);
  const endTime = Date.now();
  console.log(`Run time: ${(endTime - startTime) / 1000} S`);

  return ret;
}

(async () => {
  // const {imgs: testData, labels: testLabel} = await timeEvaluator(getDataSet, 'TEST');

  // console.log(testLabel.length);
  
  // const {imgs: trainData, labels: trainLabel} = await timeEvaluator(getDataSet, 'TRAIN');

  // console.log(trainLabel.length);
})();

