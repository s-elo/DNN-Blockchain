import { getData } from "./dataHandler";

async function timeEvaluator(fn: any) {
  const startTime = Date.now();
  await fn();
  const endTime = Date.now();
  console.log(`Run time: ${(endTime - startTime) / 1000} S`);
}

timeEvaluator(getData);
