import express from "express";
import fs from "fs-extra";
import {
  getScriptNames,
  compressScript,
  addSuffix,
  splitSuffix,
} from "../server-utils";

const router = express.Router();

const scriptNames = getScriptNames();

scriptNames.forEach((scriptName) => {
  router.get(`/${scriptName}`, async (_, res) => {
    // to distinguish the typescripts scripts and python scripts
    const compressPath = await compressScript(...splitSuffix(scriptName));

    if (!fs.existsSync(compressPath)) {
      return res.send({ msg: "compression failed" });
    }

    const readStream = fs.createReadStream(compressPath);

    readStream.on("data", (chunk) => res.write(chunk, "binary"));
    readStream.on("end", function () {
      // delete the zip file
      fs.unlink(compressPath);

      res.end('Script Deliveried');
    });
  });
});

export default router;
