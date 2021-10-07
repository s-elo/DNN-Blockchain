const Mallet = require("../mallet/lib/mallet.js");
const { requestFunds, getBalance, sendTransaction, deploy, getReceipt } = require("./apis.js");

// place where stores the accounts
const dataDir = "./KevmData";

// connect the kevm net and get the wallet instance
// different dataDir corresponding to different wallet with diff accounts
const wallet = new Mallet("kevm", dataDir);

const accounts = wallet.listAccounts();

// select as the current account
wallet.selectAccount(accounts[0]);

console.log("current account: ", wallet.currentAccount());

// requestFunds(wallet, accounts[2]);

// get balance
const balances = getBalance(wallet, accounts);
console.log(balances);

const tx = {
  to: accounts[2], // recipient's address, optional, new contract created if not provided
  gas: 100000, // gas limit, mandatory
  gasPrice: 5000000000, // gasPrice, optional, default: 5 Gwei
  value: 1000000, // optional, default: 0
  data: "How u doing?", // optional, default: empty,
  password: "123",
};

// const transactionHash = sendTransaction(wallet, tx);

// console.log('hash', transactionHash);

// console.log(wallet.getReceipt(transactionHash));
const deployParams = {
  path: "/HelloWorld.bin",
  gas: 6000000000,
  password: "123",
};
// const deploymentHash = deploy(wallet, deployParams);
// console.log(deploymentHash);

const receipt = getReceipt(wallet, "0xe1dbd46f732cd762f0dc207977a4f04b9b1c5891b8e6881ad820023526174d4e");
console.log(receipt);
