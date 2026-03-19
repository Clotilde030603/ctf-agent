const fs = require("fs");
const { serializeCircuit } = require("./files/server/utils");
const { runCPU } = require("./files/server/cpu");

const program = fs.readFileSync("./files/server/programs/nand_checker.bin");
const circuit = [
  { input1: 5, input2: 5, output: 1 },
  { input1: 6, input2: 6, output: 2 },
  { input1: 7, input2: 7, output: 3 },
  { input1: 8, input2: 8, output: 4 },
];

let wins = 0;
for (let t = 0; t < 20; t++) {
  const inputState = new Uint16Array(4);
  for (let i = 0; i < 4; i++) inputState[i] = Math.random() < 0.5 ? 0x0000 : 0xffff;
  const outputState = new Uint16Array(4);
  for (let i = 0; i < 4; i++) outputState[i] = inputState[i] === 0xffff ? 0x0000 : 0xffff;
  const memory = serializeCircuit(circuit, program, inputState, outputState);
  const flag = runCPU(memory);
  const result = memory[0x1000] | (memory[0x1001] << 8);
  console.log({ t, input: Array.from(inputState), output: Array.from(outputState), result, flag });
  if (!flag && result === 0x1337) wins++;
}
console.log('wins', wins);
