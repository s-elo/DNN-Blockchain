import path from "path";
import fs from "fs-extra";
import archiver from "archiver";

const filterNames = ["privateKey.py"];

export function getScriptNames(
  types?: string[],
  filter?: (scriptName: string) => boolean
) {
  // get the types of the scripts
  const scriptTypes = types
    ? types
    : fs.readdirSync(path.resolve(__dirname, ".", "training-scripts"));

  const scriptNames = scriptTypes.reduce((names, curType) => {
    // get the current type path
    const curTypePath = path.resolve(
      __dirname,
      ".",
      `training-scripts/${curType}`
    );

    // get the script names of the current type ieg: py
    const curScriptNames = fs
      .readdirSync(curTypePath)
      .filter((script) => script !== "template");

    return names.concat(...addSuffix(curScriptNames, curType));
  }, [] as string[]);

  return scriptNames.filter(filter ? filter : () => true);
}

export function compressScript(
  address: string,
  scriptName: string,
  type: string
) {
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

    const fileNames = await getFileNames(
      scriptDirPath,
      // remove the files that should be filtered
      (name) => !filterNames.includes(name)
    );
      
    // temporarily copy the files to a new dir
    // to exclude other dirs like logs, dataset and _pycache_
    const copyDirPath = path.resolve(scriptDirPath, ".", "tempt");
    if (!fs.existsSync(copyDirPath)) fs.mkdirSync(copyDirPath);

    const copyPromises = fileNames.map((name) => {
      const originalFilePath = path.resolve(scriptDirPath, name);
      const copyFilePath = path.resolve(copyDirPath, name);

      // insert the account address
      if (name === `main.${type}`) {
        return fs.readFile(originalFilePath, "utf-8").then((file) => {
          return fs.writeFile(
            copyFilePath,
            insertAddress(file, `ADDRESS = "${address}"`)
          );
        });
      }

      return fs.copyFile(originalFilePath, copyFilePath);
    });

    await Promise.all(copyPromises);

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

export const addSuffix = (scriptNames: string[], suffix: string) =>
  scriptNames.map((name) => `${name}-${suffix}`);

export const splitSuffix = (scriptName: string) =>
  scriptName.split("-") as [string, string];

export function getFileNames(
  dirPath: string,
  filter?: (fileName: string) => boolean
) {
  return new Promise<string[]>((res) => {
    // all the names including dirs
    const names = fs.readdirSync(dirPath);

    const fileNames = names.filter((name) =>
      fs.statSync(path.resolve(dirPath, name)).isFile()
    );

    res(fileNames.filter(filter ? filter : () => true));
  });
}

export function insertAddress(file: string, content: string) {
  const lines = file.split("\n");

  const insertLine = lines.findIndex((line) => !line.includes("import"));

  lines.splice(insertLine + 1, 0, content);

  return lines.join("\n");
}
