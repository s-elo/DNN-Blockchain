import path from "path";
import fs from "fs";
import * as tf from "@tensorflow/tfjs-node-gpu";

const DATASET_PATH = path.resolve(__dirname, ".", "dataset");
const TRAIN_PATH = path.resolve(DATASET_PATH, "train");
const TEST_PATH = path.resolve(DATASET_PATH, "test");

export const CLASS_NAMES = getClassNames();

export const IMAGE_WIDTH = 32;
export const IMAGE_HEIGHT = 32;
export const IMAGE_CHANNELS = 3;

export const BATCH_SIZE = 512;

type OriginalData = {
  imgs: Array<tf.Tensor3D>;
  labels: Array<number>;
};

type NormalizedData = {
  imgs: tf.Tensor<tf.Rank>;
  labels: tf.Tensor<tf.Rank>;
};

export function getSingleImgTensor(
  imgName: string,
  className: string,
  from: "TRAIN" | "TEST"
) {
  const imgBuffer = fs.readFileSync(
    `${from === "TRAIN" ? TRAIN_PATH : TEST_PATH}/${className}/${imgName}`
  );

  const resizedTfImg = tf.image.resizeBilinear(
    tf.node.decodeImage(imgBuffer) as tf.Tensor3D,
    [IMAGE_WIDTH, IMAGE_HEIGHT]
  );

  return resizedTfImg;
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

export function getDataSet(type: "TRAIN" | "TEST") {
  return new Promise<NormalizedData>((res) => {
    const result = CLASS_NAMES.reduce(
      (set, curClass, classIdx) => {
        const imgNames = fs.readdirSync(
          `${type === "TRAIN" ? TRAIN_PATH : TEST_PATH}/${curClass}`
        );

        imgNames.forEach(async (imgName) => {
          // getSingleImgTensor return a promise
          // the tensor should be turned into normal data here
          set.imgs.push(getSingleImgTensor(imgName, curClass, type));

          set.labels.push(classIdx);
        });

        return set;
      },
      {
        imgs: [],
        labels: [],
      } as OriginalData
    );

    res(normalization(result));
  });
}

function normalization(dataset: OriginalData) {
  return tf.tidy(() => {
    // each pos represents a class
    // the value of the pos is 1 means the label is that class
    // tfLabels: (sample_num, class_num)
    const tfLabels = tf.oneHot(
      tf.tensor1d(dataset.labels, "int32"),
      CLASS_NAMES.length,
      1, // onVlaue
      0 // offValue
    );

    // tfImgs: (sample_num, width, height, channel)
    const tfImgs = tf.stack(dataset.imgs);

    // 0-1
    const normalizedImgs = tfImgs.div(255);

    return {
      imgs: normalizedImgs,
      labels: tfLabels,
    };
  });
}
