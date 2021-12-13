import path from "path";
import fs from "fs-extra";
import os from "os";
import { exec } from "child_process";
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


// export async function checkEnv() {
//   const platform = os.platform();

//   switch (platform) {
//     case "linux": {
//       exec("nvidia-smi", (error, stdout, stderr) => {
//         if (error) {
//           console.log(`error: ${error.message}`);
//           return;
//         }
//         if (stderr) {
//           console.log(`stderr: ${stderr}`);
//           return;
//         }
//         // Normalise the result here to get the GPU name
//         console.log(`stdout: ${stdout}`);
//         console.log(typeof stdout);
        
//       });
//     }
//   }
// }
