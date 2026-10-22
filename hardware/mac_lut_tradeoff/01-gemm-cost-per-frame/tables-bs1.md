# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 1

Generated 2026-10-22 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table under 64 bytes, costed as the smallest table at or above that. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 1.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 655* / 1.64* | 757 / 1.70 | 967 / 1.82 | 1,305 / 2.00 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 655* / 1.64* | 655 / 1.64 | 757 / 1.70 | 967 / 1.82 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 655* / 1.64* | 757 / 1.70 | 967 / 1.82 | 1,305 / 2.00 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 655* / 1.64* | 655 / 1.64 | 757 / 1.70 | 967 / 1.82 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | # / # | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | # / # | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | # / # | # / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 967 / 1.82 | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 757 / 1.70 | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 967 / 1.82 | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 757 / 1.70 | # / # | # / # | # / # |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int2×int8 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,515 / 3.40 | 1,934 / 3.64 | 2,610 / 4.00 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,310 / 3.28 | 1,515 / 3.40 | 1,934 / 3.64 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×int8 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 2,272 / 5.11 | 2,901 / 5.47 | 3,916 / 6.00 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 1,964 / 4.92 | 2,272 / 5.11 | 2,901 / 5.47 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×int8 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 3,030 / 6.81 | 3,868 / 7.29 | 5,221 / 7.99 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 2,619 / 6.56 | 3,030 / 6.81 | 3,868 / 7.29 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×int8 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 4,544 / 10.21 | 5,801 / 10.93 | 7,831 / 11.99 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 3,929 / 9.84 | 4,544 / 10.21 | 5,801 / 10.93 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×int8 mul + v × fp16 add | 2,629 / 7.10 | 3,944 / 10.65 | 4,601 / 12.42 | 5,259 / 14.19 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 6,059 / 13.62 | 7,735 / 14.58 | 10,442 / 15.99 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 5,239 / 13.12 | 6,059 / 13.62 | 7,735 / 14.58 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,198 / # | 3,146 / # | 5,709 / # | 10,901 / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 872 / # | 1,855 / # | 3,146 / # | 5,709 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,198 / # | 3,146 / # | 5,709 / # | 10,901 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 872 / # | 1,855 / # | 3,146 / # | 5,709 / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 655* / 1.64* | 757 / 1.70 | 967 / 1.82 | 1,305 / 2.00 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 655* / 1.64* | 655 / 1.64 | 757 / 1.70 | 967 / 1.82 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 655* / 1.64* | 757 / 1.70 | 967 / 1.82 | 1,305 / 2.00 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 655* / 1.64* | 655 / 1.64 | 757 / 1.70 | 967 / 1.82 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,709 / # | # / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,146 / # | # / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,709 / # | # / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,146 / # | # / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 967 / 1.82 | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 757 / 1.70 | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 967 / 1.82 | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 757 / 1.70 | # / # | # / # | # / # |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int2×fp16 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 2,395 / # | 6,292 / # | 11,417 / # | 21,802 / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,745 / # | 3,710 / # | 6,292 / # | 11,417 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,515 / 3.40 | 1,934 / 3.64 | 2,610 / 4.00 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,310 / 3.28 | 1,515 / 3.40 | 1,934 / 3.64 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×fp16 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 3,593 / # | 9,438 / # | 17,126 / # | 32,703 / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 2,617 / # | 5,565 / # | 9,438 / # | 17,126 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 2,272 / 5.11 | 2,901 / 5.47 | 3,916 / 6.00 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 1,964 / 4.92 | 2,272 / 5.11 | 2,901 / 5.47 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×fp16 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 4,791 / # | 12,584 / # | 22,834 / # | 43,605 / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 3,489 / # | 7,419 / # | 12,584 / # | 22,834 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 3,030 / 6.81 | 3,868 / 7.29 | 5,221 / 7.99 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 2,619 / 6.56 | 3,030 / 6.81 | 3,868 / 7.29 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×fp16 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 7,186 / # | 18,876 / # | 34,251 / # | 65,407 / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 5,234 / # | 11,129 / # | 18,876 / # | 34,251 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 4,544 / 10.21 | 5,801 / 10.93 | 7,831 / 11.99 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 3,929 / 9.84 | 4,544 / 10.21 | 5,801 / 10.93 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×fp16 mul + v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 9,581 / # | 25,168 / # | 45,668 / # | 87,209 / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 6,978 / # | 14,839 / # | 25,168 / # | 45,668 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 6,059 / 13.62 | 7,735 / 14.58 | 10,442 / 15.99 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 5,239 / 13.12 | 6,059 / 13.62 | 7,735 / 14.58 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
