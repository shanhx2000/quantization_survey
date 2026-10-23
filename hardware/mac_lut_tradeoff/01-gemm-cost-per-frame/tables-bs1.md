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
| LUT reg dup, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 962 / 1.67 | 2,381 / 1.85 | 4,206 / 2.01 | 7,896 / 2.26 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 749 / 1.63 | 1,466 / 1.74 | 2,381 / 1.85 | 4,206 / 2.01 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 962 / 1.67 | 2,381 / 1.85 | 4,206 / 2.01 | 7,896 / 2.26 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 749 / 1.63 | 1,466 / 1.74 | 2,381 / 1.85 | 4,206 / 2.01 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 655* / 1.60* | 757 / 1.63 | 967 / 1.69 | 1,305 / 1.78 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 655* / 1.60* | 655 / 1.60 | 757 / 1.63 | 967 / 1.69 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 655* / 1.60* | 757 / 1.63 | 967 / 1.69 | 1,305 / 1.78 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 655* / 1.60* | 655 / 1.60 | 757 / 1.63 | 967 / 1.69 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 3,906 / 1.99 | 30,046 / 3.98 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 2,228 / 1.83 | 15,269 / 2.89 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 3,906 / 1.99 | 30,046 / 3.98 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 2,228 / 1.83 | 15,269 / 2.89 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 967 / 1.69 | 3,295 / 2.19 | 14,620 / 3.50 | 24,359 / 5.02 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 757 / 1.63 | 2,082 / 1.91 | 6,110 / 2.90 | 14,620 / 3.50 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 967 / 1.69 | 3,295 / 2.19 | 14,620 / 3.50 | 24,359 / 5.02 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 757 / 1.63 | 2,082 / 1.91 | 6,110 / 2.90 | 14,620 / 3.50 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int2×int8 mul + v × fp16 add | 2,194 / 6.49 | 3,292 / 9.74 | 3,840 / 11.36 | 4,389 / 12.99 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,923 / 3.35 | 4,762 / 3.71 | 8,411 / 4.02 | 15,791 / 4.52 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,498 / 3.27 | 2,932 / 3.48 | 4,762 / 3.71 | 8,411 / 4.02 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,582 / 3.31 | 3,264 / 3.54 | 5,423 / 3.74 | 9,800 / 4.04 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,326 / 3.24 | 2,185 / 3.41 | 3,264 / 3.54 | 5,423 / 3.74 |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,310* / 3.21* | 1,515 / 3.26 | 1,934 / 3.38 | 2,610 / 3.56 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,310* / 3.21* | 1,310 / 3.21 | 1,515 / 3.26 | 1,934 / 3.38 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,529* / 3.23* | 1,926 / 3.27 | 2,566 / 3.40 | 3,859 / 3.59 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,529* / 3.23* | 1,529 / 3.23 | 1,926 / 3.27 | 2,566 / 3.40 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×int8 mul + v × fp16 add | 2,250 / 6.56 | 3,376 / 9.83 | 3,938 / 11.47 | 4,501 / 13.11 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 2,885 / 5.02 | 7,143 / 5.56 | 12,617 / 6.03 | 23,687 / 6.78 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 2,247 / 4.90 | 4,397 / 5.23 | 7,143 / 5.56 | 12,617 / 6.03 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,198 / 4.95 | 4,146 / 5.27 | 6,639 / 5.53 | 11,704 / 5.90 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 1,903 / 4.86 | 2,899 / 5.10 | 4,146 / 5.27 | 6,639 / 5.53 |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,964* / 4.81* | 2,272 / 4.89 | 2,901 / 5.07 | 3,916 / 5.33 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,964* / 4.81* | 1,964 / 4.81 | 2,272 / 4.89 | 2,901 / 5.07 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,303* / 4.86* | 2,919 / 4.91 | 3,882 / 5.12 | 5,835 / 5.39 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,303* / 4.86* | 2,303 / 4.86 | 2,919 / 4.91 | 3,882 / 5.12 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×int8 mul + v × fp16 add | 2,317 / 6.59 | 3,476 / 9.89 | 4,055 / 11.54 | 4,635 / 13.19 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,847 / 6.70 | 9,524 / 7.41 | 16,822 / 8.03 | 31,582 / 9.04 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,996 / 6.53 | 5,863 / 6.97 | 9,524 / 7.41 | 16,822 / 8.03 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 2,816 / 6.60 | 5,031 / 7.00 | 7,857 / 7.31 | 13,609 / 7.76 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 2,480 / 6.47 | 3,614 / 6.78 | 5,031 / 7.00 | 7,857 / 7.31 |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,619* / 6.42* | 3,030 / 6.53 | 3,868 / 6.76 | 5,221 / 7.11 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,619* / 6.42* | 2,619 / 6.42 | 3,030 / 6.53 | 3,868 / 6.76 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 3,128* / 6.50* | 4,015 / 6.57 | 5,372 / 6.86 | 8,111 / 7.23 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 3,128* / 6.50* | 3,128 / 6.50 | 4,015 / 6.57 | 5,372 / 6.86 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×int8 mul + v × fp16 add | 2,486 / 6.93 | 3,729 / 10.39 | 4,350 / 12.12 | 4,971 / 13.86 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 5,770 / 10.04 | 14,286 / 11.12 | 25,233 / 12.05 | 47,373 / 13.56 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 4,494 / 9.80 | 8,795 / 10.45 | 14,286 / 11.12 | 25,233 / 12.05 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 4,051 / 9.89 | 6,792 / 10.46 | 10,292 / 10.89 | 17,422 / 11.47 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 3,634 / 9.71 | 5,042 / 10.16 | 6,792 / 10.46 | 10,292 / 10.89 |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,929* / 9.63* | 4,544 / 9.79 | 5,801 / 10.15 | 7,831 / 10.67 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,929* / 9.63* | 3,929 / 9.63 | 4,544 / 9.79 | 5,801 / 10.15 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 4,947* / 9.82* | 6,481 / 9.93 | 8,807 / 10.43 | 14,733 / 11.50 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 4,947* / 9.82* | 4,947 / 9.82 | 6,481 / 9.93 | 8,807 / 10.43 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×int8 mul + v × fp16 add | 2,629 / 7.10 | 3,944 / 10.65 | 4,601 / 12.42 | 5,259 / 14.19 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,693 / 13.39 | 19,048 / 14.83 | 33,644 / 16.07 | 63,164 / 18.08 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,993 / 13.06 | 11,726 / 13.93 | 19,048 / 14.83 | 33,644 / 16.07 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 5,277 / 13.18 | 8,557 / 13.93 | 12,724 / 14.47 | 21,246 / 15.19 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 4,787 / 12.94 | 6,462 / 13.52 | 8,557 / 13.93 | 12,724 / 14.47 |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,239* / 12.84* | 6,059 / 13.05 | 7,735 / 13.53 | 10,442 / 14.22 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,239* / 12.84* | 5,239 / 12.84 | 6,059 / 13.05 | 7,735 / 13.53 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 6,966* / 13.19* | 9,292 / 13.35 | 13,211 / 14.21 | 21,816 / 15.71 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 6,966* / 13.19* | 6,966 / 13.19 | 9,292 / 13.35 | 13,211 / 14.21 |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,197 / 1.73 | 3,137 / 1.93 | 5,707 / 2.09 | 10,894 / 2.35 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 872 / 1.68 | 1,848 / 1.80 | 3,137 / 1.93 | 5,707 / 2.09 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,197 / 1.73 | 3,137 / 1.93 | 5,707 / 2.09 | 10,894 / 2.35 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 872 / 1.68 | 1,848 / 1.80 | 3,137 / 1.93 | 5,707 / 2.09 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 655* / 1.60* | 757 / 1.63 | 967 / 1.69 | 1,305 / 1.78 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 655* / 1.60* | 655 / 1.60 | 757 / 1.63 | 967 / 1.69 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 655* / 1.60* | 757 / 1.63 | 967 / 1.69 | 1,305 / 1.78 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 655* / 1.60* | 655 / 1.60 | 757 / 1.63 | 967 / 1.69 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,707 / 2.09 | 41,991 / 4.07 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,137 / 1.93 | 21,247 / 2.97 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,707 / 2.09 | 41,991 / 4.07 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,137 / 1.93 | 21,247 / 2.97 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 967 / 1.69 | 3,295 / 2.19 | 14,620 / 3.50 | 24,359 / 5.02 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 757 / 1.63 | 2,082 / 1.91 | 6,110 / 2.90 | 14,620 / 3.50 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 967 / 1.69 | 3,295 / 2.19 | 14,620 / 3.50 | 24,359 / 5.02 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 757 / 1.63 | 2,082 / 1.91 | 6,110 / 2.90 | 14,620 / 3.50 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int2×fp16 mul + v × fp16 add | 2,223 / 6.58 | 3,335 / 9.87 | 3,891 / 11.52 | 4,446 / 13.17 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 2,393 / 3.46 | 6,275 / 3.85 | 11,413 / 4.18 | 21,787 / 4.71 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,745 / 3.36 | 3,696 / 3.59 | 6,275 / 3.85 | 11,413 / 4.18 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | 1,873 / 3.43 | 4,169 / 3.68 | 7,212 / 3.90 | 13,372 / 4.23 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | 1,482 / 3.36 | 2,647 / 3.52 | 4,169 / 3.68 | 7,212 / 3.90 |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 1,310* / 3.21* | 1,515 / 3.26 | 1,934 / 3.38 | 2,610 / 3.56 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,310* / 3.21* | 1,310 / 3.21 | 1,515 / 3.26 | 1,934 / 3.38 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | 1,529* / 3.23* | 1,926 / 3.27 | 2,566 / 3.40 | 3,859 / 3.59 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | 1,529* / 3.23* | 1,529 / 3.23 | 1,926 / 3.27 | 2,566 / 3.40 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×fp16 mul + v × fp16 add | 2,818 / 8.45 | 4,227 / 12.67 | 4,931 / 14.79 | 5,636 / 16.90 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 3,590 / 5.19 | 9,412 / 5.78 | 17,120 / 6.27 | 32,681 / 7.06 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 2,617 / 5.05 | 5,545 / 5.39 | 9,412 / 5.78 | 17,120 / 6.27 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | 2,545 / 5.13 | 5,201 / 5.47 | 8,719 / 5.77 | 15,852 / 6.18 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | 2,091 / 5.03 | 3,441 / 5.26 | 5,201 / 5.47 | 8,719 / 5.77 |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 1,964* / 4.81* | 2,272 / 4.89 | 2,901 / 5.07 | 3,916 / 5.33 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 1,964* / 4.81* | 1,964 / 4.81 | 2,272 / 4.89 | 2,901 / 5.07 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | 2,303* / 4.86* | 2,919 / 4.91 | 3,882 / 5.12 | 5,835 / 5.39 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | 2,303* / 4.86* | 2,303 / 4.86 | 2,919 / 4.91 | 3,882 / 5.12 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×fp16 mul + v × fp16 add | 2,954 / 8.76 | 4,431 / 13.13 | 5,169 / 15.32 | 5,908 / 17.51 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 4,787 / 6.92 | 12,549 / 7.71 | 22,827 / 8.35 | 43,575 / 9.42 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 3,489 / 6.73 | 7,393 / 7.19 | 12,549 / 7.71 | 22,827 / 8.35 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | 3,218 / 6.83 | 6,232 / 7.27 | 10,226 / 7.63 | 18,337 / 8.13 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | 2,701 / 6.70 | 4,234 / 7.00 | 6,232 / 7.27 | 10,226 / 7.63 |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 2,619* / 6.42* | 3,030 / 6.53 | 3,868 / 6.76 | 5,221 / 7.11 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 2,619* / 6.42* | 2,619 / 6.42 | 3,030 / 6.53 | 3,868 / 6.76 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | 3,128* / 6.50* | 4,015 / 6.57 | 5,372 / 6.86 | 8,111 / 7.23 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | 3,128* / 6.50* | 3,128 / 6.50 | 4,015 / 6.57 | 5,372 / 6.86 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×fp16 mul + v × fp16 add | 3,323 / 9.97 | 4,985 / 14.95 | 5,816 / 17.45 | 6,647 / 19.94 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 7,180 / 10.39 | 18,824 / 11.56 | 34,240 / 12.53 | 65,362 / 14.12 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 5,234 / 10.09 | 11,089 / 10.78 | 18,824 / 11.56 | 34,240 / 12.53 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | 4,563 / 10.24 | 8,295 / 10.86 | 13,241 / 11.37 | 23,300 / 12.02 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | 3,919 / 10.05 | 5,821 / 10.47 | 8,295 / 10.86 | 13,241 / 11.37 |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 3,929* / 9.63* | 4,544 / 9.79 | 5,801 / 10.15 | 7,831 / 10.67 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 3,929* / 9.63* | 3,929 / 9.63 | 4,544 / 9.79 | 5,801 / 10.15 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | 4,947* / 9.82* | 6,481 / 9.93 | 8,807 / 10.43 | 14,733 / 11.50 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | 4,947* / 9.82* | 4,947 / 9.82 | 6,481 / 9.93 | 8,807 / 10.43 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×fp16 mul + v × fp16 add | 3,667 / 10.54 | 5,500 / 15.81 | 6,417 / 18.45 | 7,333 / 21.08 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 9,574 / 13.85 | 25,098 / 15.42 | 45,653 / 16.71 | 87,150 / 18.83 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 6,978 / 13.45 | 14,785 / 14.38 | 25,098 / 15.42 | 45,653 / 16.71 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | 5,908 / 13.64 | 10,358 / 14.46 | 16,255 / 15.11 | 28,259 / 15.92 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | 5,138 / 13.39 | 7,408 / 13.95 | 10,358 / 14.46 | 16,255 / 15.11 |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 5,239* / 12.84* | 6,059 / 13.05 | 7,735 / 13.53 | 10,442 / 14.22 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 5,239* / 12.84* | 5,239 / 12.84 | 6,059 / 13.05 | 7,735 / 13.53 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | 6,966* / 13.19* | 9,292 / 13.35 | 13,211 / 14.21 | 21,816 / 15.71 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | 6,966* / 13.19* | 6,966 / 13.19 | 9,292 / 13.35 | 13,211 / 14.21 |
