import express from 'express';
import getScripts from './routers/getScripts';

const server = express();

const port = 3500;

// Cross-Origin Resource Sharing
// server.all("*", (_, res, next) => {
//   res.header("Access-Control-Allow-Origin", `*`);
//   res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE, PUT");

//   next();
// });

server.use('/get-scripts', getScripts);

server.listen(port, () => console.log(`Listening on port ${port}`));
