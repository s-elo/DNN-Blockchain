import fs from "fs-extra";
import path from "path";

import { Web3Storage, File } from "web3.storage";

const modelName = process.argv.slice(2)[0];

Web3StorageTest();
async function Web3StorageTest() {
  // Construct with token and endpoint
  const storage = new Web3Storage({
    token:
      "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweENiRmI4MDk1MkZiMDc2RWUzQjBkRjRlQzlkQTQ5NjkyOEU4MkRlOEIiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NDYxOTY0MjI1MDgsIm5hbWUiOiJETk4tbW9kZWwtc3RvcmFnZSJ9.XFAWDW8TPUaqqIc6ofagZhB-uNaXbc9c2nixviVTZ_8",
  });

  const buffer = fs.readFileSync(
    path.resolve(__dirname, `./${modelName}/model.json`)
  );

  const file = [new File([buffer], `${modelName}_model.json`)];

  const hash = await storage.put(file);

  storeHash(`${modelName}_model.json`, hash);

  // Get info on the Filecoin deals that the CID is stored in
  const info = await storage.status(hash); // Promise<Status | undefined>

  console.log(hash, info);
}

function storeHash(filename: string, hash: string) {
  const deployedData = JSON.parse(
    fs.readFileSync(path.resolve(__dirname, "./deploy_hash.json"), "utf-8")
  );

  deployedData.push({
    filename,
    hash,
  });

  fs.writeFileSync(
    path.resolve(__dirname, "./deploy_hash.json"),
    JSON.stringify(deployedData)
  );
}
