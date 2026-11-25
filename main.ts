// News Image — Tuesday 24 November 2026.
//
// This program ships the front page it holds: it copies entry.png,
// the one image that sums up Tuesday 24 November 2026, to the output
// directory the grader reads. Copying keeps both runs byte-identical,
// because no drawing happens here, so no run can drift from the other.
//
// Before writing, it checks the file really is a PNG of at most 1 MiB
// and at most 1024 by 1024 pixels, and refuses anything else — so a
// bad image fails here, loudly, instead of reaching the judge.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The grader runs it with /output as the target instead.

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = resolve(fileURLToPath(new URL(".", import.meta.url)));
const SOURCE = join(HERE, "entry.png");
const TARGET_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const TARGET = join(TARGET_DIR, "entry.png");
const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

if (!existsSync(SOURCE)) {
  throw new Error(`missing image next to this program: ${SOURCE}`);
}
const picture = readFileSync(SOURCE);
const looksPng =
  picture.length >= PNG_SIGNATURE.length &&
  PNG_SIGNATURE.every((byte, index) => picture[index] === byte);
if (!looksPng) {
  throw new Error("entry.png is not a PNG file");
}
if (picture.length > 1024 * 1024) {
  throw new Error(`entry.png is ${picture.length} bytes, over the 1 MiB limit`);
}
const picWidth = picture.readUInt32BE(16);
const picHeight = picture.readUInt32BE(20);
if (picWidth > 1024 || picHeight > 1024) {
  throw new Error(`entry.png is ${picWidth}x${picHeight}, over the 1024x1024 limit`);
}
mkdirSync(TARGET_DIR, { recursive: true });
writeFileSync(TARGET, picture);
const digest = createHash("sha256").update(picture).digest("hex");
console.log(`wrote ${TARGET} (${picture.length} bytes, sha256 ${digest})`);
