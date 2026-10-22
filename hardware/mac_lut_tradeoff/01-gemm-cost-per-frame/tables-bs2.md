# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 2

Generated 2026-10-22 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table under 64 bytes, costed as the smallest table at or above that. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 2.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int2×int8 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int3×int8 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int4×int8 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int6×int8 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int8×int8 mul + 2·v × fp16 add | 5,259 / 14.19 | 7,888 / 21.29 | 9,203 / 24.84 | 10,517 / 28.39 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int2×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 2·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 2·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int3×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 2·16b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·16b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 2·16b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·16b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int4×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 2·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 2·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int6×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 2·16b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·16b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 2·16b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·16b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int8×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 2·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 2·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
