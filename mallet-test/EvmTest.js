// const Mallet = require("@iohk/mallet");
const Mallet = require("../mallet/lib/mallet.js");
const { requestFunds, getBalance, sendTransaction, deploy, getReceipt } = require("./apis.js");

// place where stores the accounts
const dataDir = "./EvmData";

// connect the kevm net and get the wallet instance
// different dataDir corresponding to different wallet with diff accounts
const wallet = new Mallet("evm", dataDir);
// wallet.newAccount();

const accounts = wallet.listAccounts();

// select as the current account
wallet.selectAccount(accounts[0]);

console.log("current account: ", wallet.currentAccount());

// requestFunds(wallet, accounts[1]);

// get balance
// const balances = getBalance(wallet, accounts);
// console.log(balances);

const tx = {
  to: accounts[1], // recipient's address, optional, new contract created if not provided
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

// const receipt = getReceipt(wallet, "0x4a7ab0d37a104e98640297fa3279428fe0312eceb5e1dce694c9299fe0b7dd03");
// console.log(receipt);
