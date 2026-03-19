# Notes

## Timer

- Start time:
- Deadline:
- Current best lead: send a minimal NAND self-loop inversion circuit to `/check`

## Facts

- Challenge title is `Pachinko` and category is `Web Exploitation`.
- Live site: `http://activist-birds.picoctf.net:56603/`
- Source shows `/check` serializes a circuit and returns `FLAG1` when the result code is `0x1337`.
- Input nodes are numbered `5` to `8` and output nodes are numbered `1` to `4`.
- A NAND gate with the same input twice computes logical NOT.
- Submitting four self-NAND outputs returns the first flag.

## Hypotheses

- The intended first solve is the legitimate NAND inversion circuit, not an admin endpoint exploit.

## Disproved ideas

- Hunting for hidden hints is unnecessary for flag one.
- The first flag does not require the `/flag` admin endpoint.

## Useful commands

- `curl -s http://activist-birds.picoctf.net:56603/check -H 'Content-Type: application/json' --data '{"circuit":[{"input1":5,"input2":5,"output":1},{"input1":6,"input2":6,"output":2},{"input1":7,"input2":7,"output":3},{"input1":8,"input2":8,"output":4}]}'`

## Flag candidates

- `picoCTF{p4ch1nk0_f146_0n3_e947b9d7}`
