import path from "path";
import fs from "fs-extra";
import archiver from "archiver";

// to distinguish the typescripts scripts and python scripts
const tsScriptsPath = path.resolve(__dirname, ".", "training-scripts/ts");
const pyScriptsPath = path.resolve(__dirname, ".", "training-scripts/py");

export function getScriptNames() {
  const tsScriptNames = fs
    .readdirSync(tsScriptsPath)
    .filter((script) => script !== "template");
  const pyScriptNames = fs
    .readdirSync(pyScriptsPath)
    .filter((script) => script !== "template");

  return [...addSuffix(tsScriptNames, "ts"), ...addSuffix(pyScriptNames, "py")];
}

export async function compressScript(scriptName: string, type: SuffixType) {  
  return new Promise<string>((res, rej) => {
    const scriptDirPath = path.resolve(
      __dirname,
      ".",
      `training-scripts/${type}/${scriptName}`
    );

    const outputPath = path.resolve(
      __dirname,
      "../",
      `public/${scriptName}.zip`
    );

    const outputStream = fs.createWriteStream(`${outputPath}`);

    const archive = archiver("zip");

    archive.pipe(outputStream);

    // append files from a sub-directory and naming it `new-subdir` within the archive
    archive.directory(`${scriptDirPath}`, `${scriptName}`);

    archive.finalize();

    // listen for all archive data to be written
    // 'close' event is fired only when a file descriptor is involved
    outputStream.on("close", function () {
      console.log(archive.pointer() + " total bytes");
      console.log(
        "archiver has been finalized and the output file descriptor has closed."
      );
      res(outputPath);
    });

    archive.on("error", function (err) {
      rej(err);
    });
  });
}

type SuffixType = "ts" | "py";

export const addSuffix = (scriptNames: string[], suffix: SuffixType) =>
  scriptNames.map((name) => `${name}-${suffix}`);

export const splitSuffix = (scriptName: string) =>
  scriptName.split("-") as [string, SuffixType];
