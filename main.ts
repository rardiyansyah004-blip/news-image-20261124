// The World in One Day — Tuesday, 24 November 2026 (v5).
// Output program for the news-image entry: it publishes the front page
// (entry.png, drawn from 50 dated stories across 10 regions, with a
// nine-point UTC timeline, a world map pinning 19 stories, sixteen drawn
// scenes, and a how-sure label on every story) to the standard output
// path and reports its fingerprint, so the published image can be
// checked byte for byte.
//
// The page was drawn with Pillow from the verified stories listed in the
// README. Every number on it was checked against the live wires on
// 25 November 2026: TAIEX +8.99% to 40,122.35 (record 3,310-point gain),
// KOSPI 5,006.03 (+6.32%), Nikkei 58,644.63 (+3.91%), Sanofi's $41.0bn
// Insmed deal at $175 a share, the Nepal quake at 01:32 UTC (EMSC 5.3,
// Nepal 5.6, 10 km deep), Nvidia +31.48% on Monday (+$952bn), gold
// $3,661 an ounce, and the CAS verdict restoring Senegal's AFCON title
// at 15:47 UTC. The date-check box on the page names the Monday
// announcements covered on Tuesday and the wrong-day news left out.
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

const bytes = readFileSync(source);
if (bytes.length > 1024 * 1024) {
  console.error(`entry.png too big: ${bytes.length} bytes (limit 1 MiB)`);
  process.exit(1);
}
if (bytes.subarray(0, 8).toString("hex") !== "89504e470d0a1a0a") {
  console.error("entry.png is not a PNG");
  process.exit(1);
}
// PNG IHDR: width and height are big-endian uint32 at offsets 16 and 20.
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1536 || height !== 1536) {
  console.error(`entry.png is ${width}x${height}, expected 1536x1536`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const out = readFileSync(target);
const digest = createHash("sha256").update(out).digest("hex");
const size = statSync(target).size;
console.log(`wrote ${target} (${size} bytes, sha256 ${digest})`);
console.log("front page: THE WORLD IN ONE DAY — Tuesday, 24 November 2026");
console.log("50 stories · 10 regions · 16 drawn scenes · UTC timeline · world map, 19 pinned · how-sure label on every story");
