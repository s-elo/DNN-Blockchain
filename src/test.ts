import * as utils from "./server-utils";
import { exec } from "child_process";
import fs from 'fs-extra';
// const names = utils.getScriptNames();
// console.log(names);

// utils.compressScript("cifar10", 'py');
const files = fs.readdirSync('./');
console.log(files);

exec('echo "./home/chao/anaconda3/etc/profile.d/conda.sh" >> ~/.bashrc', () => {
    exec('conda activate fl', () => {
        exec('python test.py')
    })
})
console.log('called');

