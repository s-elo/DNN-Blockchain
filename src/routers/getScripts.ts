import express from "express";
import { getScriptNames, compressScript } from "../server-utils";

const router = express.Router();

const scriptNames = getScriptNames();

scriptNames.forEach((scriptName) => {
  router.get(`/${scriptName}`, async (_, res) => {
    const isCompressed = await compressScript(scriptName);

    console.log(isCompressed);

    return res.send(isCompressed);
  });
});

export default router;
