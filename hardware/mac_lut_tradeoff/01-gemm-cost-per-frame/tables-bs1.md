# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 1

Generated 2026-10-23 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 1.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 962 / # | 2,381 / # | 4,206 / # | 7,896 / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 749 / # | 1,466 / # | 2,381 / # | 4,206 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 962 / # | 2,381 / # | 4,206 / # | 7,896 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 749 / # | 1,466 / # | 2,381 / # | 4,206 / # |
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
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 3,906 / # | 30,046 / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 2,228 / # | 15,269 / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 3,906 / # | 30,046 / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 2,228 / # | 15,269 / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 967 / 1.82 | 3,295 / 2.96 | 14,620 / 6.79 | 24,359 / 10.97 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 757 / 1.70 | 2,082 / 2.34 | 6,110 / 4.67 | 14,620 / 6.79 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 967 / 1.82 | 3,295 / 2.96 | 14,620 / 6.79 | 24,359 / 10.97 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 757 / 1.70 | 2,082 / 2.34 | 6,110 / 4.67 | 14,620 / 6.79 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int2×int8 mul + v × fp16 add | 2,194 / 6.49 | 3,292 / 9.74 | 3,840 / 11.36 | 4,389 / 12.99 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,923 / # | 4,762 / # | 8,411 / # | 15,791 / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,498 / # | 2,932 / # | 4,762 / # | 8,411 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,582 / # | 3,264 / # | 5,423 / # | 9,800 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,326 / # | 2,185 / # | 3,264 / # | 5,423 / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,515 / 3.40 | 1,934 / 3.64 | 2,610 / 4.00 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,310 / 3.28 | 1,515 / 3.40 | 1,934 / 3.64 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,529* / 3.29* | 1,926 / 3.37 | 2,566 / 3.57 | 3,859 / 3.91 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,529* / 3.29* | 1,529 / 3.29 | 1,926 / 3.37 | 2,566 / 3.57 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×int8 mul + v × fp16 add | 2,250 / 6.56 | 3,376 / 9.83 | 3,938 / 11.47 | 4,501 / 13.11 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 2,885 / # | 7,143 / # | 12,617 / # | 23,687 / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 2,247 / # | 4,397 / # | 7,143 / # | 12,617 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,198 / # | 4,146 / # | 6,639 / # | 11,704 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 1,903 / # | 2,899 / # | 4,146 / # | 6,639 / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 2,272 / 5.11 | 2,901 / 5.47 | 3,916 / 6.00 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 1,964 / 4.92 | 2,272 / 5.11 | 2,901 / 5.47 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,303* / 4.93* | 2,919 / 5.03 | 3,882 / 5.32 | 5,835 / 5.76 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,303* / 4.93* | 2,303 / 4.93 | 2,919 / 5.03 | 3,882 / 5.32 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×int8 mul + v × fp16 add | 2,317 / 6.59 | 3,476 / 9.89 | 4,055 / 11.54 | 4,635 / 13.19 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,847 / # | 9,524 / # | 16,822 / # | 31,582 / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,996 / # | 5,863 / # | 9,524 / # | 16,822 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 2,816 / # | 5,031 / # | 7,857 / # | 13,609 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 2,480 / # | 3,614 / # | 5,031 / # | 7,857 / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 3,030 / 6.81 | 3,868 / 7.29 | 5,221 / 7.99 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 2,619 / 6.56 | 3,030 / 6.81 | 3,868 / 7.29 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 3,128* / 6.57* | 4,015 / 6.70 | 5,372 / 7.08 | 8,111 / 7.65 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 3,128* / 6.57* | 3,128 / 6.57 | 4,015 / 6.70 | 5,372 / 7.08 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×int8 mul + v × fp16 add | 2,486 / 6.93 | 3,729 / 10.39 | 4,350 / 12.12 | 4,971 / 13.86 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 5,770 / # | 14,286 / # | 25,233 / # | 47,373 / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 4,494 / # | 8,795 / # | 14,286 / # | 25,233 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 4,051 / # | 6,792 / # | 10,292 / # | 17,422 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 3,634 / # | 5,042 / # | 6,792 / # | 10,292 / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 4,544 / 10.21 | 5,801 / 10.93 | 7,831 / 11.99 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 3,929 / 9.84 | 4,544 / 10.21 | 5,801 / 10.93 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 4,947* / 9.91* | 6,481 / 10.09 | 8,807 / 10.71 | 14,733 / 12.10 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 4,947* / 9.91* | 4,947 / 9.91 | 6,481 / 10.09 | 8,807 / 10.71 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×int8 mul + v × fp16 add | 2,629 / 7.10 | 3,944 / 10.65 | 4,601 / 12.42 | 5,259 / 14.19 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,693 / # | 19,048 / # | 33,644 / # | 63,164 / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,993 / # | 11,726 / # | 19,048 / # | 33,644 / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 5,277 / # | 8,557 / # | 12,724 / # | 21,246 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 4,787 / # | 6,462 / # | 8,557 / # | 12,724 / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 6,059 / 13.62 | 7,735 / 14.58 | 10,442 / 15.99 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 5,239 / 13.12 | 6,059 / 13.62 | 7,735 / 14.58 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 6,966* / 13.30* | 9,292 / 13.53 | 13,211 / 14.61 | 21,816 / 16.43 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 6,966* / 13.30* | 6,966 / 13.30 | 9,292 / 13.53 | 13,211 / 14.61 |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,197 / 1.73 | 3,137 / # | 5,707 / 2.09 | 10,894 / # |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 872 / # | 1,848 / # | 3,137 / # | 5,707 / 2.09 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,197 / 1.73 | 3,137 / # | 5,707 / 2.09 | 10,894 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 872 / # | 1,848 / # | 3,137 / # | 5,707 / 2.09 |
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
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,707 / 2.09 | 41,991 / # | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,137 / # | 21,247 / # | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,707 / 2.09 | 41,991 / # | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,137 / # | 21,247 / # | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 967 / 1.82 | 3,295 / 2.96 | 14,620 / 6.79 | 24,359 / 10.97 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 757 / 1.70 | 2,082 / 2.34 | 6,110 / 4.67 | 14,620 / 6.79 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 967 / 1.82 | 3,295 / 2.96 | 14,620 / 6.79 | 24,359 / 10.97 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 757 / 1.70 | 2,082 / 2.34 | 6,110 / 4.67 | 14,620 / 6.79 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int2×fp16 mul + v × fp16 add | 2,223 / 6.58 | 3,335 / 9.87 | 3,891 / 11.52 | 4,446 / 13.17 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 2,393 / 3.46 | 6,275 / # | 11,413 / 4.18 | 21,787 / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,745 / # | 3,696 / # | 6,275 / # | 11,413 / 4.18 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | 1,873 / # | 4,169 / # | 7,212 / # | 13,372 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | 1,482 / # | 2,647 / # | 4,169 / # | 7,212 / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,515 / 3.40 | 1,934 / 3.64 | 2,610 / 4.00 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,310 / 3.28 | 1,515 / 3.40 | 1,934 / 3.64 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | 1,529* / 3.29* | 1,926 / 3.37 | 2,566 / 3.57 | 3,859 / 3.91 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | 1,529* / 3.29* | 1,529 / 3.29 | 1,926 / 3.37 | 2,566 / 3.57 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×fp16 mul + v × fp16 add | 2,818 / 8.45 | 4,227 / 12.67 | 4,931 / 14.79 | 5,636 / 16.90 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 3,590 / 5.19 | 9,412 / # | 17,120 / 6.27 | 32,681 / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 2,617 / # | 5,545 / # | 9,412 / # | 17,120 / 6.27 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | 2,545 / # | 5,201 / # | 8,719 / # | 15,852 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | 2,091 / # | 3,441 / # | 5,201 / # | 8,719 / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 2,272 / 5.11 | 2,901 / 5.47 | 3,916 / 6.00 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 1,964 / 4.92 | 2,272 / 5.11 | 2,901 / 5.47 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | 2,303* / 4.93* | 2,919 / 5.03 | 3,882 / 5.32 | 5,835 / 5.76 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | 2,303* / 4.93* | 2,303 / 4.93 | 2,919 / 5.03 | 3,882 / 5.32 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×fp16 mul + v × fp16 add | 2,954 / 8.76 | 4,431 / 13.13 | 5,169 / 15.32 | 5,908 / 17.51 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 4,787 / 6.92 | 12,549 / # | 22,827 / 8.35 | 43,575 / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 3,489 / # | 7,393 / # | 12,549 / # | 22,827 / 8.35 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | 3,218 / # | 6,232 / # | 10,226 / # | 18,337 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | 2,701 / # | 4,234 / # | 6,232 / # | 10,226 / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 3,030 / 6.81 | 3,868 / 7.29 | 5,221 / 7.99 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 2,619 / 6.56 | 3,030 / 6.81 | 3,868 / 7.29 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | 3,128* / 6.57* | 4,015 / 6.70 | 5,372 / 7.08 | 8,111 / 7.65 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | 3,128* / 6.57* | 3,128 / 6.57 | 4,015 / 6.70 | 5,372 / 7.08 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×fp16 mul + v × fp16 add | 3,323 / 9.97 | 4,985 / 14.95 | 5,816 / 17.45 | 6,647 / 19.94 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 7,180 / 10.39 | 18,824 / # | 34,240 / 12.53 | 65,362 / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 5,234 / # | 11,089 / # | 18,824 / # | 34,240 / 12.53 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | 4,563 / # | 8,295 / # | 13,241 / # | 23,300 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | 3,919 / # | 5,821 / # | 8,295 / # | 13,241 / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 4,544 / 10.21 | 5,801 / 10.93 | 7,831 / 11.99 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 3,929 / 9.84 | 4,544 / 10.21 | 5,801 / 10.93 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | 4,947* / 9.91* | 6,481 / 10.09 | 8,807 / 10.71 | 14,733 / 12.10 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | 4,947* / 9.91* | 4,947 / 9.91 | 6,481 / 10.09 | 8,807 / 10.71 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×fp16 mul + v × fp16 add | 3,667 / 10.54 | 5,500 / 15.81 | 6,417 / 18.45 | 7,333 / 21.08 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 9,574 / 13.85 | 25,098 / # | 45,653 / 16.71 | 87,150 / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 6,978 / # | 14,785 / # | 25,098 / # | 45,653 / 16.71 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | 5,908 / # | 10,358 / # | 16,255 / # | 28,259 / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | 5,138 / # | 7,408 / # | 10,358 / # | 16,255 / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 6,059 / 13.62 | 7,735 / 14.58 | 10,442 / 15.99 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 5,239 / 13.12 | 6,059 / 13.62 | 7,735 / 14.58 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | 6,966* / 13.30* | 9,292 / 13.53 | 13,211 / 14.61 | 21,816 / 16.43 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | 6,966* / 13.30* | 6,966 / 13.30 | 9,292 / 13.53 | 13,211 / 14.61 |
