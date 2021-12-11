import { execSync } from "child_process";
import fs from "fs";
import path from "path";

export function install(libs: Array<string>) {
  const pakageJsonPath = path.resolve(__dirname, ".", "package.json");
  if (!fs.existsSync(pakageJsonPath)) {
    // without questionaire
    execSync("npm init -y");

    libs.forEach((lib) => {
      execSync(`npm install ${lib}`);
    });

    // with questionaire
    // spawn("npm", ["init"], {
    //   cwd: __dirname,
    //   shell: true,
    //   stdio: "inherit",
    // });
  }
}
