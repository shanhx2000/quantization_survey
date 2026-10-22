# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 1

Generated 2026-10-22 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports; or register-file power from a 5 ns clock-transition run whose 0.1 ns rerun is not done yet. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 1.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC opt | v × fp16 add | 2,060 / 6.12 | 3,091 / 9.18 | 3,606 / 10.71 | 4,121 / 12.24 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 962 / 1.84* | 2,391 / 2.26* | 4,209 / 2.69* | 7,903 / 4.35* |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 749 / 1.78* | 1,473 / 2.03* | 2,391 / 2.26* | 4,209 / 2.69* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 962 / 1.84* | 2,391 / 2.26* | 4,209 / 2.69* | 7,903 / 4.35* |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 749 / 1.78* | 1,473 / 2.03* | 2,391 / 2.26* | 4,209 / 2.69* |
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
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 3,909 / 2.61* | 30,024 / 11.98* | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 2,240 / 2.21* | 15,297 / 6.96* | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 3,909 / 2.61* | 30,024 / 11.98* | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 2,240 / 2.21* | 15,297 / 6.96* | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 967 / 1.82 | 3,295 / 2.96 | 14,620 / 6.79 | 24,359 / 10.97 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 757 / 1.70 | 2,082 / 2.34 | 6,110 / 4.67 | 14,620 / 6.79 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 967 / 1.82 | 3,295 / 2.96 | 14,620 / 6.79 | 24,359 / 10.97 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 757 / 1.70 | 2,082 / 2.34 | 6,110 / 4.67 | 14,620 / 6.79 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int2×int8 mul + v × fp16 add | 2,194 / 6.49 | 3,292 / 9.74 | 3,840 / 11.36 | 4,389 / 12.98 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,924 / 3.69* | 4,781 / 4.52* | 8,419 / 5.39* | 15,806 / 8.70* |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,498 / 3.55* | 2,946 / 4.06* | 4,781 / 4.52* | 8,419 / 5.39* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,581 / 3.60* | 3,279 / 4.11* | 5,427 / 4.59* | 9,822 / 6.31* |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,327 / 3.51* | 2,193 / 3.85* | 3,279 / 4.11* | 5,427 / 4.59* |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,515 / 3.40 | 1,934 / 3.64 | 2,610 / 4.00 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,310 / 3.28 | 1,515 / 3.40 | 1,934 / 3.64 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,529* / 3.29* | 1,926 / 3.37 | 2,566 / 3.57 | 3,859 / 3.91 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,529* / 3.29* | 1,529 / 3.29 | 1,926 / 3.37 | 2,566 / 3.57 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×int8 mul + v × fp16 add | 2,249 / 6.55 | 3,374 / 9.83 | 3,936 / 11.47 | 4,499 / 13.10 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 2,886 / 5.53* | 7,172 / 6.78* | 12,628 / 8.08* | 23,709 / 13.04* |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 2,247 / 5.33* | 4,419 / 6.10* | 7,172 / 6.78* | 12,628 / 8.08* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,199 / 5.36* | 4,168 / 5.96* | 6,649 / 6.49* | 11,704 / 7.96 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 1,904 / 5.24* | 2,910 / 5.66* | 4,168 / 5.96* | 6,649 / 6.49* |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 2,272 / 5.11 | 2,901 / 5.47 | 3,916 / 6.00 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 1,964 / 4.92 | 2,272 / 5.11 | 2,901 / 5.47 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,303* / 4.93* | 2,919 / 5.03 | 3,882 / 5.32 | 5,835 / 5.76 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,303* / 4.93* | 2,303 / 4.93 | 2,919 / 5.03 | 3,882 / 5.32 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×int8 mul + v × fp16 add | 2,317 / 6.59 | 3,475 / 9.89 | 4,055 / 11.53 | 4,634 / 13.18 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,849 / 7.38* | 9,563 / 9.04* | 16,837 / 10.78* | 31,612 / 17.39* |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,996 / 7.10* | 5,892 / 8.13* | 9,563 / 9.04* | 16,837 / 10.78* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 2,816 / 6.66 | 5,031 / 7.33 | 7,857 / 7.95 | 13,609 / 9.82 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 2,480 / 6.50 | 3,614 / 6.97 | 5,031 / 7.33 | 7,857 / 7.95 |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 3,030 / 6.81 | 3,868 / 7.29 | 5,221 / 7.99 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 2,619 / 6.56 | 3,030 / 6.81 | 3,868 / 7.29 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 3,128* / 6.57* | 4,015 / 6.70 | 5,372 / 7.08 | 8,111 / 7.65 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 3,128* / 6.57* | 3,128 / 6.57 | 4,015 / 6.70 | 5,372 / 7.08 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×int8 mul + v × fp16 add | 2,477 / 6.85 | 3,716 / 10.28 | 4,335 / 11.99 | 4,954 / 13.71 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 5,773 / 11.07* | 14,344 / 13.56* | 25,256 / 16.16* | 47,418 / 26.09* |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 4,494 / 10.65* | 8,838 / 12.19* | 14,344 / 13.56* | 25,256 / 16.16* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 4,051 / 9.95 | 6,792 / 10.79 | 10,292 / 11.52 | 17,422 / 13.53 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 3,634 / 9.73 | 5,042 / 10.34 | 6,792 / 10.79 | 10,292 / 11.52 |
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
| LUT reg dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,697 / 14.76* | 19,126 / 18.08* | 33,674 / 21.55* | 63,224 / 34.78* |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,992 / 14.20* | 11,784 / 16.25* | 19,126 / 18.08* | 33,674 / 21.55* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 5,277 / 13.23 | 8,557 / 14.26 | 12,724 / 15.10 | 21,246 / 17.26 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 4,787 / 12.96 | 6,462 / 13.70 | 8,557 / 14.26 | 12,724 / 15.10 |
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
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,198 / 2.00* | 3,146 / 2.51* | 5,709 / 3.08* | 10,901 / 5.39* |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 872 / 1.91* | 1,855 / 2.21* | 3,146 / 2.51* | 5,709 / 3.08* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,198 / 2.00* | 3,146 / 2.51* | 5,709 / 3.08* | 10,901 / 5.39* |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 872 / 1.91* | 1,855 / 2.21* | 3,146 / 2.51* | 5,709 / 3.08* |
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
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,709 / 3.08* | 41,976 / 15.78* | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,146 / 2.51* | 21,273 / 8.90* | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,709 / 3.08* | 41,976 / 15.78* | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,146 / 2.51* | 21,273 / 8.90* | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 967 / 1.82 | 3,295 / 2.96 | 14,620 / 6.79 | 24,359 / 10.97 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 757 / 1.70 | 2,082 / 2.34 | 6,110 / 4.67 | 14,620 / 6.79 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 967 / 1.82 | 3,295 / 2.96 | 14,620 / 6.79 | 24,359 / 10.97 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 757 / 1.70 | 2,082 / 2.34 | 6,110 / 4.67 | 14,620 / 6.79 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int2×fp16 mul + v × fp16 add | 2,212 / 6.52 | 3,318 / 9.78 | 3,871 / 11.41 | 4,424 / 13.04 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 2,395 / 4.01* | 6,292 / 5.02* | 11,417 / 6.16* | 21,802 / 10.78* |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,745 / 3.82* | 3,710 / 4.42* | 6,292 / 5.02* | 11,417 / 6.16* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | 1,872 / 3.89* | 4,184 / 4.47* | 7,217 / 5.08* | 13,389 / 7.48* |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | 1,483 / 3.78* | 2,658 / 4.14* | 4,184 / 4.47* | 7,217 / 5.08* |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,515 / 3.40 | 1,934 / 3.64 | 2,610 / 4.00 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,310* / 3.28* | 1,310 / 3.28 | 1,515 / 3.40 | 1,934 / 3.64 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | 1,529* / 3.29* | 1,926 / 3.37 | 2,566 / 3.57 | 3,859 / 3.91 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | 1,529* / 3.29* | 1,529 / 3.29 | 1,926 / 3.37 | 2,566 / 3.57 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×fp16 mul + v × fp16 add | 2,752 / 8.21 | 4,128 / 12.31 | 4,816 / 14.36 | 5,504 / 16.41 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 3,593 / 6.01* | 9,438 / 7.53* | 17,126 / 9.24* | 32,703 / 16.17* |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 2,617 / 5.73* | 5,565 / 6.63* | 9,438 / 7.53* | 17,126 / 9.24* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | 2,545 / 5.23 | 5,201 / 5.93 | 8,719 / 6.65 | 15,852 / 9.13 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | 2,091 / 5.07 | 3,441 / 5.51 | 5,201 / 5.93 | 8,719 / 6.65 |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 2,272 / 5.11 | 2,901 / 5.47 | 3,916 / 6.00 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 1,964* / 4.92* | 1,964 / 4.92 | 2,272 / 5.11 | 2,901 / 5.47 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | 2,303* / 4.93* | 2,919 / 5.03 | 3,882 / 5.32 | 5,835 / 5.76 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | 2,303* / 4.93* | 2,303 / 4.93 | 2,919 / 5.03 | 3,882 / 5.32 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×fp16 mul + v × fp16 add | 2,960 / 9.10 | 4,440 / 13.66 | 5,180 / 15.93 | 5,920 / 18.21 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 4,791 / 8.02* | 12,584 / 10.04* | 22,834 / 12.32* | 43,605 / 21.56* |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 3,489 / 7.65* | 7,419 / 8.85* | 12,584 / 10.04* | 22,834 / 12.32* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | 3,218 / 6.93 | 6,232 / 7.73 | 10,226 / 8.52 | 18,337 / 11.08 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | 2,701 / 6.74 | 4,234 / 7.25 | 6,232 / 7.73 | 10,226 / 8.52 |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 3,030 / 6.81 | 3,868 / 7.29 | 5,221 / 7.99 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 2,619* / 6.56* | 2,619 / 6.56 | 3,030 / 6.81 | 3,868 / 7.29 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | 3,128* / 6.57* | 4,015 / 6.70 | 5,372 / 7.08 | 8,111 / 7.65 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | 3,128* / 6.57* | 3,128 / 6.57 | 4,015 / 6.70 | 5,372 / 7.08 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×fp16 mul + v × fp16 add | 3,405 / 9.85 | 5,107 / 14.77 | 5,958 / 17.23 | 6,809 / 19.70 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 7,186 / 12.03* | 18,876 / 15.05* | 34,251 / 18.48* | 65,407 / 32.34* |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 5,234 / 11.47* | 11,129 / 13.27* | 18,876 / 15.05* | 34,251 / 18.48* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | 4,563 / 10.33 | 8,295 / 11.32 | 13,241 / 12.26 | 23,300 / 14.97 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | 3,919 / 10.09 | 5,821 / 10.73 | 8,295 / 11.32 | 13,241 / 12.26 |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 4,544 / 10.21 | 5,801 / 10.93 | 7,831 / 11.99 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 3,929* / 9.84* | 3,929 / 9.84 | 4,544 / 10.21 | 5,801 / 10.93 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | 4,947* / 9.91* | 6,481 / 10.09 | 8,807 / 10.71 | 14,733 / 12.10 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | 4,947* / 9.91* | 4,947 / 9.91 | 6,481 / 10.09 | 8,807 / 10.71 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×fp16 mul + v × fp16 add | 3,754 / 10.74 | 5,631 / 16.11 | 6,570 / 18.79 | 7,509 / 21.48 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 9,581 / 16.03* | 25,168 / 20.07* | 45,668 / 24.64* | 87,209 / 43.12* |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 6,978 / 15.29* | 14,839 / 17.69* | 25,168 / 20.07* | 45,668 / 24.64* |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | 5,908 / 13.74 | 10,358 / 14.91 | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | 5,138 / 13.44 | 7,408 / 14.20 | 10,358 / 14.91 | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 6,059 / 13.62 | 7,735 / 14.58 | 10,442 / 15.99 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 5,239* / 13.12* | 5,239 / 13.12 | 6,059 / 13.62 | 7,735 / 14.58 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | 6,966* / 13.30* | 9,292 / 13.53 | 13,211 / 14.61 | 21,816 / 16.43 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | 6,966* / 13.30* | 6,966 / 13.30 | 9,292 / 13.53 | 13,211 / 14.61 |
