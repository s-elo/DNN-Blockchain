const fs = require("fs");
const keepCall = require("./utils.js");

const contractBasePath = "../bin/mallet-test";

module.exports.getBalance = function getBalance(wallet, accounts) {
  if (!Array.isArray(accounts))
    return {
      account,
      balance: keepCall(wallet, wallet.getBalance, 5000, accounts),
    };

  const ret = [];

  for (const account of accounts) {
    const balance = keepCall(wallet, wallet.getBalance, 5000, account);

    ret.push({
      account,
      balance,
    });
  }

  return ret;
};

module.exports.requestFunds = function getMoney(wallet, accounts) {
  if (!Array.isArray(accounts))
    return keepCall(wallet, wallet.requestFunds, 5000, accounts);

  for (const account of accounts) {
    keepCall(wallet, wallet.requestFunds, 5000, account);
  }
};

module.exports.sendTransaction = function sendTransaction(wallet, params) {
  const { password, ...tx } = params;

  const transactionHash = keepCall(
    wallet,
    wallet.sendTransaction,
    5000,
    tx,
    password
  );

  // store the transaction info
  const path = `${wallet.datadir}/transactions.json`;
  // no such dir then create one
  if (!fs.existsSync(path)) {
    const data = [
      {
        transactionHash,
        ...params,
      },
    ];

    fs.writeFile(path, JSON.stringify(data), (err) =>
      err ? console.log(err.message) : null
    );
  } else {
    fs.readFile(path, "utf8", (err, data) => {
      if (err) {
        return console.log(err.message);
      }

      const transactions = JSON.parse(data);

      transactions.push({
        transactionHash,
        ...params,
      });

      fs.writeFileSync(path, JSON.stringify(transactions));
    });
  }

  return transactionHash;
};

module.exports.deploy = function deploy(wallet, params) {
  const { path, gas, password } = params;

  const contract = "0x" + fs.readFileSync(`${contractBasePath}${path}`, "utf8");

  const tx = {
    gas,
    data: contract,
  };

  const deploymentHash = keepCall(
    wallet,
    wallet.sendTransaction,
    5000,
    tx,
    password
  );

  const nameReg = /\/(\w+)\.bin$/;

  fs.readFile(`./${wallet.datadir}/deployHash.json`, "utf8", (err, data) => {
    if (err) {
      return console.log(err.message);
    }

    const contracts = JSON.parse(data);

    if (contracts.some((v) => v.deploymentHash === deploymentHash)) return;

    contracts.push({
      contract: path.match(nameReg)[1],
      deploymentHash,
    });

    fs.writeFileSync(`./${wallet.datadir}/deployHash.json`, JSON.stringify(contracts));
  });

  return deploymentHash;
};

module.exports.getReceipt = function getReceipt(wallet, hash) {
  return keepCall(wallet, wallet.getReceipt, 5000, hash);
};
