import express from "express";
import fs from "fs-extra";
import { getScriptNames, compressScript, splitSuffix } from "../server-utils";

const router = express.Router();

const scriptNames = getScriptNames();

scriptNames.forEach((scriptName) => {
  // /get-scripts/{scriptName(with suffix)}
  router.get(`/${scriptName}`, async (req, res) => {
    // get the user account address
    const { address = "" } = req.query;

    // to distinguish the typescripts scripts and python scripts
    const compressPath = await compressScript(
      address as string,
      ...splitSuffix(scriptName)
    );

    if (!fs.existsSync(compressPath)) {
      return res.send({ msg: "compression failed" });
    }

    const readStream = fs.createReadStream(compressPath);

    readStream.on("data", (chunk) => res.write(chunk, "binary"));
    readStream.on("end", function () {
      // delete the zip file
      fs.unlink(compressPath);

      res.end("Script Deliveried");
    });
  });

  router.get("/", async (_, res) => {
    // so far only get the python scripts
    const pythonScriptNames = getScriptNames(
      ["py"],
      (name) => {
        // filter the xxx_cen scripts
        return !name.match(/_cen/g);
      }
    );

    const resData = pythonScriptNames.map((name) => ({
      name: name.split("-")[0],
      desc: "No any description yet",
      // just make up so far
      curAccuracy: 0.8,
    }));

    return res.send(resData);
  });
});

export default router;
