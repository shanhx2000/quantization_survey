# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 2

Generated 2026-10-22 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz; `#` = no data
yet. LUT entries are 16 bits for wa = int8, 32 bits for wa = fp16.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 1,713 / # | 3,661 / # | 6,224 / # | 11,416 / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,387 / # | 2,370 / # | 3,661 / # | 6,224 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 1,713 / # | 3,661 / # | 6,224 / # | 11,416 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,387 / # | 2,370 / # | 3,661 / # | 6,224 / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 2 × fp16 add | # / # | 1,273 / 3.23 | 1,482 / 3.35 | 1,820 / 3.53 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | # / # | 1,170 / 3.17 | 1,273 / 3.23 | 1,482 / 3.35 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 2 × fp16 add | # / # | 1,273 / 3.23 | 1,482 / 3.35 | 1,820 / 3.53 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | # / # | 1,170 / 3.17 | 1,273 / 3.23 | 1,482 / 3.35 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 2 × fp16 add | 6,224 / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 2 × fp16 add | 3,661 / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 2 × fp16 add | 6,224 / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 2 × fp16 add | 3,661 / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 2 × fp16 add | 1,482 / 3.35 | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 2 × fp16 add | 1,273 / 3.23 | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 2 × fp16 add | 1,482 / 3.35 | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 2 × fp16 add | 1,273 / 3.23 | # / # | # / # | # / # |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int2×int8 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 3,425 / # | 7,322 / # | 12,447 / # | 22,832 / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 2,775 / # | 4,740 / # | 7,322 / # | 12,447 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 4 × fp16 add | # / # | 2,545 / 6.46 | 2,964 / 6.70 | 3,641 / 7.06 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | # / # | 2,340 / 6.34 | 2,545 / 6.46 | 2,964 / 6.70 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int3×int8 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 5,138 / # | 10,983 / # | 18,671 / # | 34,249 / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 4,162 / # | 7,110 / # | 10,983 / # | 18,671 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 6 × fp16 add | # / # | 3,818 / 9.70 | 4,446 / 10.06 | 5,461 / 10.58 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | # / # | 3,510 / 9.51 | 3,818 / 9.70 | 4,446 / 10.06 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int4×int8 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 6,851 / # | 14,644 / # | 24,895 / # | 45,665 / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 5,550 / # | 9,480 / # | 14,644 / # | 24,895 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 8 × fp16 add | # / # | 5,090 / 12.93 | 5,928 / 13.41 | 7,281 / 14.11 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | # / # | 4,680 / 12.68 | 5,090 / 12.93 | 5,928 / 13.41 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int6×int8 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 12 × fp16 add | 10,276 / # | 21,966 / # | 37,342 / # | 68,497 / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 12 × fp16 add | 8,324 / # | 14,220 / # | 21,966 / # | 37,342 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 12 × fp16 add | # / # | 7,635 / 19.39 | 8,892 / 20.11 | 10,922 / 21.17 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 12 × fp16 add | # / # | 7,019 / 19.02 | 7,635 / 19.39 | 8,892 / 20.11 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int8×int8 mul + 2·v × fp16 add | 5,259 / 14.19 | 7,888 / 21.29 | 9,203 / 24.84 | 10,517 / 28.39 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 16 × fp16 add | 13,702 / # | 29,288 / # | 49,789 / # | 91,330 / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 16 × fp16 add | 11,099 / # | 18,959 / # | 29,288 / # | 49,789 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 16 × fp16 add | # / # | 10,180 / 25.86 | 11,856 / 26.82 | 14,562 / 28.23 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 16 × fp16 add | # / # | 9,359 / 25.36 | 10,180 / 25.86 | 11,856 / 26.82 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC opt | 2·v × fp16 add | 4,121 / 12.24 | 6,181 / 18.36 | 7,211 / 21.42 | 8,241 / 24.48 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 32b, 1R] + 2 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int2×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 32b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 32b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 32b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 32b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 32b, 1R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 32b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int3×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 32b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 32b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 32b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 32b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 32b, 1R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 32b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int4×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 32b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 32b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 32b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 32b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 32b, 1R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 32b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int6×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 32b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 32b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 32b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 32b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 32b, 1R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 32b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,190 / 20.75 | 10,785 / 31.13 | 12,583 / 36.31 | 14,380 / 41.50 |
| MAC opt | 2·v × int8×fp16 mul + 2·v × fp16 add | # / # | # / # | # / # | # / # |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,400 / 2.38 | 2,100 / 3.57 | 2,450 / 4.17 | 2,800 / 4.76 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 32b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 32b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 32b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 32b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 32b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 32b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 32b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
