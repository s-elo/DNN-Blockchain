import * as utils from "../server-utils";
import { exec } from "child_process";
import fs from "fs-extra";
import path from "path";

import { Web3Storage, File } from "web3.storage";

console.log(process.argv.slice(2));

// insertTest();
function insertTest() {
  const filePath = path.resolve(__dirname, ".", "test.py");
  const file = fs.readFileSync(filePath, "utf-8");

  const lines = file.split("\n");

  lines.splice(1, 0, "insert = 10");

  fs.writeFileSync(filePath, lines.join("\n"));
}

// Web3StorageTest();
async function Web3StorageTest() {
  // Construct with token and endpoint
  const storage = new Web3Storage({
    token:
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweENiRmI4MDk1MkZiMDc2RWUzQjBkRjRlQzlkQTQ5NjkyOEU4MkRlOEIiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NDYxOTY0MjI1MDgsIm5hbWUiOiJETk4tbW9kZWwtc3RvcmFnZSJ9.XFAWDW8TPUaqqIc6ofagZhB-uNaXbc9c2nixviVTZ_8",
  });

  const testObj = {
    param: "asdfasdfas",
    archi: "asdfasdfas",
  };

  const buffer = Buffer.from(JSON.stringify(testObj));

  const file = [new File([buffer], "test.json")];

  const hash = await storage.put(file);

  // Get info on the Filecoin deals that the CID is stored in
  const info = await storage.status(hash); // Promise<Status | undefined>

  console.log(hash, info);
}
