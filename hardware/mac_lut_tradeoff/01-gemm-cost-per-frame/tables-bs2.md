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
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,901 / 3.32 | 4,676 / 3.61 | 8,260 / 3.87 | 15,492 / 4.29 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,487 / 3.25 | 2,890 / 3.44 | 4,676 / 3.61 | 8,260 / 3.87 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,901 / 3.32 | 4,676 / 3.61 | 8,260 / 3.87 | 15,492 / 4.29 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,487 / 3.25 | 2,890 / 3.44 | 4,676 / 3.61 | 8,260 / 3.87 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,242* / 3.17* | 1,379 / 3.21 | 1,662 / 3.28 | 2,147 / 3.41 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,242* / 3.17* | 1,242 / 3.17 | 1,379 / 3.21 | 1,662 / 3.28 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,242* / 3.17* | 1,379 / 3.21 | 1,662 / 3.28 | 2,147 / 3.41 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,242* / 3.17* | 1,242 / 3.17 | 1,379 / 3.21 | 1,662 / 3.28 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 7,662 / 3.84 | 58,691 / 6.97 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 4,376 / 3.59 | 29,928 / 5.24 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 7,662 / 3.84 | 58,691 / 6.97 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 4,376 / 3.59 | 29,928 / 5.24 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,662 / 3.28 | 5,409 / 4.15 | 20,052 / 5.86 | 37,203 / 9.12 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,379 / 3.21 | 3,188 / 3.60 | 9,334 / 5.06 | 20,052 / 5.86 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,662 / 3.28 | 5,409 / 4.15 | 20,052 / 5.86 | 37,203 / 9.12 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,379 / 3.21 | 3,188 / 3.60 | 9,334 / 5.06 | 20,052 / 5.86 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int2×int8 mul + 2·v × fp16 add | 4,389 / 12.99 | 6,583 / 19.48 | 7,680 / 22.72 | 8,778 / 25.97 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,802 / 6.64 | 9,352 / 7.23 | 16,520 / 7.74 | 30,984 / 8.57 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,974 / 6.51 | 5,781 / 6.88 | 9,352 / 7.23 | 16,520 / 7.74 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,483* / 6.34* | 2,758 / 6.41 | 3,325 / 6.56 | 4,293 / 6.81 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,483* / 6.34* | 2,483 / 6.34 | 2,758 / 6.41 | 3,325 / 6.56 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | 2,817* / 6.38* | 3,343 / 6.44 | 4,421 / 6.59 | 6,042 / 6.88 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | 2,817* / 6.38* | 2,817 / 6.38 | 3,343 / 6.44 | 4,421 / 6.59 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int3×int8 mul + 2·v × fp16 add | 4,501 / 13.11 | 6,751 / 19.67 | 7,876 / 22.95 | 9,001 / 26.23 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 5,703 / 9.96 | 14,028 / 10.84 | 24,780 / 11.61 | 46,476 / 12.86 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 4,461 / 9.76 | 8,671 / 10.33 | 14,028 / 10.84 | 24,780 / 11.61 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,725* / 9.51* | 4,137 / 9.62 | 4,987 / 9.84 | 6,440 / 10.22 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,725* / 9.51* | 3,725 / 9.51 | 4,137 / 9.62 | 4,987 / 9.84 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | 4,249* / 9.59* | 5,061 / 9.67 | 6,697 / 9.90 | 9,145 / 10.34 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | 4,249* / 9.59* | 4,249 / 9.59 | 5,061 / 9.67 | 6,697 / 9.90 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int4×int8 mul + 2·v × fp16 add | 4,635 / 13.19 | 6,952 / 19.78 | 8,111 / 23.08 | 9,270 / 26.37 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,604 / 13.29 | 18,704 / 14.45 | 33,040 / 15.48 | 61,968 / 17.14 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,948 / 13.02 | 11,562 / 13.77 | 18,704 / 14.45 | 33,040 / 15.48 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,966* / 12.68* | 5,516 / 12.82 | 6,649 / 13.13 | 8,586 / 13.63 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,966* / 12.68* | 4,966 / 12.68 | 5,516 / 12.82 | 6,649 / 13.13 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | 5,763* / 12.83* | 6,926 / 12.93 | 9,512 / 13.44 | 13,251 / 13.97 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | 5,763* / 12.83* | 5,763 / 12.83 | 6,926 / 12.93 | 9,512 / 13.44 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int6×int8 mul + 2·v × fp16 add | 4,971 / 13.86 | 7,457 / 20.78 | 8,700 / 24.25 | 9,943 / 27.71 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 11,406 / 19.93 | 28,056 / 21.68 | 49,560 / 23.22 | 92,952 / 25.72 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 8,922 / 19.53 | 17,343 / 20.65 | 28,056 / 21.68 | 49,560 / 23.22 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,449* / 19.02* | 8,274 / 19.23 | 9,974 / 19.69 | 12,879 / 20.44 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,449* / 19.02* | 7,449 / 19.02 | 8,274 / 19.23 | 9,974 / 19.69 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | 9,049* / 19.36* | 11,063 / 19.52 | 15,335 / 20.39 | 21,601 / 21.26 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | 9,049* / 19.36* | 9,049 / 19.36 | 11,063 / 19.52 | 15,335 / 20.39 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int8×int8 mul + 2·v × fp16 add | 5,259 / 14.19 | 7,888 / 21.29 | 9,203 / 24.84 | 10,517 / 28.39 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 15,208 / 26.57 | 37,408 / 28.91 | 66,079 / 30.95 | 123,936 / 34.29 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 11,895 / 26.03 | 23,124 / 27.54 | 37,408 / 28.91 | 66,079 / 30.95 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,932* / 25.37* | 11,033 / 25.65 | 13,298 / 26.25 | 17,172 / 27.26 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,932* / 25.37* | 9,932 / 25.37 | 11,033 / 25.65 | 13,298 / 26.25 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | 12,656* / 25.98* | 15,718 / 26.22 | 22,032 / 27.53 | 31,463 / 28.82 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | 12,656* / 25.98* | 12,656 / 25.98 | 15,718 / 26.22 | 22,032 / 27.53 |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 2,374 / 3.44 | 6,185 / 3.76 | 11,253 / 4.05 | 21,495 / 4.48 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,734 / 3.36 | 3,658 / 3.56 | 6,185 / 3.76 | 11,253 / 4.05 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 2,374 / 3.44 | 6,185 / 3.76 | 11,253 / 4.05 | 21,495 / 4.48 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,734 / 3.36 | 3,658 / 3.56 | 6,185 / 3.76 | 11,253 / 4.05 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 1,315* / 3.20* | 1,489 / 3.24 | 1,839 / 3.33 | 2,618 / 3.46 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,315* / 3.20* | 1,315 / 3.20 | 1,489 / 3.24 | 1,839 / 3.33 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 1,315* / 3.20* | 1,489 / 3.24 | 1,839 / 3.33 | 2,618 / 3.46 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,315* / 3.20* | 1,315 / 3.20 | 1,489 / 3.24 | 1,839 / 3.33 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 11,253 / 4.05 | 83,042 / 7.42 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 6,185 / 3.76 | 41,892 / 5.47 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 11,253 / 4.05 | 83,042 / 7.42 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 6,185 / 3.76 | 41,892 / 5.47 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 1,839 / 3.33 | 6,693 / 4.49 | 25,534 / 6.72 | 54,165 / 10.71 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 1,489 / 3.24 | 3,840 / 3.76 | 12,101 / 5.70 | 25,534 / 6.72 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 1,839 / 3.33 | 6,693 / 4.49 | 25,534 / 6.72 | 54,165 / 10.71 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 1,489 / 3.24 | 3,840 / 3.76 | 12,101 / 5.70 | 25,534 / 6.72 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int2×fp16 mul + 2·v × fp16 add | 4,446 / 13.17 | 6,669 / 19.75 | 7,781 / 23.04 | 8,893 / 26.33 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 2·16b, 1R] + 4 × fp16 add | 4,747 / 6.88 | 12,370 / 7.53 | 22,505 / 8.09 | 42,990 / 8.97 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·16b, 1R] + 4 × fp16 add | 3,467 / 6.72 | 7,316 / 7.12 | 12,370 / 7.53 | 22,505 / 8.09 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 2·16b, 1R] + 4 × fp16 add | 2,630* / 6.40* | 2,977 / 6.49 | 3,679 / 6.66 | 5,235 / 6.93 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·16b, 1R] + 4 × fp16 add | 2,630* / 6.40* | 2,630 / 6.40 | 2,977 / 6.49 | 3,679 / 6.66 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 2R] + 4 × fp16 add | 3,086* / 6.46* | 3,721 / 6.53 | 5,020 / 6.71 | 7,799 / 7.20 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 2R] + 4 × fp16 add | 3,086* / 6.46* | 3,086 / 6.46 | 3,721 / 6.53 | 5,020 / 6.71 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int3×fp16 mul + 2·v × fp16 add | 5,636 / 16.90 | 8,454 / 25.35 | 9,863 / 29.57 | 11,271 / 33.80 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 2·16b, 1R] + 6 × fp16 add | 7,121 / 10.32 | 18,555 / 11.29 | 33,758 / 12.14 | 64,486 / 13.45 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·16b, 1R] + 6 × fp16 add | 5,201 / 10.08 | 10,973 / 10.67 | 18,555 / 11.29 | 33,758 / 12.14 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 2·16b, 1R] + 6 × fp16 add | 3,945* / 9.60* | 4,466 / 9.73 | 5,518 / 10.00 | 7,853 / 10.39 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·16b, 1R] + 6 × fp16 add | 3,945* / 9.60* | 3,945 / 9.60 | 4,466 / 9.73 | 5,518 / 10.00 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 3R] + 6 × fp16 add | 4,655* / 9.73* | 5,636 / 9.82 | 7,602 / 10.09 | 11,759 / 10.83 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 3R] + 6 × fp16 add | 4,655* / 9.73* | 4,655 / 9.73 | 5,636 / 9.82 | 7,602 / 10.09 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int4×fp16 mul + 2·v × fp16 add | 5,908 / 17.51 | 8,862 / 26.27 | 10,339 / 30.64 | 11,816 / 35.02 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 2·16b, 1R] + 8 × fp16 add | 9,494 / 13.76 | 24,739 / 15.05 | 45,011 / 16.18 | 85,981 / 17.94 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·16b, 1R] + 8 × fp16 add | 6,935 / 13.44 | 14,631 / 14.23 | 24,739 / 15.05 | 45,011 / 16.18 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 2·16b, 1R] + 8 × fp16 add | 5,260* / 12.81* | 5,955 / 12.97 | 7,358 / 13.33 | 10,471 / 13.86 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·16b, 1R] + 8 × fp16 add | 5,260* / 12.81* | 5,260 / 12.81 | 5,955 / 12.97 | 7,358 / 13.33 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 4R] + 8 × fp16 add | 6,343* / 13.02* | 7,743 / 13.15 | 10,501 / 13.52 | 16,292 / 14.55 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 4R] + 8 × fp16 add | 6,343* / 13.02* | 6,343 / 13.02 | 7,743 / 13.15 | 10,501 / 13.52 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int6×fp16 mul + 2·v × fp16 add | 6,647 / 19.94 | 9,970 / 29.91 | 11,632 / 34.89 | 13,294 / 39.88 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 2·16b, 1R] + 12 × fp16 add | 14,242 / 20.63 | 37,109 / 22.58 | 67,516 / 24.27 | 128,971 / 26.90 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·16b, 1R] + 12 × fp16 add | 10,402 / 20.16 | 21,947 / 21.35 | 37,109 / 22.58 | 67,516 / 24.27 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 2·16b, 1R] + 12 × fp16 add | 7,890* / 19.21* | 8,932 / 19.46 | 11,037 / 19.99 | 15,706 / 20.78 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·16b, 1R] + 12 × fp16 add | 7,890* / 19.21* | 7,890 / 19.21 | 8,932 / 19.46 | 11,037 / 19.99 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 6R] + 12 × fp16 add | 10,070* / 19.71* | 12,489 / 19.92 | 17,246 / 20.54 | 27,052 / 22.28 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 6R] + 12 × fp16 add | 10,070* / 19.71* | 10,070 / 19.71 | 12,489 / 19.92 | 17,246 / 20.54 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int8×fp16 mul + 2·v × fp16 add | 7,333 / 21.08 | 11,000 / 31.62 | 12,833 / 36.89 | 14,666 / 42.16 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 2·16b, 1R] + 16 × fp16 add | 18,989 / 27.51 | 49,479 / 30.11 | 90,021 / 32.37 | 171,962 / 35.87 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·16b, 1R] + 16 × fp16 add | 13,869 / 26.89 | 29,262 / 28.46 | 49,479 / 30.11 | 90,021 / 32.37 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 2·16b, 1R] + 16 × fp16 add | 10,520* / 25.61* | 11,909 / 25.95 | 14,716 / 26.66 | 20,942 / 27.71 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·16b, 1R] + 16 × fp16 add | 10,520* / 25.61* | 10,520 / 25.61 | 11,909 / 25.95 | 14,716 / 26.66 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 8R] + 16 × fp16 add | 14,905* / 26.60* | 18,322 / 26.93 | 25,237 / 27.90 | 40,054 / 30.40 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 8R] + 16 × fp16 add | 14,905* / 26.60* | 14,905 / 26.60 | 18,322 / 26.93 | 25,237 / 27.90 |
