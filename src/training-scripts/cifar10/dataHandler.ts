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
  imgs: tf.Tensor<tf.Rank>[];
  labels: number[];
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
    tf.node.decodeImage(imgBuffer, IMAGE_CHANNELS) as tf.Tensor3D,
    [IMAGE_WIDTH, IMAGE_HEIGHT]
  );

  // const floatImg = tf.cast(resizedTfImg, "float32");
  // return floatImg;
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

export function getData(type: "TRAIN" | "TEST", percent: number = 1) {
  return new Promise<NormalizedData>((res) => {
    const result = CLASS_NAMES.reduce(
      (set, curClass, classIdx) => {
        const imgNames = fs.readdirSync(
          `${type === "TRAIN" ? TRAIN_PATH : TEST_PATH}/${curClass}`
        );

        for (const [index, imgName] of imgNames.entries()) {
          // getSingleImgTensor return a promise
          // the tensor should be turned into normal data here
          set.imgs.push(getSingleImgTensor(imgName, curClass, type));

          set.labels.push(classIdx);
          if (index >= imgNames.length * percent) break;
        }

        return set;
      },
      {
        imgs: [],
        labels: [],
      } as OriginalData
    );

    res(tersorization(result));
  });
}

function tersorization(dataset: OriginalData) {
  // return tf.data.zip({
  //   xs: tf.data.array(dataset.imgs),
  //   ys: tf.data.array(dataset.labels),
  // });
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
  return {
    imgs: tfImgs.div(255),
    labels: tfLabels,
  };
  // return tf.tidy(() => {

  // });
}

export function getDataset(type: "TRAIN" | "TEST", percent: number = 1) {
  const dataset = tf.data
    .generator(getDataGen.bind(null, type, percent))
    .batch(5000);

  return dataset;
}

function* getDataGen(type: "TRAIN" | "TEST", percent: number = 1) {
  for (const [classIdx, className] of CLASS_NAMES.entries()) {
    const imgNames = fs.readdirSync(
      `${type === "TRAIN" ? TRAIN_PATH : TEST_PATH}/${className}`
    );

    for (const [index, imgName] of imgNames.entries()) {
      if (index >= imgNames.length * percent) break;

      // getSingleImgTensor return a promise
      // the tensor should be turned into normal data here
      yield {
        xs: getSingleImgTensor(imgName, className, type),
        ys: tf.tensor1d(generateLabel(CLASS_NAMES.length, classIdx)),
      };
    }
  }
}

function generateLabel(classNum: number, indice: number) {
  return new Array(classNum).fill(0).map((_, idx) => (idx === indice ? 1 : 0));
}
