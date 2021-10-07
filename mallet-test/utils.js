module.exports = function keepCall(wallet, fn, time, ...args) {
  const start = Date.now();

  while (Date.now() - start <= time) {
    try {
      const ret = fn.call(wallet, ...args);
      return ret;
    } catch (err) {
      console.log(err.message);
    }
  }

  console.log("time out");

  return "time out";
};
