// The World in One Day — Tuesday, 24 November 2026 (v4).
// Output program for the news-image entry: it publishes the front page
// (entry.png, drawn from 44 dated stories across 10 regions) to the
// standard output path and reports its fingerprint, so the published
// image can be checked byte for byte.
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  console.error(`missing source image: ${source}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const bytes = readFileSync(target);
const digest = createHash("sha256").update(bytes).digest("hex");
const size = statSync(target).size;
console.log(`wrote ${target} (${size} bytes, sha256 ${digest})`);
console.log("front page: THE WORLD IN ONE DAY — Tuesday, 24 November 2026");
console.log("44 stories \u00b7 10 regions \u00b7 12 drawn scenes \u00b7 two named sources per feature");
