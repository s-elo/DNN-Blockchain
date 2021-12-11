import { install } from "./install";

console.log("Installing packages...");

install(["@tensorflow/tfjs-node-gpu", "fs-extra", "axios"]);

console.log("Installation done!");

import * as tf from "@tensorflow/tfjs-node-gpu";
