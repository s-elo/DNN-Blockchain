import * as utils from "./server-utils";
import { exec } from "child_process";
import fs from 'fs-extra';
import path from "path";

const filePath = path.resolve(__dirname, '.', 'test.py');
const file = fs.readFileSync(filePath, 'utf-8');

const lines = file.split('\n');

lines.splice(1, 0, 'insert = 10');

fs.writeFileSync(filePath, lines.join('\n'));
