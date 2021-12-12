import path from "path";
import fs from "fs";
import * as tf from "@tensorflow/tfjs-node-gpu";

const DATASET_PATH = path.resolve(__dirname, ".", "dataset");
const TRAIN_PATH = path.resolve(DATASET_PATH, "train");
const TEST_PATH = path.resolve(DATASET_PATH, "test");

const CLASS_NAMES = getClassNames();

const IMAGE_SIZE = 32;
const IMAGE_CHANNEL = 3;

type PromiseForClass = {
  imgs: Array<tf.Tensor3D | tf.Tensor4D>;
  labels: Array<string>;
};

export function getSingleImgTensor(
  imgName: string,
  className: string,
  from: "TRAIN" | "TEST"
) {
  const imgBuffer = fs.readFileSync(
    `${from === "TRAIN" ? TRAIN_PATH : TEST_PATH}/${className}/${imgName}`
  );

  return tf.image.resizeBilinear(tf.node.decodeImage(imgBuffer), [
    IMAGE_SIZE,
    IMAGE_SIZE,
  ]);
}

export function getClassNames() {
  const classNameFromTrain = fs.readdirSync(TRAIN_PATH);
  const classNameFromTest = fs.readdirSync(TEST_PATH);

  if (classNameFromTrain.length !== classNameFromTest.length) {
    throw new Error(
      "The classifications between your training set and test set are not matched"
    );
  }

  const isClassMatched = (testClass: string[]) => (className: string) =>
    testClass.includes(className);

  if (!classNameFromTrain.every(isClassMatched(classNameFromTest))) {
    throw new Error(
      "The classifications between your training set and test set are not matched"
    );
  }

  return classNameFromTrain;
}

export async function getData() {
  const [
    { imgs: trainData, labels: trainLabel },
    { imgs: testData, labels: testLabel },
  ] = await Promise.all([getDataSet("TRAIN"), getDataSet("TEST")]);

  console.log(trainLabel.length, testLabel.length);
}

export function getDataSet(type: "TRAIN" | "TEST") {
  return new Promise<PromiseForClass>((res) => {
    const ret = CLASS_NAMES.reduce(
      (set, curClass) => {
        const imgNames = fs.readdirSync(
          `${type === "TRAIN" ? TRAIN_PATH : TEST_PATH}/${curClass}`
        );

        imgNames.forEach(async (imgName) => {
          // getSingleImgTensor return a promise
          set.imgs.push(getSingleImgTensor(imgName, curClass, type));

          set.labels.push(curClass);
        });

        return set;
      },
      {
        imgs: [],
        labels: [],
      } as PromiseForClass
    );

    res(ret);
  });
}
