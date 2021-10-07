const Mallet = require("../mallet/lib/mallet.js");
const malletAPIs = require("./apis.js");

// place where stores the accounts
const dataDir = "./dataDir";

// connect the kevm net and get the wallet instance
// different dataDir corresponding to different wallet with diff accounts
const wallet = new Mallet("kevm", dataDir);

const balances = malletAPIs.getBalance(wallet, wallet.listAccounts());
console.log(balances);

// create a new account
// const newAccountAddress = malletInKevm.newAccount();

// select as the current account
// malletInKevm.selectAccount(accounts[0]);

// console.log("current account: ", malletInKevm.currentAccount());

// const tx = {
//   to: accounts[2], // recipient's address, optional, new contract created if not provided
//   gas: 100000, // gas limit, mandatory
//   gasPrice: 5000000000, // gasPrice, optional, default: 5 Gwei
//   value: 1000000, // optional, default: 0
//   data: "hello!", // optional, default: empty
// };

// lauched by the current selected account
// const transactionHash = keepCall(malletInKevm, malletInKevm.sendTransaction, 5000, tx, '123');

// console.log(transactionHash);

// you can just get the receipt
// console.log(malletInKevm.getReceipt(transactionHash));

// const deploymentHash = deploy(malletInKevm, "/HelloWorld.bin", 5000000000, "123");

// console.log(deploymentHash);

// const address = keepCall(
//   malletInKevm,
//   malletInKevm.getReceipt,
//   5000,
//   "0xbda5a1eef79279df866ee5ea4a8414baecfcef7f504ae810cce1bc32a3924658"
// );

// console.log(address);
