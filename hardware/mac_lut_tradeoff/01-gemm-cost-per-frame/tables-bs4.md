# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 4

Generated 2026-10-23 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 4.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC opt | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.49 | 1,048 / 1.70 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,428* / 6.30* | 2,744 / 6.39 | 3,222 / 6.51 | 4,267 / 6.70 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,428* / 6.30* | 2,502 / 6.34 | 2,744 / 6.39 | 3,222 / 6.51 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,428* / 6.30* | 2,744 / 6.39 | 3,222 / 6.51 | 4,267 / 6.70 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,428* / 6.30* | 2,502 / 6.34 | 2,744 / 6.39 | 3,222 / 6.51 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC opt | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.49 | 1,048 / 1.70 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,061 / 6.45 | 10,527 / 8.23 | 38,810 / 12.66 | 79,299 / 17.80 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,639 / 6.35 | 6,527 / 7.27 | 20,179 / 9.66 | 38,810 / 12.66 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,061 / 6.45 | 10,527 / 8.23 | 38,810 / 12.66 | 79,299 / 17.80 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,639 / 6.35 | 6,527 / 7.27 | 20,179 / 9.66 | 38,810 / 12.66 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int2×int8 mul + 4·v × fp16 add | 8,778 / 25.97 | 13,166 / 38.96 | 15,361 / 45.45 | 17,555 / 51.94 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,856* / 12.60* | 5,487 / 12.78 | 6,445 / 13.02 | 8,533 / 13.40 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,856* / 12.60* | 5,003 / 12.67 | 5,487 / 12.78 | 6,445 / 13.02 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | 5,478* / 12.68* | 6,640 / 12.88 | 8,396 / 13.12 | 12,605 / 13.86 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | 5,478* / 12.68* | 5,788 / 12.78 | 6,640 / 12.88 | 8,396 / 13.12 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int3×int8 mul + 4·v × fp16 add | 9,001 / 26.23 | 13,502 / 39.34 | 15,753 / 45.90 | 18,003 / 52.45 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,284* / 18.90* | 8,231 / 19.17 | 9,667 / 19.53 | 12,800 / 20.10 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,284* / 18.90* | 7,505 / 19.01 | 8,231 / 19.17 | 9,667 / 19.53 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | 8,254* / 19.08* | 10,070 / 19.38 | 12,725 / 19.74 | 19,068 / 20.89 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | 8,254* / 19.08* | 8,738 / 19.24 | 10,070 / 19.38 | 12,725 / 19.74 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int4×int8 mul + 4·v × fp16 add | 9,270 / 26.37 | 13,904 / 39.56 | 16,222 / 46.16 | 18,539 / 52.75 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,712* / 25.20* | 10,975 / 25.56 | 12,889 / 26.04 | 17,067 / 26.80 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,712* / 25.20* | 10,007 / 25.34 | 10,975 / 25.56 | 12,889 / 26.04 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | 11,200* / 25.52* | 14,426 / 26.01 | 18,165 / 26.54 | 26,416 / 28.08 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | 11,200* / 25.52* | 12,492 / 25.80 | 14,426 / 26.01 | 18,165 / 26.54 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int6×int8 mul + 4·v × fp16 add | 9,943 / 27.71 | 14,914 / 41.57 | 17,400 / 48.50 | 19,886 / 55.43 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,567* / 37.80* | 16,462 / 38.35 | 19,334 / 39.05 | 25,600 / 40.20 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,567* / 37.80* | 15,010 / 38.01 | 16,462 / 38.35 | 19,334 / 39.05 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | 18,276* / 38.59* | 22,964 / 39.37 | 29,229 / 40.24 | 43,729 / 42.96 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | 18,276* / 38.59* | 19,715 / 39.03 | 22,964 / 39.37 | 29,229 / 40.24 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int8×int8 mul + 4·v × fp16 add | 10,517 / 28.39 | 15,776 / 42.58 | 18,406 / 49.68 | 21,035 / 56.78 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,423* / 50.40* | 21,949 / 51.13 | 25,778 / 52.07 | 34,133 / 53.59 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,423* / 50.40* | 20,014 / 50.68 | 21,949 / 51.13 | 25,778 / 52.07 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | 25,478* / 51.80* | 32,572 / 52.99 | 42,003 / 54.29 | 64,510 / 58.52 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | 25,478* / 51.80* | 27,718 / 52.50 | 32,572 / 52.99 | 42,003 / 54.29 |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC opt | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.49 | 1,048 / 1.70 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 4,726 / 6.85 | 12,288 / 7.45 | 22,382 / 7.93 | 42,901 / 8.73 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 3,456 / 6.72 | 7,280 / 7.07 | 12,288 / 7.45 | 22,382 / 7.93 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 4,726 / 6.85 | 12,288 / 7.45 | 22,382 / 7.93 | 42,901 / 8.73 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 3,456 / 6.72 | 7,280 / 7.07 | 12,288 / 7.45 | 22,382 / 7.93 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 2,689* / 6.42* | 3,005 / 6.49 | 3,623 / 6.63 | 4,955 / 6.88 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 2,689* / 6.42* | 2,689 / 6.42 | 3,005 / 6.49 | 3,623 / 6.63 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 2,689* / 6.42* | 3,005 / 6.49 | 3,623 / 6.63 | 4,955 / 6.88 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 2,689* / 6.42* | 2,689 / 6.42 | 3,005 / 6.49 | 3,623 / 6.63 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC opt | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.49 | 1,048 / 1.70 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 22,382 / 7.93 | 166,177 / 13.67 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 12,288 / 7.45 | 83,796 / 10.50 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 22,382 / 7.93 | 166,177 / 13.67 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 12,288 / 7.45 | 83,796 / 10.50 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 3,623 / 6.63 | 13,439 / 8.94 | 50,756 / 14.64 | 104,247 / 21.15 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 3,005 / 6.49 | 7,882 / 7.64 | 23,307 / 11.10 | 50,756 / 14.64 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 3,623 / 6.63 | 13,439 / 8.94 | 50,756 / 14.64 | 104,247 / 21.15 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 3,005 / 6.49 | 7,882 / 7.64 | 23,307 / 11.10 | 50,756 / 14.64 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int2×fp16 mul + 4·v × fp16 add | 8,893 / 26.33 | 13,339 / 39.50 | 15,562 / 46.08 | 17,785 / 52.66 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 4·16b, 1R] + 8 × fp16 add | 9,453 / 13.71 | 24,576 / 14.89 | 44,763 / 15.86 | 85,803 / 17.46 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·16b, 1R] + 8 × fp16 add | 6,911 / 13.45 | 14,560 / 14.14 | 24,576 / 14.89 | 44,763 / 15.86 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 4·16b, 1R] + 8 × fp16 add | 5,379* / 12.83* | 6,010 / 12.97 | 7,245 / 13.26 | 9,910 / 13.76 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·16b, 1R] + 8 × fp16 add | 5,379* / 12.83* | 5,379 / 12.83 | 6,010 / 12.97 | 7,245 / 13.26 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 2R] + 8 × fp16 add | 6,925* / 13.03* | 8,100 / 13.18 | 10,428 / 13.52 | 15,011 / 14.07 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 2R] + 8 × fp16 add | 6,925* / 13.03* | 6,925 / 13.03 | 8,100 / 13.18 | 10,428 / 13.52 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int3×fp16 mul + 4·v × fp16 add | 11,271 / 33.80 | 16,907 / 50.69 | 19,725 / 59.14 | 22,543 / 67.59 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 4·16b, 1R] + 12 × fp16 add | 14,179 / 20.56 | 36,864 / 22.34 | 67,145 / 23.79 | 128,704 / 26.19 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·16b, 1R] + 12 × fp16 add | 10,367 / 20.17 | 21,840 / 21.21 | 36,864 / 22.34 | 67,145 / 23.79 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 4·16b, 1R] + 12 × fp16 add | 8,068* / 19.25* | 9,015 / 19.46 | 10,868 / 19.90 | 14,866 / 20.64 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·16b, 1R] + 12 × fp16 add | 8,068* / 19.25* | 8,068 / 19.25 | 9,015 / 19.46 | 10,868 / 19.90 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 3R] + 12 × fp16 add | 10,552* / 19.67* | 12,322 / 19.88 | 15,797 / 20.36 | 22,662 / 21.15 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 3R] + 12 × fp16 add | 10,552* / 19.67* | 10,552 / 19.67 | 12,322 / 19.88 | 15,797 / 20.36 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int4×fp16 mul + 4·v × fp16 add | 11,816 / 35.02 | 17,724 / 52.53 | 20,678 / 61.28 | 23,632 / 70.04 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 4·16b, 1R] + 16 × fp16 add | 18,905 / 27.41 | 49,153 / 29.78 | 89,526 / 31.72 | 171,606 / 34.92 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·16b, 1R] + 16 × fp16 add | 13,822 / 26.90 | 29,120 / 28.29 | 49,153 / 29.78 | 89,526 / 31.72 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 4·16b, 1R] + 16 × fp16 add | 10,757* / 25.66* | 12,020 / 25.94 | 14,491 / 26.53 | 19,821 / 27.52 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·16b, 1R] + 16 × fp16 add | 10,757* / 25.66* | 10,757 / 25.66 | 12,020 / 25.94 | 14,491 / 26.53 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 4R] + 16 × fp16 add | 14,514* / 26.40* | 16,998 / 26.67 | 21,831 / 27.34 | 31,416 / 28.40 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 4R] + 16 × fp16 add | 14,514* / 26.40* | 14,514 / 26.40 | 16,998 / 26.67 | 21,831 / 27.34 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int6×fp16 mul + 4·v × fp16 add | 13,294 / 39.88 | 19,940 / 59.82 | 23,264 / 69.79 | 26,587 / 79.76 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 4·16b, 1R] + 24 × fp16 add | 28,358 / 41.12 | 73,729 / 44.67 | 134,289 / 47.57 | 257,409 / 52.38 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·16b, 1R] + 24 × fp16 add | 20,733 / 40.35 | 43,679 / 42.43 | 73,729 / 44.67 | 134,289 / 47.57 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 4·16b, 1R] + 24 × fp16 add | 16,136* / 38.49* | 18,029 / 38.91 | 21,736 / 39.79 | 29,731 / 41.28 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·16b, 1R] + 24 × fp16 add | 16,136* / 38.49* | 16,136 / 38.49 | 18,029 / 38.91 | 21,736 / 39.79 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 6R] + 24 × fp16 add | 23,427* / 40.15* | 27,658 / 40.59 | 35,868 / 41.68 | 52,204 / 43.43 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 6R] + 24 × fp16 add | 23,427* / 40.15* | 23,427 / 40.15 | 27,658 / 40.59 | 35,868 / 41.68 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int8×fp16 mul + 4·v × fp16 add | 14,666 / 42.16 | 22,000 / 63.24 | 25,666 / 73.78 | 29,333 / 84.32 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 4·16b, 1R] + 32 × fp16 add | 37,810 / 54.82 | 98,305 / 59.56 | 179,052 / 63.43 | 343,212 / 69.84 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·16b, 1R] + 32 × fp16 add | 27,644 / 53.80 | 58,239 / 56.57 | 98,305 / 59.56 | 179,052 / 63.43 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 4·16b, 1R] + 32 × fp16 add | 21,515* / 51.32* | 24,039 / 51.88 | 28,981 / 53.06 | 39,642 / 55.04 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·16b, 1R] + 32 × fp16 add | 21,515* / 51.32* | 21,515 / 51.32 | 24,039 / 51.88 | 28,981 / 53.06 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 8R] + 32 × fp16 add | 33,637* / 54.28* | 40,031 / 54.94 | 52,512 / 56.56 | 77,624 / 59.16 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 8R] + 32 × fp16 add | 33,637* / 54.28* | 33,637 / 54.28 | 40,031 / 54.94 | 52,512 / 56.56 |
