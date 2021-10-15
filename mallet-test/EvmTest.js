// const Mallet = require("@iohk/mallet");
const Mallet = require("../mallet/lib/mallet.js");
const fs = require("fs");
const {
  requestFunds,
  getBalance,
  sendTransaction,
  deploy,
  getReceipt,
} = require("./apis.js");

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
const balances = getBalance(wallet, accounts);
console.log(balances);

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

// const code = fs.readFileSync('../bin/mallet-test/HelloWorld.bin');

const deployParams = {
  path: "/HelloWorld.bin",
  gas: 1,
  password: "123",
};

// const deploymentHash = deploy(wallet, deployParams);
// console.log(deploymentHash);

// const receipt = getReceipt(wallet, "0x91eaaf8b7ab541234f43e6e4ac8a47dc8987bf41a83ba26ac9d9baeb2c7ea538");
// console.log(receipt);
