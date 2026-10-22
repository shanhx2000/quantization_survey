# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 8

Generated 2026-10-22 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table under 64 bytes, costed as the smallest table at or above that. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 8.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 add | 16,483 / 48.95 | 24,724 / 73.43 | 28,845 / 85.67 | 32,966 / 97.91 |
| MAC opt | 8·v × fp16 add | 16,483 / 48.95 | 24,724 / 73.43 | 28,845 / 85.67 | 32,966 / 97.91 |
| MAC int8 | 8·v × int16 add | 1,048 / 1.70 | 1,572 / 2.55 | 1,835 / 2.97 | 2,097 / 3.40 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 add | 16,483 / 48.95 | 24,724 / 73.43 | 28,845 / 85.67 | 32,966 / 97.91 |
| MAC opt | 8·v × fp16 add | 16,483 / 48.95 | 24,724 / 73.43 | 28,845 / 85.67 | 32,966 / 97.91 |
| MAC int8 | 8·v × int16 add | 1,048 / 1.70 | 1,572 / 2.55 | 1,835 / 2.97 | 2,097 / 3.40 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int2×int8 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int3×int8 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int4×int8 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int6×int8 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int8×int8 mul + 8·v × fp16 add | 21,035 / 56.78 | 31,552 / 85.17 | 36,811 / 99.36 | 42,070 / 113.56 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 add | 16,483 / 48.95 | 24,724 / 73.43 | 28,845 / 85.67 | 32,966 / 97.91 |
| MAC opt | 8·v × fp16 add | 16,483 / 48.95 | 24,724 / 73.43 | 28,845 / 85.67 | 32,966 / 97.91 |
| MAC int8 | 8·v × int16 add | 1,048 / 1.70 | 1,572 / 2.55 | 1,835 / 2.97 | 2,097 / 3.40 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 add | 16,483 / 48.95 | 24,724 / 73.43 | 28,845 / 85.67 | 32,966 / 97.91 |
| MAC opt | 8·v × fp16 add | 16,483 / 48.95 | 24,724 / 73.43 | 28,845 / 85.67 | 32,966 / 97.91 |
| MAC int8 | 8·v × int16 add | 1,048 / 1.70 | 1,572 / 2.55 | 1,835 / 2.97 | 2,097 / 3.40 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int2×fp16 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 8·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 8·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int3×fp16 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 8·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 8·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int4×fp16 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 8·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 8·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int6×fp16 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 8·16b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·16b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 8·16b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·16b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int8×fp16 mul + 8·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 8·16b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·16b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 8·16b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·16b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
