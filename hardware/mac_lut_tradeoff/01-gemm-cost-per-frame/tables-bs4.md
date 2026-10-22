# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 4

Generated 2026-10-22 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table under 64 bytes, costed as the smallest table at or above that. `—` = not costed: ternary register-file tables above v = 6.
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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int2×int8 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int3×int8 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int4×int8 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int6×int8 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |

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
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC opt | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.49 | 1,048 / 1.70 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC opt | 4·v × fp16 add | 8,241 / 24.48 | 12,362 / 36.72 | 14,422 / 42.84 | 16,483 / 48.95 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.49 | 1,048 / 1.70 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int2×fp16 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 4·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 4·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int3×fp16 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 4·16b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·16b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 4·16b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·16b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int4×fp16 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 4·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 4·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int6×fp16 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 4·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 4·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,380 / 41.50 | 21,570 / 62.25 | 25,165 / 72.63 | 28,760 / 83.01 |
| MAC opt | 4·v × int8×fp16 mul + 4·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,800 / 4.76 | 4,200 / 7.14 | 4,900 / 8.33 | 5,600 / 9.52 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 4·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 4·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
