# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 8

Generated 2026-10-28 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 8.

## wq = binary, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 add | 16,826 / 49.44 | 25,238 / 74.16 | 29,445 / 86.52 | 33,651 / 98.88 |
| MAC opt | 8·v × fp16 add | 16,826 / 49.44 | 25,238 / 74.16 | 29,445 / 86.52 | 33,651 / 98.88 |
| MAC int8 | 8·v × int16 add | 1,048 / 1.69 | 1,572 / 2.54 | 1,835 / 2.96 | 2,097 / 3.39 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,535 / 13.29 | 18,321 / 14.14 | 32,241 / 14.83 | 60,486 / 16.02 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,949 / 13.12 | 11,395 / 13.70 | 18,321 / 14.14 | 32,241 / 14.83 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,535 / 13.29 | 18,321 / 14.14 | 32,241 / 14.83 | 60,486 / 16.02 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,949 / 13.12 | 11,395 / 13.70 | 18,321 / 14.14 | 32,241 / 14.83 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,033* / 12.74* | 5,588 / 12.89 | 6,420 / 13.08 | 8,185 / 13.41 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,033* / 12.74* | 5,161 / 12.79 | 5,588 / 12.89 | 6,420 / 13.08 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,033* / 12.74* | 5,588 / 12.89 | 6,420 / 13.08 | 8,185 / 13.41 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,033* / 12.74* | 5,161 / 12.79 | 5,588 / 12.89 | 6,420 / 13.08 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 add | 16,826 / 49.44 | 25,238 / 74.16 | 29,445 / 86.52 | 33,651 / 98.88 |
| MAC opt | 8·v × fp16 add | 16,826 / 49.44 | 25,238 / 74.16 | 29,445 / 86.52 | 33,651 / 98.88 |
| MAC int8 | 8·v × int16 add | 1,048 / 1.69 | 1,572 / 2.54 | 1,835 / 2.96 | 2,097 / 3.39 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 29,602 / 14.55 | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 16,995 / 13.96 | 116,804 / 18.49 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 29,602 / 14.55 | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 16,995 / 13.96 | 116,804 / 18.49 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 6,162 / 13.00 | 19,294 / 16.00 | 71,373 / 24.00 | 144,980 / 32.59 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,416 / 12.82 | 12,367 / 14.47 | 33,647 / 19.21 | 71,373 / 24.00 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 6,162 / 13.00 | 19,294 / 16.00 | 71,373 / 24.00 | 144,980 / 32.59 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,416 / 12.82 | 12,367 / 14.47 | 33,647 / 19.21 | 71,373 / 24.00 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int2×int8 mul + 8·v × fp16 add | 17,898 / 52.43 | 26,847 / 78.64 | 31,322 / 91.75 | 35,796 / 104.85 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 15,069 / 26.59 | 36,641 / 28.29 | 64,481 / 29.65 | 120,972 / 32.03 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 11,898 / 26.25 | 22,790 / 27.39 | 36,641 / 28.29 | 64,481 / 29.65 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 10,066* / 25.48* | 11,176 / 25.77 | 12,839 / 26.15 | 16,369 / 26.83 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 10,066* / 25.48* | 10,322 / 25.58 | 11,176 / 25.77 | 12,839 / 26.15 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | 12,150* / 25.77* | 14,272 / 26.13 | 17,333 / 26.57 | 23,377 / 27.33 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | 12,150* / 25.77* | 12,727 / 25.94 | 14,272 / 26.13 | 17,333 / 26.57 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int3×int8 mul + 8·v × fp16 add | 18,346 / 52.94 | 27,518 / 79.41 | 32,105 / 92.64 | 36,691 / 105.87 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 22,604 / 39.88 | 54,962 / 42.43 | 96,722 / 44.48 | 181,459 / 48.05 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 17,847 / 39.37 | 34,185 / 41.09 | 54,962 / 42.43 | 96,722 / 44.48 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 15,099* / 38.22* | 16,764 / 38.66 | 19,259 / 39.23 | 24,554 / 40.24 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 15,099* / 38.22* | 15,484 / 38.38 | 16,764 / 38.66 | 19,259 / 39.23 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | 18,488* / 38.85* | 21,731 / 39.41 | 26,303 / 40.04 | 35,354 / 41.13 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | 18,488* / 38.85* | 19,408 / 39.13 | 21,731 / 39.41 | 26,303 / 40.04 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int4×int8 mul + 8·v × fp16 add | 18,882 / 53.23 | 28,323 / 79.85 | 33,043 / 93.16 | 37,764 / 106.47 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 30,139 / 53.18 | 73,283 / 56.58 | 128,963 / 59.30 | 241,945 / 64.07 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 23,796 / 52.49 | 45,580 / 54.79 | 73,283 / 56.58 | 128,963 / 59.30 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 20,132* / 50.96* | 22,351 / 51.54 | 25,679 / 52.31 | 32,738 / 53.65 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 20,132* / 50.96* | 20,645 / 51.17 | 22,351 / 51.54 | 25,679 / 52.31 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | 25,292* / 52.06* | 29,891 / 52.86 | 36,256 / 53.72 | 48,894 / 55.20 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | 25,292* / 52.06* | 26,633 / 52.49 | 29,891 / 52.86 | 36,256 / 53.72 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int6×int8 mul + 8·v × fp16 add | 20,229 / 55.91 | 30,343 / 83.87 | 35,400 / 97.84 | 40,457 / 111.82 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | 45,208 / 79.77 | 109,924 / 84.87 | 193,444 / 88.95 | 362,917 / 96.10 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | 35,695 / 78.74 | 68,370 / 82.18 | 109,924 / 84.87 | 193,444 / 88.95 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | 30,198* / 76.44* | 33,527 / 77.31 | 38,518 / 78.46 | 49,107 / 80.48 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | 30,198* / 76.44* | 30,967 / 76.75 | 33,527 / 77.31 | 38,518 / 78.46 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | 40,275* / 78.90* | 48,241 / 80.32 | 59,071 / 81.75 | 80,621 / 84.17 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | 40,275* / 78.90* | 42,688 / 79.71 | 48,241 / 80.32 | 59,071 / 81.75 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int8×int8 mul + 8·v × fp16 add | 21,430 / 57.81 | 32,145 / 86.71 | 37,503 / 101.16 | 42,860 / 115.61 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | 60,277 / 106.36 | 146,565 / 113.15 | 257,925 / 118.60 | 483,889 / 128.13 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | 47,593 / 104.98 | 91,159 / 109.57 | 146,565 / 113.15 | 257,925 / 118.60 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | 40,264* / 101.92* | 44,703 / 103.08 | 51,357 / 104.61 | 65,476 / 107.31 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | 40,264* / 101.92* | 41,290 / 102.34 | 44,703 / 103.08 | 51,357 / 104.61 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | 57,065* / 106.31* | 69,269 / 108.52 | 85,743 / 110.65 | 118,519 / 114.26 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | 57,065* / 106.31* | 60,857 / 107.61 | 69,269 / 108.52 | 85,743 / 110.65 |

## wq = binary, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 add | 16,826 / 49.44 | 25,238 / 74.16 | 29,445 / 86.52 | 33,651 / 98.88 |
| MAC opt | 8·v × fp16 add | 16,826 / 49.44 | 25,238 / 74.16 | 29,445 / 86.52 | 33,651 / 98.88 |
| MAC int8 | 8·v × int16 add | 1,048 / 1.69 | 1,572 / 2.54 | 1,835 / 2.96 | 2,097 / 3.39 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | 9,515 / 13.83 | 24,584 / 14.87 | 44,679 / 15.78 | 85,782 / 17.46 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | 6,987 / 13.59 | 14,578 / 14.24 | 24,584 / 14.87 | 44,679 / 15.78 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | 9,515 / 13.83 | 24,584 / 14.87 | 44,679 / 15.78 | 85,782 / 17.46 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | 6,987 / 13.59 | 14,578 / 14.24 | 24,584 / 14.87 | 44,679 / 15.78 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | 5,923* / 13.08* | 6,574 / 13.23 | 7,851 / 13.53 | 10,401 / 14.09 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | 5,923* / 13.08* | 5,923 / 13.08 | 6,574 / 13.23 | 7,851 / 13.53 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | 5,923* / 13.08* | 6,574 / 13.23 | 7,851 / 13.53 | 10,401 / 14.09 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | 5,923* / 13.08* | 5,923 / 13.08 | 6,574 / 13.23 | 7,851 / 13.53 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 add | 16,826 / 49.44 | 25,238 / 74.16 | 29,445 / 86.52 | 33,651 / 98.88 |
| MAC opt | 8·v × fp16 add | 16,826 / 49.44 | 25,238 / 74.16 | 29,445 / 86.52 | 33,651 / 98.88 |
| MAC int8 | 8·v × int16 add | 1,048 / 1.69 | 1,572 / 2.54 | 1,835 / 2.96 | 2,097 / 3.39 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | 44,679 / 15.78 | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | 24,584 / 14.87 | 189,325 / 22.57 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | 44,679 / 15.78 | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | 24,584 / 14.87 | 189,325 / 22.57 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | 7,851 / 13.53 | 26,161 / 17.69 | 105,145 / 29.56 | 213,691 / 41.68 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | 6,574 / 13.23 | 16,292 / 15.53 | 46,646 / 22.29 | 105,145 / 29.56 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | 7,851 / 13.53 | 26,161 / 17.69 | 105,145 / 29.56 | 213,691 / 41.68 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | 6,574 / 13.23 | 16,292 / 15.53 | 46,646 / 22.29 | 105,145 / 29.56 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int2×fp16 mul + 8·v × fp16 add | 18,128 / 53.15 | 27,192 / 79.72 | 31,724 / 93.01 | 36,256 / 106.30 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 8·16b, 1R] + 16 × fp16 add | 19,030 / 27.67 | 49,169 / 29.74 | 89,359 / 31.56 | 171,564 / 34.93 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·16b, 1R] + 16 × fp16 add | 13,975 / 27.17 | 29,155 / 28.48 | 49,169 / 29.74 | 89,359 / 31.56 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 8·16b, 1R] + 16 × fp16 add | 11,846* / 26.17* | 13,147 / 26.46 | 15,702 / 27.07 | 20,803 / 28.18 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·16b, 1R] + 16 × fp16 add | 11,846* / 26.17* | 11,846 / 26.17 | 13,147 / 26.46 | 15,702 / 27.07 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 2R] + 16 × fp16 add | 16,135* / 26.79* | 18,358 / 27.07 | 22,765 / 27.67 | 31,490 / 28.75 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 2R] + 16 × fp16 add | 16,135* / 26.79* | 16,135 / 26.79 | 18,358 / 27.07 | 22,765 / 27.67 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int3×fp16 mul + 8·v × fp16 add | 22,886 / 68.08 | 34,328 / 102.11 | 40,050 / 119.13 | 45,771 / 136.15 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 8·16b, 1R] + 24 × fp16 add | 28,544 / 41.50 | 73,753 / 44.61 | 134,038 / 47.34 | 257,346 / 52.39 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·16b, 1R] + 24 × fp16 add | 20,962 / 40.76 | 43,733 / 42.72 | 73,753 / 44.61 | 134,038 / 47.34 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 8·16b, 1R] + 24 × fp16 add | 17,770* / 39.25* | 19,721 / 39.69 | 23,552 / 40.60 | 31,204 / 42.27 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·16b, 1R] + 24 × fp16 add | 17,770* / 39.25* | 17,770 / 39.25 | 19,721 / 39.69 | 23,552 / 40.60 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 3R] + 24 × fp16 add | 24,951* / 40.65* | 28,302 / 41.04 | 34,914 / 41.91 | 48,026 / 43.46 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 3R] + 24 × fp16 add | 24,951* / 40.65* | 24,951 / 40.65 | 28,302 / 41.04 | 34,914 / 41.91 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int4×fp16 mul + 8·v × fp16 add | 23,974 / 70.53 | 35,961 / 105.79 | 41,955 / 123.42 | 47,949 / 141.05 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 8·16b, 1R] + 32 × fp16 add | 38,059 / 55.33 | 98,337 / 59.48 | 178,718 / 63.12 | 343,128 / 69.85 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·16b, 1R] + 32 × fp16 add | 27,949 / 54.34 | 58,310 / 56.96 | 98,337 / 59.48 | 178,718 / 63.12 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 8·16b, 1R] + 32 × fp16 add | 23,693* / 52.33* | 26,294 / 52.93 | 31,403 / 54.13 | 41,605 / 56.36 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·16b, 1R] + 32 × fp16 add | 23,693* / 52.33* | 23,693 / 52.33 | 26,294 / 52.93 | 31,403 / 54.13 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 4R] + 32 × fp16 add | 33,859* / 54.83* | 38,320 / 55.37 | 47,070 / 56.55 | 64,455 / 58.66 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 4R] + 32 × fp16 add | 33,859* / 54.83* | 33,859 / 54.83 | 38,320 / 55.37 | 47,070 / 56.55 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int6×fp16 mul + 8·v × fp16 add | 26,930 / 80.24 | 40,395 / 120.36 | 47,127 / 140.43 | 53,859 / 160.49 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 8·16b, 1R] + 48 × fp16 add | 57,089 / 83.00 | 147,506 / 89.22 | 268,077 / 94.68 | 514,692 / 104.78 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·16b, 1R] + 48 × fp16 add | 41,924 / 81.51 | 87,465 / 85.45 | 147,506 / 89.22 | 268,077 / 94.68 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 8·16b, 1R] + 48 × fp16 add | 35,539* / 78.50* | 39,441 / 79.39 | 47,105 / 81.20 | 62,408 / 84.54 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·16b, 1R] + 48 × fp16 add | 35,539* / 78.50* | 35,539 / 78.50 | 39,441 / 79.39 | 47,105 / 81.20 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 6R] + 48 × fp16 add | 55,843* / 84.18* | 63,457 / 85.06 | 78,370 / 87.01 | 108,047 / 90.49 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 6R] + 48 × fp16 add | 55,843* / 84.18* | 55,843 / 84.18 | 63,457 / 85.06 | 78,370 / 87.01 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 29,555 / 83.75 | 44,332 / 125.62 | 51,720 / 146.56 | 59,109 / 167.50 |
| MAC opt | 8·v × int8×fp16 mul + 8·v × fp16 add | 29,676 / 84.81 | 44,513 / 127.21 | 51,932 / 148.41 | 59,351 / 169.61 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,653 / 10.06 | 8,479 / 15.09 | 9,893 / 17.61 | 11,306 / 20.12 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 8·16b, 1R] + 64 × fp16 add | 76,118 / 110.67 | 196,675 / 118.96 | 357,436 / 126.24 | 686,255 / 139.70 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·16b, 1R] + 64 × fp16 add | 55,899 / 108.68 | 116,621 / 113.93 | 196,675 / 118.96 | 357,436 / 126.24 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 8·16b, 1R] + 64 × fp16 add | 47,386* / 104.67* | 52,588 / 105.85 | 62,806 / 108.26 | 83,210 / 112.72 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·16b, 1R] + 64 × fp16 add | 47,386* / 104.67* | 47,386 / 104.67 | 52,588 / 105.85 | 62,806 / 108.26 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 8R] + 64 × fp16 add | 81,599* / 114.86* | 93,143 / 116.17 | 115,817 / 119.07 | 160,930 / 124.25 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 8R] + 64 × fp16 add | 81,599* / 114.86* | 81,599 / 114.86 | 93,143 / 116.17 | 115,817 / 119.07 |
