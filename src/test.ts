import * as utils from "./server-utils";

const names = utils.getScriptNames();
console.log(names);

utils.compressScript("baseball");
