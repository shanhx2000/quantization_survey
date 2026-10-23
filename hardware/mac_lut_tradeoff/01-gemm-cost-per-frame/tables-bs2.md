# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 2

Generated 2026-10-23 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 2.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,901 / # | 4,676 / # | 8,260 / # | 15,492 / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,487 / # | 2,890 / # | 4,676 / # | 8,260 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,901 / # | 4,676 / # | 8,260 / # | 15,492 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,487 / # | 2,890 / # | 4,676 / # | 8,260 / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,242* / 3.22* | 1,379 / 3.30 | 1,662 / 3.46 | 2,147 / 3.71 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,242* / 3.22* | 1,242 / 3.22 | 1,379 / 3.30 | 1,662 / 3.46 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,242* / 3.22* | 1,379 / 3.30 | 1,662 / 3.46 | 2,147 / 3.71 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,242* / 3.22* | 1,242 / 3.22 | 1,379 / 3.30 | 1,662 / 3.46 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 7,662 / # | 58,691 / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 4,376 / # | 29,928 / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 7,662 / # | 58,691 / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 4,376 / # | 29,928 / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,662 / 3.46 | 5,409 / 5.53 | 20,052 / 10.49 | 37,203 / 19.23 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,379 / 3.30 | 3,188 / 4.20 | 9,334 / 7.59 | 20,052 / 10.49 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,662 / 3.46 | 5,409 / 5.53 | 20,052 / 10.49 | 37,203 / 19.23 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,379 / 3.30 | 3,188 / 4.20 | 9,334 / 7.59 | 20,052 / 10.49 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int2×int8 mul + 2·v × fp16 add | 4,389 / 12.99 | 6,583 / 19.48 | 7,680 / 22.72 | 8,778 / 25.97 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,802 / # | 9,352 / # | 16,520 / # | 30,984 / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,974 / # | 5,781 / # | 9,352 / # | 16,520 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,483* / 6.44* | 2,758 / 6.61 | 3,325 / 6.93 | 4,293 / 7.43 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,483* / 6.44* | 2,483 / 6.44 | 2,758 / 6.61 | 3,325 / 6.93 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | 2,817* / 6.46* | 3,343 / 6.58 | 4,421 / 6.86 | 6,042 / 7.33 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | 2,817* / 6.46* | 2,817 / 6.46 | 3,343 / 6.58 | 4,421 / 6.86 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int3×int8 mul + 2·v × fp16 add | 4,501 / 13.11 | 6,751 / 19.67 | 7,876 / 22.95 | 9,001 / 26.23 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 5,703 / # | 14,028 / # | 24,780 / # | 46,476 / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 4,461 / # | 8,671 / # | 14,028 / # | 24,780 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,725* / 9.66* | 4,137 / 9.91 | 4,987 / 10.39 | 6,440 / 11.14 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,725* / 9.66* | 3,725 / 9.66 | 4,137 / 9.91 | 4,987 / 10.39 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | 4,249* / 9.68* | 5,061 / 9.83 | 6,697 / 10.20 | 9,145 / 10.86 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | 4,249* / 9.68* | 4,249 / 9.68 | 5,061 / 9.83 | 6,697 / 10.20 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int4×int8 mul + 2·v × fp16 add | 4,635 / 13.19 | 6,952 / 19.78 | 8,111 / 23.08 | 9,270 / 26.37 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,604 / # | 18,704 / # | 33,040 / # | 61,968 / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,948 / # | 11,562 / # | 18,704 / # | 33,040 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,966* / 12.88* | 5,516 / 13.21 | 6,649 / 13.85 | 8,586 / 14.86 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,966* / 12.88* | 4,966 / 12.88 | 5,516 / 13.21 | 6,649 / 13.85 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | 5,763* / 12.93* | 6,926 / 13.11 | 9,512 / 13.83 | 13,251 / 14.71 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | 5,763* / 12.93* | 5,763 / 12.93 | 6,926 / 13.11 | 9,512 / 13.83 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int6×int8 mul + 2·v × fp16 add | 4,971 / 13.86 | 7,457 / 20.78 | 8,700 / 24.25 | 9,943 / 27.71 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 11,406 / # | 28,056 / # | 49,560 / # | 92,952 / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 8,922 / # | 17,343 / # | 28,056 / # | 49,560 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,449* / 19.32* | 8,274 / 19.82 | 9,974 / 20.78 | 12,879 / 22.28 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,449* / 19.32* | 7,449 / 19.32 | 8,274 / 19.82 | 9,974 / 20.78 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | 9,049* / 19.49* | 11,063 / 19.75 | 15,335 / 20.87 | 21,601 / 22.17 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | 9,049* / 19.49* | 9,049 / 19.49 | 11,063 / 19.75 | 15,335 / 20.87 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int8×int8 mul + 2·v × fp16 add | 5,259 / 14.19 | 7,888 / 21.29 | 9,203 / 24.84 | 10,517 / 28.39 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 15,208 / # | 37,408 / # | 66,079 / # | 123,936 / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 11,895 / # | 23,124 / # | 37,408 / # | 66,079 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,932* / 25.76* | 11,033 / 26.42 | 13,298 / 27.71 | 17,172 / 29.71 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,932* / 25.76* | 9,932 / 25.76 | 11,033 / 26.42 | 13,298 / 27.71 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | 12,656* / 26.14* | 15,718 / 26.50 | 22,032 / 28.11 | 31,463 / 29.90 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | 12,656* / 26.14* | 12,656 / 26.14 | 15,718 / 26.50 | 22,032 / 28.11 |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 2,374 / # | 6,185 / # | 11,253 / # | 21,495 / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,734 / # | 3,658 / # | 6,185 / # | 11,253 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 2,374 / # | 6,185 / # | 11,253 / # | 21,495 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,734 / # | 3,658 / # | 6,185 / # | 11,253 / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 1,315* / 3.26* | 1,489 / 3.36 | 1,839 / 3.55 | 2,618 / 3.90 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,315* / 3.26* | 1,315 / 3.26 | 1,489 / 3.36 | 1,839 / 3.55 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 1,315* / 3.26* | 1,489 / 3.36 | 1,839 / 3.55 | 2,618 / 3.90 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,315* / 3.26* | 1,315 / 3.26 | 1,489 / 3.36 | 1,839 / 3.55 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 11,253 / # | 83,042 / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 6,185 / # | 41,892 / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 11,253 / # | 83,042 / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 6,185 / # | 41,892 / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 1,839 / 3.55 | 6,693 / 6.25 | 25,534 / 12.67 | 54,165 / 22.82 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 1,489 / 3.36 | 3,840 / 4.52 | 12,101 / 8.97 | 25,534 / 12.67 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 1,839 / 3.55 | 6,693 / 6.25 | 25,534 / 12.67 | 54,165 / 22.82 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 1,489 / 3.36 | 3,840 / 4.52 | 12,101 / 8.97 | 25,534 / 12.67 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int2×fp16 mul + 2·v × fp16 add | 4,446 / 13.17 | 6,669 / 19.75 | 7,781 / 23.04 | 8,893 / 26.33 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 2·16b, 1R] + 4 × fp16 add | 4,747 / # | 12,370 / # | 22,505 / # | 42,990 / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·16b, 1R] + 4 × fp16 add | 3,467 / # | 7,316 / # | 12,370 / # | 22,505 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 2·16b, 1R] + 4 × fp16 add | 2,630* / 6.53* | 2,977 / 6.72 | 3,679 / 7.11 | 5,235 / 7.79 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·16b, 1R] + 4 × fp16 add | 2,630* / 6.53* | 2,630 / 6.53 | 2,977 / 6.72 | 3,679 / 7.11 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 2R] + 4 × fp16 add | 3,086* / 6.56* | 3,721 / 6.70 | 5,020 / 7.04 | 7,799 / 7.92 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 2R] + 4 × fp16 add | 3,086* / 6.56* | 3,086 / 6.56 | 3,721 / 6.70 | 5,020 / 7.04 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int3×fp16 mul + 2·v × fp16 add | 5,636 / 16.90 | 8,454 / 25.35 | 9,863 / 29.57 | 11,271 / 33.80 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 2·16b, 1R] + 6 × fp16 add | 7,121 / # | 18,555 / # | 33,758 / # | 64,486 / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·16b, 1R] + 6 × fp16 add | 5,201 / # | 10,973 / # | 18,555 / # | 33,758 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 2·16b, 1R] + 6 × fp16 add | 3,945* / 9.79* | 4,466 / 10.08 | 5,518 / 10.66 | 7,853 / 11.69 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·16b, 1R] + 6 × fp16 add | 3,945* / 9.79* | 3,945 / 9.79 | 4,466 / 10.08 | 5,518 / 10.66 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 3R] + 6 × fp16 add | 4,655* / 9.84* | 5,636 / 10.02 | 7,602 / 10.47 | 11,759 / 11.67 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 3R] + 6 × fp16 add | 4,655* / 9.84* | 4,655 / 9.84 | 5,636 / 10.02 | 7,602 / 10.47 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int4×fp16 mul + 2·v × fp16 add | 5,908 / 17.51 | 8,862 / 26.27 | 10,339 / 30.64 | 11,816 / 35.02 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 2·16b, 1R] + 8 × fp16 add | 9,494 / # | 24,739 / # | 45,011 / # | 85,981 / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·16b, 1R] + 8 × fp16 add | 6,935 / # | 14,631 / # | 24,739 / # | 45,011 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 2·16b, 1R] + 8 × fp16 add | 5,260* / 13.05* | 5,955 / 13.44 | 7,358 / 14.21 | 10,471 / 15.58 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·16b, 1R] + 8 × fp16 add | 5,260* / 13.05* | 5,260 / 13.05 | 5,955 / 13.44 | 7,358 / 14.21 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 4R] + 8 × fp16 add | 6,343* / 13.15* | 7,743 / 13.38 | 10,501 / 13.95 | 16,292 / 15.50 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 4R] + 8 × fp16 add | 6,343* / 13.15* | 6,343 / 13.15 | 7,743 / 13.38 | 10,501 / 13.95 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int6×fp16 mul + 2·v × fp16 add | 6,647 / 19.94 | 9,970 / 29.91 | 11,632 / 34.89 | 13,294 / 39.88 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 2·16b, 1R] + 12 × fp16 add | 14,242 / # | 37,109 / # | 67,516 / # | 128,971 / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·16b, 1R] + 12 × fp16 add | 10,402 / # | 21,947 / # | 37,109 / # | 67,516 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 2·16b, 1R] + 12 × fp16 add | 7,890* / 19.58* | 8,932 / 20.17 | 11,037 / 21.32 | 15,706 / 23.37 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·16b, 1R] + 12 × fp16 add | 7,890* / 19.58* | 7,890 / 19.58 | 8,932 / 20.17 | 11,037 / 21.32 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 6R] + 12 × fp16 add | 10,070* / 19.88* | 12,489 / 20.21 | 17,246 / 21.07 | 27,052 / 23.46 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 6R] + 12 × fp16 add | 10,070* / 19.88* | 10,070 / 19.88 | 12,489 / 20.21 | 17,246 / 21.07 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int8×fp16 mul + 2·v × fp16 add | 7,333 / 21.08 | 11,000 / 31.62 | 12,833 / 36.89 | 14,666 / 42.16 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 2·16b, 1R] + 16 × fp16 add | 18,989 / # | 49,479 / # | 90,021 / # | 171,962 / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·16b, 1R] + 16 × fp16 add | 13,869 / # | 29,262 / # | 49,479 / # | 90,021 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 2·16b, 1R] + 16 × fp16 add | 10,520* / 26.10* | 11,909 / 26.89 | 14,716 / 28.42 | 20,942 / 31.16 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·16b, 1R] + 16 × fp16 add | 10,520* / 26.10* | 10,520 / 26.10 | 11,909 / 26.89 | 14,716 / 28.42 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 8R] + 16 × fp16 add | 14,905* / 26.85* | 18,322 / 27.36 | 25,237 / 28.68 | 40,054 / 31.81 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 8R] + 16 × fp16 add | 14,905* / 26.85* | 14,905 / 26.85 | 18,322 / 27.36 | 25,237 / 28.68 |
