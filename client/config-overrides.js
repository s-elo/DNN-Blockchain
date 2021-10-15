const path = require('path');

const { addLessLoader, override, addWebpackAlias } = require("customize-cra");

module.exports = override(addLessLoader(), addWebpackAlias({
    ["@"]: path.resolve(__dirname, './src')
}));
