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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,428* / 6.38* | 2,744 / 6.56 | 3,222 / 6.82 | 4,267 / 7.30 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,428* / 6.38* | 2,502 / 6.42 | 2,744 / 6.56 | 3,222 / 6.82 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,428* / 6.38* | 2,744 / 6.56 | 3,222 / 6.82 | 4,267 / 7.30 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,428* / 6.38* | 2,502 / 6.42 | 2,744 / 6.56 | 3,222 / 6.82 |

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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,061 / 6.72 | 10,527 / 10.74 | 38,810 / 22.10 | 79,299 / 36.69 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,639 / 6.49 | 6,527 / 8.65 | 20,179 / 15.06 | 38,810 / 22.10 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,061 / 6.72 | 10,527 / 10.74 | 38,810 / 22.10 | 79,299 / 36.69 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,639 / 6.49 | 6,527 / 8.65 | 20,179 / 15.06 | 38,810 / 22.10 |

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
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,856* / 12.75* | 5,487 / 13.11 | 6,445 / 13.63 | 8,533 / 14.60 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,856* / 12.75* | 5,003 / 12.84 | 5,487 / 13.11 | 6,445 / 13.63 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | 5,478* / 12.80* | 6,640 / 13.12 | 8,396 / 13.58 | 12,605 / 14.89 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | 5,478* / 12.80* | 5,788 / 12.91 | 6,640 / 13.12 | 8,396 / 13.58 |

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
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,284* / 19.13* | 8,231 / 19.67 | 9,667 / 20.45 | 12,800 / 21.90 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,284* / 19.13* | 7,505 / 19.26 | 8,231 / 19.67 | 9,667 / 20.45 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | 8,254* / 19.22* | 10,070 / 19.67 | 12,725 / 20.27 | 19,068 / 22.09 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | 8,254* / 19.22* | 8,738 / 19.40 | 10,070 / 19.67 | 12,725 / 20.27 |

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
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,712* / 25.50* | 10,975 / 26.22 | 12,889 / 27.27 | 17,067 / 29.20 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,712* / 25.50* | 10,007 / 25.69 | 10,975 / 26.22 | 12,889 / 27.27 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | 11,200* / 25.68* | 14,426 / 26.41 | 18,165 / 27.29 | 26,416 / 29.45 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | 11,200* / 25.68* | 12,492 / 26.03 | 14,426 / 26.41 | 18,165 / 27.29 |

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
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,567* / 38.25* | 16,462 / 39.33 | 19,334 / 40.90 | 25,600 / 43.80 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,567* / 38.25* | 15,010 / 38.53 | 16,462 / 39.33 | 19,334 / 40.90 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | 18,276* / 38.84* | 22,964 / 39.88 | 29,229 / 41.17 | 43,729 / 44.68 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | 18,276* / 38.84* | 19,715 / 39.32 | 22,964 / 39.88 | 29,229 / 41.17 |

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
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,423* / 51.00* | 21,949 / 52.44 | 25,778 / 54.54 | 34,133 / 58.40 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,423* / 51.00* | 20,014 / 51.37 | 21,949 / 52.44 | 25,778 / 54.54 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | 25,478* / 52.11* | 32,572 / 53.61 | 42,003 / 55.41 | 64,510 / 60.59 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | 25,478* / 52.11* | 27,718 / 52.86 | 32,572 / 53.61 | 42,003 / 55.41 |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC opt | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.49 | 1,048 / 1.70 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 4,726 / # | 12,288 / # | 22,382 / # | 42,901 / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 3,456 / # | 7,280 / # | 12,288 / # | 22,382 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 4,726 / # | 12,288 / # | 22,382 / # | 42,901 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 3,456 / # | 7,280 / # | 12,288 / # | 22,382 / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 2,689* / 6.53* | 3,005 / 6.69 | 3,623 / 7.03 | 4,955 / 7.65 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 2,689* / 6.53* | 2,689 / 6.53 | 3,005 / 6.69 | 3,623 / 7.03 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 2,689* / 6.53* | 3,005 / 6.69 | 3,623 / 7.03 | 4,955 / 7.65 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 2,689* / 6.53* | 2,689 / 6.53 | 3,005 / 6.69 | 3,623 / 7.03 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC opt | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.49 | 1,048 / 1.70 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 22,382 / # | 166,177 / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 12,288 / # | 83,796 / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 22,382 / # | 166,177 / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 12,288 / # | 83,796 / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 3,623 / 7.03 | 13,439 / 12.20 | 50,756 / 26.56 | 104,247 / 45.00 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 3,005 / 6.69 | 7,882 / 9.41 | 23,307 / 17.56 | 50,756 / 26.56 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 3,623 / 7.03 | 13,439 / 12.20 | 50,756 / 26.56 | 104,247 / 45.00 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 3,005 / 6.69 | 7,882 / 9.41 | 23,307 / 17.56 | 50,756 / 26.56 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int2×fp16 mul + 4·v × fp16 add | 8,893 / 26.33 | 13,339 / 39.50 | 15,562 / 46.08 | 17,785 / 52.66 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 4·16b, 1R] + 8 × fp16 add | 9,453 / # | 24,576 / # | 44,763 / # | 85,803 / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·16b, 1R] + 8 × fp16 add | 6,911 / # | 14,560 / # | 24,576 / # | 44,763 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 4·16b, 1R] + 8 × fp16 add | 5,379* / 13.05* | 6,010 / 13.39 | 7,245 / 14.05 | 9,910 / 15.30 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·16b, 1R] + 8 × fp16 add | 5,379* / 13.05* | 5,379 / 13.05 | 6,010 / 13.39 | 7,245 / 14.05 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 2R] + 8 × fp16 add | 6,925* / 13.24* | 8,100 / 13.56 | 10,428 / 14.25 | 15,011 / 15.50 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 2R] + 8 × fp16 add | 6,925* / 13.24* | 6,925 / 13.24 | 8,100 / 13.56 | 10,428 / 14.25 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int3×fp16 mul + 4·v × fp16 add | 11,271 / 33.80 | 16,907 / 50.69 | 19,725 / 59.14 | 22,543 / 67.59 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 4·16b, 1R] + 12 × fp16 add | 14,179 / # | 36,864 / # | 67,145 / # | 128,704 / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·16b, 1R] + 12 × fp16 add | 10,367 / # | 21,840 / # | 36,864 / # | 67,145 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 4·16b, 1R] + 12 × fp16 add | 8,068* / 19.58* | 9,015 / 20.08 | 10,868 / 21.08 | 14,866 / 22.94 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·16b, 1R] + 12 × fp16 add | 8,068* / 19.58* | 8,068 / 19.58 | 9,015 / 20.08 | 10,868 / 21.08 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 3R] + 12 × fp16 add | 10,552* / 19.92* | 12,322 / 20.33 | 15,797 / 21.22 | 22,662 / 22.80 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 3R] + 12 × fp16 add | 10,552* / 19.92* | 10,552 / 19.92 | 12,322 / 20.33 | 15,797 / 21.22 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int4×fp16 mul + 4·v × fp16 add | 11,816 / 35.02 | 17,724 / 52.53 | 20,678 / 61.28 | 23,632 / 70.04 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 4·16b, 1R] + 16 × fp16 add | 18,905 / # | 49,153 / # | 89,526 / # | 171,606 / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·16b, 1R] + 16 × fp16 add | 13,822 / # | 29,120 / # | 49,153 / # | 89,526 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 4·16b, 1R] + 16 × fp16 add | 10,757* / 26.10* | 12,020 / 26.77 | 14,491 / 28.10 | 19,821 / 30.59 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·16b, 1R] + 16 × fp16 add | 10,757* / 26.10* | 10,757 / 26.10 | 12,020 / 26.77 | 14,491 / 28.10 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 4R] + 16 × fp16 add | 14,514* / 26.70* | 16,998 / 27.20 | 21,831 / 28.31 | 31,416 / 30.28 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 4R] + 16 × fp16 add | 14,514* / 26.70* | 14,514 / 26.70 | 16,998 / 27.20 | 21,831 / 28.31 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int6×fp16 mul + 4·v × fp16 add | 13,294 / 39.88 | 19,940 / 59.82 | 23,264 / 69.79 | 26,587 / 79.76 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 4·16b, 1R] + 24 × fp16 add | 28,358 / # | 73,729 / # | 134,289 / # | 257,409 / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·16b, 1R] + 24 × fp16 add | 20,733 / # | 43,679 / # | 73,729 / # | 134,289 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 4·16b, 1R] + 24 × fp16 add | 16,136* / 39.15* | 18,029 / 40.16 | 21,736 / 42.15 | 29,731 / 45.89 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·16b, 1R] + 24 × fp16 add | 16,136* / 39.15* | 16,136 / 39.15 | 18,029 / 40.16 | 21,736 / 42.15 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 6R] + 24 × fp16 add | 23,427* / 40.54* | 27,658 / 41.27 | 35,868 / 42.90 | 52,204 / 45.76 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 6R] + 24 × fp16 add | 23,427* / 40.54* | 23,427 / 40.54 | 27,658 / 41.27 | 35,868 / 42.90 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int8×fp16 mul + 4·v × fp16 add | 14,666 / 42.16 | 22,000 / 63.24 | 25,666 / 73.78 | 29,333 / 84.32 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 4·16b, 1R] + 32 × fp16 add | 37,810 / # | 98,305 / # | 179,052 / # | 343,212 / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·16b, 1R] + 32 × fp16 add | 27,644 / # | 58,239 / # | 98,305 / # | 179,052 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 4·16b, 1R] + 32 × fp16 add | 21,515* / 52.20* | 24,039 / 53.55 | 28,981 / 56.20 | 39,642 / 61.18 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·16b, 1R] + 32 × fp16 add | 21,515* / 52.20* | 21,515 / 52.20 | 24,039 / 53.55 | 28,981 / 56.20 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 8R] + 32 × fp16 add | 33,637* / 54.77* | 40,031 / 55.77 | 52,512 / 58.04 | 77,624 / 61.95 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 8R] + 32 × fp16 add | 33,637* / 54.77* | 33,637 / 54.77 | 40,031 / 55.77 | 52,512 / 58.04 |
