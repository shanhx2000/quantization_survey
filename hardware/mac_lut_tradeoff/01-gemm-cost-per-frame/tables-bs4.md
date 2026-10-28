# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 4

Generated 2026-10-28 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 4.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,413 / 24.72 | 12,619 / 37.08 | 14,722 / 43.26 | 16,826 / 49.44 |
| MAC opt | 4·v × fp16 add | 8,413 / 24.72 | 12,619 / 37.08 | 14,722 / 43.26 | 16,826 / 49.44 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.48 | 1,048 / 1.69 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,794 / 6.68 | 9,215 / 7.13 | 16,227 / 7.51 | 30,473 / 8.16 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,989 / 6.57 | 5,734 / 6.89 | 9,215 / 7.13 | 16,227 / 7.51 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,794 / 6.68 | 9,215 / 7.13 | 16,227 / 7.51 | 30,473 / 8.16 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,989 / 6.57 | 5,734 / 6.89 | 9,215 / 7.13 | 16,227 / 7.51 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,471* / 6.36* | 2,786 / 6.45 | 3,265 / 6.57 | 4,310 / 6.76 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,471* / 6.36* | 2,545 / 6.40 | 2,786 / 6.45 | 3,265 / 6.57 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,471* / 6.36* | 2,786 / 6.45 | 3,265 / 6.57 | 4,310 / 6.76 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,471* / 6.36* | 2,545 / 6.40 | 2,786 / 6.45 | 3,265 / 6.57 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,413 / 24.72 | 12,619 / 37.08 | 14,722 / 43.26 | 16,826 / 49.44 |
| MAC opt | 4·v × fp16 add | 8,413 / 24.72 | 12,619 / 37.08 | 14,722 / 43.26 | 16,826 / 49.44 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.48 | 1,048 / 1.69 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 14,966 / 7.47 | 115,475 / 12.09 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 8,584 / 7.10 | 58,772 / 9.50 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 14,966 / 7.47 | 115,475 / 12.09 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 8,584 / 7.10 | 58,772 / 9.50 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,104 / 6.52 | 10,570 / 8.29 | 38,853 / 12.72 | 79,342 / 17.86 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,682 / 6.41 | 6,570 / 7.34 | 20,222 / 9.72 | 38,853 / 12.72 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,104 / 6.52 | 10,570 / 8.29 | 38,853 / 12.72 | 79,342 / 17.86 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,682 / 6.41 | 6,570 / 7.34 | 20,222 / 9.72 | 38,853 / 12.72 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int2×int8 mul + 4·v × fp16 add | 8,949 / 26.21 | 13,424 / 39.32 | 15,661 / 45.87 | 17,898 / 52.43 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,587 / 13.36 | 18,431 / 14.26 | 32,453 / 15.02 | 60,947 / 16.32 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,977 / 13.15 | 11,467 / 13.77 | 18,431 / 14.26 | 32,453 / 15.02 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,941* / 12.72* | 5,573 / 12.90 | 6,530 / 13.14 | 8,619 / 13.52 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,941* / 12.72* | 5,089 / 12.79 | 5,573 / 12.90 | 6,530 / 13.14 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | 5,564* / 12.80* | 6,726 / 13.00 | 8,481 / 13.24 | 12,691 / 13.98 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 2R] + 8 × fp16 add | 5,564* / 12.80* | 5,873 / 12.90 | 6,726 / 13.00 | 8,481 / 13.24 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int3×int8 mul + 4·v × fp16 add | 9,173 / 26.47 | 13,759 / 39.70 | 16,052 / 46.32 | 18,346 / 52.94 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 11,381 / 20.03 | 27,646 / 21.40 | 48,680 / 22.52 | 91,420 / 24.48 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 8,966 / 19.72 | 17,201 / 20.66 | 27,646 / 21.40 | 48,680 / 22.52 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,412* / 19.08* | 8,359 / 19.36 | 9,795 / 19.71 | 12,929 / 20.28 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,412* / 19.08* | 7,634 / 19.19 | 8,359 / 19.36 | 9,795 / 19.71 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | 8,383* / 19.26* | 10,199 / 19.56 | 12,853 / 19.92 | 19,197 / 21.07 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 3R] + 12 × fp16 add | 8,383* / 19.26* | 8,867 / 19.42 | 10,199 / 19.56 | 12,853 / 19.92 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int4×int8 mul + 4·v × fp16 add | 9,441 / 26.62 | 14,161 / 39.93 | 16,522 / 46.58 | 18,882 / 53.23 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 15,175 / 26.71 | 36,862 / 28.53 | 64,906 / 30.03 | 121,894 / 32.64 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 11,954 / 26.29 | 22,934 / 27.55 | 36,862 / 28.53 | 64,906 / 30.03 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,883* / 25.44* | 11,146 / 25.81 | 13,061 / 26.28 | 17,238 / 27.04 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,883* / 25.44* | 10,178 / 25.58 | 11,146 / 25.81 | 13,061 / 26.28 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | 11,371* / 25.76* | 14,597 / 26.25 | 18,336 / 26.78 | 26,588 / 28.32 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 4R] + 16 × fp16 add | 11,371* / 25.76* | 12,664 / 26.04 | 14,597 / 26.25 | 18,336 / 26.78 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int6×int8 mul + 4·v × fp16 add | 10,114 / 27.96 | 15,171 / 41.93 | 17,700 / 48.92 | 20,229 / 55.91 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 22,762 / 40.07 | 55,292 / 42.79 | 97,359 / 45.05 | 182,841 / 48.96 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 17,932 / 39.44 | 34,401 / 41.32 | 55,292 / 42.79 | 97,359 / 45.05 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,824* / 38.17* | 16,719 / 38.71 | 19,591 / 39.42 | 25,857 / 40.56 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,824* / 38.17* | 15,267 / 38.37 | 16,719 / 38.71 | 19,591 / 39.42 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | 18,533* / 38.96* | 23,221 / 39.73 | 29,487 / 40.60 | 43,986 / 43.33 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 6R] + 24 × fp16 add | 18,533* / 38.96* | 19,972 / 39.39 | 23,221 / 39.73 | 29,487 / 40.60 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int8×int8 mul + 4·v × fp16 add | 10,715 / 28.90 | 16,073 / 43.36 | 18,751 / 50.58 | 21,430 / 57.81 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 30,350 / 53.42 | 73,723 / 57.06 | 129,812 / 60.06 | 243,788 / 65.28 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 23,909 / 52.58 | 45,868 / 55.09 | 73,723 / 57.06 | 129,812 / 60.06 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,766* / 50.89* | 22,292 / 51.61 | 26,121 / 52.56 | 34,476 / 54.08 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,766* / 50.89* | 20,356 / 51.17 | 22,292 / 51.61 | 26,121 / 52.56 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | 25,820* / 52.29* | 32,914 / 53.48 | 42,346 / 54.77 | 64,852 / 59.01 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·(8+⌈log2 v⌉)b, 8R] + 32 × fp16 add | 25,820* / 52.29* | 28,060 / 52.98 | 32,914 / 53.48 | 42,346 / 54.77 |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,413 / 24.72 | 12,619 / 37.08 | 14,722 / 43.26 | 16,826 / 49.44 |
| MAC opt | 4·v × fp16 add | 8,413 / 24.72 | 12,619 / 37.08 | 14,722 / 43.26 | 16,826 / 49.44 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.48 | 1,048 / 1.69 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 4,769 / 6.95 | 12,331 / 7.55 | 22,424 / 8.03 | 42,944 / 8.83 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 3,498 / 6.82 | 7,323 / 7.17 | 12,331 / 7.55 | 22,424 / 8.03 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 4,769 / 6.95 | 12,331 / 7.55 | 22,424 / 8.03 | 42,944 / 8.83 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 3,498 / 6.82 | 7,323 / 7.17 | 12,331 / 7.55 | 22,424 / 8.03 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 2,732* / 6.48* | 3,048 / 6.55 | 3,666 / 6.69 | 4,998 / 6.94 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 2,732* / 6.48* | 2,732 / 6.48 | 3,048 / 6.55 | 3,666 / 6.69 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 1R] + 4 × fp16 add | 2,732* / 6.48* | 3,048 / 6.55 | 3,666 / 6.69 | 4,998 / 6.94 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 1R] + 4 × fp16 add | 2,732* / 6.48* | 2,732 / 6.48 | 3,048 / 6.55 | 3,666 / 6.69 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 add | 8,413 / 24.72 | 12,619 / 37.08 | 14,722 / 43.26 | 16,826 / 49.44 |
| MAC opt | 4·v × fp16 add | 8,413 / 24.72 | 12,619 / 37.08 | 14,722 / 43.26 | 16,826 / 49.44 |
| MAC int8 | 4·v × int16 add | 524 / 0.85 | 786 / 1.27 | 917 / 1.48 | 1,048 / 1.69 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 22,424 / 8.03 | 166,220 / 13.78 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 12,331 / 7.55 | 83,839 / 10.61 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 22,424 / 8.03 | 166,220 / 13.78 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 12,331 / 7.55 | 83,839 / 10.61 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 3,666 / 6.69 | 13,482 / 9.00 | 50,799 / 14.70 | 104,290 / 21.21 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 3,048 / 6.55 | 7,925 / 7.71 | 23,350 / 11.16 | 50,799 / 14.70 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 4·16b, 1R] + 4 × fp16 add | 3,666 / 6.69 | 13,482 / 9.00 | 50,799 / 14.70 | 104,290 / 21.21 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 4·16b, 1R] + 4 × fp16 add | 3,048 / 6.55 | 7,925 / 7.71 | 23,350 / 11.16 | 50,799 / 14.70 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int2×fp16 mul + 4·v × fp16 add | 9,064 / 26.57 | 13,596 / 39.86 | 15,862 / 46.50 | 18,128 / 53.15 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 4·16b, 1R] + 8 × fp16 add | 9,538 / 13.89 | 24,662 / 15.10 | 44,849 / 16.06 | 85,889 / 17.67 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·16b, 1R] + 8 × fp16 add | 6,997 / 13.64 | 14,645 / 14.35 | 24,662 / 15.10 | 44,849 / 16.06 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 2R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 4·16b, 1R] + 8 × fp16 add | 5,464* / 12.95* | 6,095 / 13.09 | 7,331 / 13.39 | 9,996 / 13.88 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 4·16b, 1R] + 8 × fp16 add | 5,464* / 12.95* | 5,464 / 12.95 | 6,095 / 13.09 | 7,331 / 13.39 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 2R] + 8 × fp16 add | 7,010* / 13.16* | 8,186 / 13.30 | 10,514 / 13.64 | 15,096 / 14.19 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 2R] + 8 × fp16 add | 7,010* / 13.16* | 7,010 / 13.16 | 8,186 / 13.30 | 10,514 / 13.64 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int3×fp16 mul + 4·v × fp16 add | 11,443 / 34.04 | 17,164 / 51.06 | 20,025 / 59.57 | 22,886 / 68.08 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 4·16b, 1R] + 12 × fp16 add | 14,307 / 20.84 | 36,993 / 22.64 | 67,273 / 24.08 | 128,833 / 26.50 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·16b, 1R] + 12 × fp16 add | 10,495 / 20.46 | 21,968 / 21.52 | 36,993 / 22.64 | 67,273 / 24.08 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 3R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 4·16b, 1R] + 12 × fp16 add | 8,197* / 19.43* | 9,143 / 19.64 | 10,997 / 20.08 | 14,994 / 20.82 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 4·16b, 1R] + 12 × fp16 add | 8,197* / 19.43* | 8,197 / 19.43 | 9,143 / 19.64 | 10,997 / 20.08 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 3R] + 12 × fp16 add | 10,681* / 19.85* | 12,450 / 20.06 | 15,925 / 20.54 | 22,790 / 21.33 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 3R] + 12 × fp16 add | 10,681* / 19.85* | 10,681 / 19.85 | 12,450 / 20.06 | 15,925 / 20.54 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int4×fp16 mul + 4·v × fp16 add | 11,987 / 35.26 | 17,981 / 52.89 | 20,977 / 61.71 | 23,974 / 70.53 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 4·16b, 1R] + 16 × fp16 add | 19,076 / 27.78 | 49,324 / 30.19 | 89,697 / 32.11 | 171,777 / 35.33 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·16b, 1R] + 16 × fp16 add | 13,994 / 27.28 | 29,291 / 28.69 | 49,324 / 30.19 | 89,697 / 32.11 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 4R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 4·16b, 1R] + 16 × fp16 add | 10,929* / 25.90* | 12,191 / 26.18 | 14,662 / 26.77 | 19,992 / 27.76 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 4·16b, 1R] + 16 × fp16 add | 10,929* / 25.90* | 10,929 / 25.90 | 12,191 / 26.18 | 14,662 / 26.77 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 4R] + 16 × fp16 add | 14,685* / 26.64* | 17,170 / 26.92 | 22,002 / 27.58 | 31,588 / 28.64 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 4R] + 16 × fp16 add | 14,685* / 26.64* | 14,685 / 26.64 | 17,170 / 26.92 | 22,002 / 27.58 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int6×fp16 mul + 4·v × fp16 add | 13,465 / 40.12 | 20,197 / 60.18 | 23,564 / 70.21 | 26,930 / 80.24 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 4·16b, 1R] + 24 × fp16 add | 28,615 / 41.67 | 73,986 / 45.29 | 134,546 / 48.17 | 257,666 / 53.00 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·16b, 1R] + 24 × fp16 add | 20,990 / 40.92 | 43,936 / 43.04 | 73,986 / 45.29 | 134,546 / 48.17 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 6R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 4·16b, 1R] + 24 × fp16 add | 16,393* / 38.85* | 18,286 / 39.28 | 21,993 / 40.16 | 29,988 / 41.64 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 4·16b, 1R] + 24 × fp16 add | 16,393* / 38.85* | 16,393 / 38.85 | 18,286 / 39.28 | 21,993 / 40.16 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 6R] + 24 × fp16 add | 23,684* / 40.51* | 27,915 / 40.96 | 36,125 / 42.04 | 52,461 / 43.79 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 6R] + 24 × fp16 add | 23,684* / 40.51* | 23,684 / 40.51 | 27,915 / 40.96 | 36,125 / 42.04 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 4·v × fp16 mul + 4·v × fp16 add | 14,777 / 41.87 | 22,166 / 62.81 | 25,860 / 73.28 | 29,555 / 83.75 |
| MAC opt | 4·v × int8×fp16 mul + 4·v × fp16 add | 14,838 / 42.40 | 22,257 / 63.60 | 25,966 / 74.20 | 29,676 / 84.81 |
| MAC int8 | 4·v × int8 mul + 4·v × int16 add | 2,826 / 5.03 | 4,240 / 7.55 | 4,946 / 8.80 | 5,653 / 10.06 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 4·16b, 1R] + 32 × fp16 add | 38,153 / 55.56 | 98,648 / 60.38 | 179,395 / 64.22 | 343,555 / 70.67 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·16b, 1R] + 32 × fp16 add | 27,987 / 54.56 | 58,582 / 57.38 | 98,648 / 60.38 | 179,395 / 64.22 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 8R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 4·16b, 1R] + 32 × fp16 add | 21,858* / 51.81* | 24,382 / 52.37 | 29,324 / 53.54 | 39,984 / 55.53 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 4·16b, 1R] + 32 × fp16 add | 21,858* / 51.81* | 21,858 / 51.81 | 24,382 / 52.37 | 29,324 / 53.54 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 4·16b, 8R] + 32 × fp16 add | 33,980* / 54.76* | 40,374 / 55.42 | 52,855 / 57.04 | 77,967 / 59.65 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 4·16b, 8R] + 32 × fp16 add | 33,980* / 54.76* | 33,980 / 54.76 | 40,374 / 55.42 | 52,855 / 57.04 |
