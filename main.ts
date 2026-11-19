// news-image-20261118 entry (Node 22, standard library only): the image is
// entry.png beside this file, drawn by tools/make_image.py from the world
// news of Wednesday 18 November 2026. The program copies it to /output/entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   MAKEFUN_OUTPUT_DIR=out node main.ts   (the output directory is created)

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');
if (!existsSync(src)) throw new Error('entry.png missing beside main.ts — run tools/make_image.py first');
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
if (statSync(src).size !== statSync(dest).size) throw new Error('copy incomplete: entry.png size mismatch');
