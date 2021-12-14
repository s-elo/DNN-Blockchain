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

export function compressScript(scriptName: string, type: SuffixType) {
  return new Promise<string>(async (res, rej) => {
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

    const fileNames = await getFileNames(scriptDirPath);

    // temporarily copy the files to a new dir
    // to exclude other dirs like logs, dataset and _pycache_
    const copyDirPath = path.resolve(scriptDirPath, ".", "tempt");
    if (!fs.existsSync(copyDirPath)) fs.mkdirSync(copyDirPath);

    fileNames.forEach((name) => {
      const originalFilePath = path.resolve(scriptDirPath, name);
      const copyFilePath = path.resolve(copyDirPath, name);

      fs.copyFileSync(originalFilePath, copyFilePath);
    });

    const archive = archiver("zip");

    archive.pipe(outputStream);

    // append files from the tempor copy dir and naming it as the script name within the archive
    archive.directory(`${copyDirPath}`, `${scriptName}`);

    archive.finalize();

    // listen for all archive data to be written
    // 'close' event is fired only when a file descriptor is involved
    outputStream.on("close", function () {
      console.log(archive.pointer() + " total bytes");
      console.log(
        "archiver has been finalized and the output file descriptor has closed."
      );

      // delete the tempor copy dir
      fs.remove(copyDirPath);

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

export function getFileNames(dirPath: string) {
  return new Promise<string[]>((res) => {
    // all the names including dirs
    const names = fs.readdirSync(dirPath);

    const fileNames = names.filter((name) =>
      fs.statSync(path.resolve(dirPath, name)).isFile()
    );

    res(fileNames);
  });
}
