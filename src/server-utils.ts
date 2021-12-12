import path from "path";
import fs from "fs-extra";
import archiver from "archiver";

const scriptsPath = path.resolve(__dirname, ".", "training-scripts");

export function getScriptNames() {
  return fs.readdirSync(scriptsPath).filter((script) => script !== "template");
}

export async function compressScript(scriptName: string) {
  return new Promise<string>((res, rej) => {
    const scriptDirPath = path.resolve(
      __dirname,
      ".",
      `training-scripts/${scriptName}`
    );

    const outputPath = path.resolve(
      __dirname,
      "../",
      `public/${scriptName}.zip`
    );

    const outputStream = fs.createWriteStream(`${outputPath}`);

    //   {
    //     zlib: { level: 9 }, // Sets the compression level.
    //   }
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
