const express = require("express");
const server = express();

const port = 3500;

// Cross-Origin Resource Sharing
// server.all("*", (_, res, next) => {
//   res.header("Access-Control-Allow-Origin", `*`);
//   res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE, PUT");

//   next();
// });

server.get("/", (_, res) => {
  return res.send("you are visiting this server right now");
});

server.listen(port, () => console.log(`Listening on port ${port}`));
