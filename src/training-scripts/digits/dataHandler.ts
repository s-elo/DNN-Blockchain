import * as tf from "@tensorflow/tfjs-node-gpu";
import path from "path";
import fs from "fs";
import axios from "axios";

const IMAGE_SIZE = 784;
const NUM_CLASSES = 10;
const NUM_DATASET_ELEMENTS = 65000;

const TRAIN_TEST_RATIO = 5 / 6;

const NUM_TRAIN_ELEMENTS = Math.floor(TRAIN_TEST_RATIO * NUM_DATASET_ELEMENTS);
const NUM_TEST_ELEMENTS = NUM_DATASET_ELEMENTS - NUM_TRAIN_ELEMENTS;

const MNIST_IMAGES_SPRITE_PATH =
  "https://storage.googleapis.com/learnjs-data/model-builder/mnist_images.png";
const MNIST_LABELS_PATH =
  "https://storage.googleapis.com/learnjs-data/model-builder/mnist_labels_uint8";

/**
 * A class that fetches the sprited MNIST dataset and returns shuffled batches.
 *
 * NOTE: This will get much easier. For now, we do data fetching and
 * manipulation manually.
 */
export class MnistData {
  shuffledTrainIndex: number = 0;
  shuffledTestIndex: number = 0;

  datasetImages: Float32Array = new Float32Array();
  datasetLabels: Uint8Array = new Uint8Array();

  trainIndices: Uint32Array = new Uint32Array();
  testIndices: Uint32Array = new Uint32Array();

  trainImages: Float32Array = new Float32Array();
  testImages: Float32Array = new Float32Array();
  trainLabels: Uint8Array = new Uint8Array();
  testLabels: Uint8Array = new Uint8Array();

  async load() {
    return new Promise(async (res) => {
      // sprited image saving path
      const spImgPath = path.resolve(__dirname, ".", "dataset/data.png");

      if (fs.existsSync(spImgPath)) return res('');

      // Make a request for the MNIST sprited image.
      const resp = await axios.get(MNIST_IMAGES_SPRITE_PATH, {
        responseType: "stream",
      });

      // create writing stream
      const writeStream = fs.createWriteStream(spImgPath);

      resp.data.pipe(writeStream);

      writeStream.on("finish", () => {
        writeStream.close();
        res("");
      });
    });
  }

  async createDataset() {
    const spImgPath = path.resolve(__dirname, ".", "dataset/data.png");

    const ImagBUff = fs.readFileSync(spImgPath);
    
    const tfImg = tf.node.decodeImage(ImagBUff, 1);
    // 0-1
    const floatImg = tf.cast(tfImg, "float32").div(255);
    
    this.datasetImages = floatImg.dataSync() as Float32Array;

    // console.log('whole data length', this.datasetImages.byteLength);
    
    const resp = await axios.get(MNIST_LABELS_PATH, {
      responseType: "arraybuffer",
    });

    // (65000, 10)
    this.datasetLabels = new Uint8Array(resp.data);

    // Create shuffled indices into the train/test set for when we select a
    // random dataset element for training / validation.
    this.trainIndices = tf.util.createShuffledIndices(NUM_TRAIN_ELEMENTS);
    this.testIndices = tf.util.createShuffledIndices(NUM_TEST_ELEMENTS);

    // Slice the the images and labels into train and test sets.
    this.trainImages = this.datasetImages.slice(
      0,
      IMAGE_SIZE * NUM_TRAIN_ELEMENTS
    );
    // console.log('train length:', this.trainImages.byteLength);
    this.testImages = this.datasetImages.slice(IMAGE_SIZE * NUM_TRAIN_ELEMENTS);
    this.trainLabels = this.datasetLabels.slice(
      0,
      NUM_CLASSES * NUM_TRAIN_ELEMENTS
    );
    this.testLabels = this.datasetLabels.slice(
      NUM_CLASSES * NUM_TRAIN_ELEMENTS
    );

    return this;
  }

  nextTrainBatch(batchSize: number) {
    return this.nextBatch(
      batchSize,
      [this.trainImages, this.trainLabels],
      () => {
        this.shuffledTrainIndex =
          (this.shuffledTrainIndex + 1) % this.trainIndices.length;
        return this.trainIndices[this.shuffledTrainIndex];
      }
    );
  }

  nextTestBatch(batchSize: number) {
    return this.nextBatch(batchSize, [this.testImages, this.testLabels], () => {
      this.shuffledTestIndex =
        (this.shuffledTestIndex + 1) % this.testIndices.length;
      return this.testIndices[this.shuffledTestIndex];
    });
  }

  nextBatch(
    batchSize: number,
    data: Array<Float32Array | Uint8Array>,
    index: () => number
  ) {
    const batchImagesArray = new Float32Array(batchSize * IMAGE_SIZE);
    const batchLabelsArray = new Uint8Array(batchSize * NUM_CLASSES);
    
    for (let i = 0; i < batchSize; i++) {
      const idx = index();

      const image = data[0].slice(
        idx * IMAGE_SIZE,
        idx * IMAGE_SIZE + IMAGE_SIZE
      );
      batchImagesArray.set(image, i * IMAGE_SIZE);

      const label = data[1].slice(
        idx * NUM_CLASSES,
        idx * NUM_CLASSES + NUM_CLASSES
      );
      batchLabelsArray.set(label, i * NUM_CLASSES);
    }

    const xs = tf.tensor2d(batchImagesArray, [batchSize, IMAGE_SIZE]);
    const labels = tf.tensor2d(batchLabelsArray, [batchSize, NUM_CLASSES]);

    return { xs, labels };
  }
}

export const data = new MnistData();
