import express from "express";
import fs from "fs-extra";
import { getScriptNames, compressScript } from "../server-utils";

const router = express.Router();

const scriptNames = getScriptNames();

scriptNames.forEach((scriptName) => {
  router.get(`/${scriptName}`, async (_, res) => {
    const compressPath = await compressScript(scriptName);

    if (!fs.existsSync(compressPath)) {
      return res.send({ msg: "compression failed" });
    }

    const readStream = fs.createReadStream(compressPath);

    readStream.on("data", (chunk) => res.write(chunk, "binary"));
    readStream.on("end", function () {
      // delete the zip file
      fs.unlink(compressPath);

      res.end();
    });
  });
});

export default router;