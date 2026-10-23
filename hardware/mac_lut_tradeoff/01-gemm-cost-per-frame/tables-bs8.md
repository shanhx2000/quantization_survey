# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 8

Generated 2026-10-23 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6.
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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,947* / 12.62* | 5,502 / 12.76 | 6,334 / 12.96 | 8,099 / 13.29 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,947* / 12.62* | 5,076 / 12.67 | 5,502 / 12.76 | 6,334 / 12.96 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,947* / 12.62* | 5,502 / 12.76 | 6,334 / 12.96 | 8,099 / 13.29 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,947* / 12.62* | 5,076 / 12.67 | 5,502 / 12.76 | 6,334 / 12.96 |

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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 6,077 / 12.88 | 19,209 / 15.88 | 71,287 / 23.88 | 144,895 / 32.47 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,331 / 12.70 | 12,281 / 14.35 | 33,561 / 19.09 | 71,287 / 23.88 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 6,077 / 12.88 | 19,209 / 15.88 | 71,287 / 23.88 | 144,895 / 32.47 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,331 / 12.70 | 12,281 / 14.35 | 33,561 / 19.09 | 71,287 / 23.88 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int2×int8 mul + 8·v × fp16 add | 17,555 / 51.94 | 26,333 / 77.91 | 30,722 / 90.90 | 35,111 / 103.88 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,895* / 25.24* | 11,004 / 25.53 | 12,668 / 25.91 | 16,198 / 26.58 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,895* / 25.24* | 10,151 / 25.34 | 11,004 / 25.53 | 12,668 / 25.91 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | 11,979* / 25.53* | 14,101 / 25.89 | 17,162 / 26.33 | 23,206 / 27.09 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | 11,979* / 25.53* | 12,556 / 25.69 | 14,101 / 25.89 | 17,162 / 26.33 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int3×int8 mul + 8·v × fp16 add | 18,003 / 52.45 | 27,004 / 78.68 | 31,505 / 91.79 | 36,006 / 104.90 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,842* / 37.86* | 16,506 / 38.29 | 19,002 / 38.87 | 24,297 / 39.88 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,842* / 37.86* | 15,227 / 38.01 | 16,506 / 38.29 | 19,002 / 38.87 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | 18,231* / 38.48* | 21,474 / 39.04 | 26,046 / 39.68 | 35,097 / 40.77 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | 18,231* / 38.48* | 19,151 / 38.76 | 21,474 / 39.04 | 26,046 / 39.68 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int4×int8 mul + 8·v × fp16 add | 18,539 / 52.75 | 27,809 / 79.12 | 32,443 / 92.31 | 37,078 / 105.50 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,789* / 50.47* | 22,009 / 51.06 | 25,336 / 51.82 | 32,395 / 53.17 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,789* / 50.47* | 20,302 / 50.68 | 22,009 / 51.06 | 25,336 / 51.82 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | 24,949* / 51.57* | 29,548 / 52.37 | 35,914 / 53.24 | 48,551 / 54.71 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | 24,949* / 51.57* | 26,290 / 52.00 | 29,548 / 52.37 | 35,914 / 53.24 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int6×int8 mul + 8·v × fp16 add | 19,886 / 55.43 | 29,829 / 83.14 | 34,800 / 97.00 | 39,772 / 110.85 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | 29,684* / 75.71* | 33,013 / 76.58 | 38,004 / 77.73 | 48,593 / 79.75 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | 29,684* / 75.71* | 30,453 / 76.03 | 33,013 / 76.58 | 38,004 / 77.73 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | 39,761* / 78.17* | 47,727 / 79.59 | 58,557 / 81.02 | 80,107 / 83.44 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | 39,761* / 78.17* | 42,174 / 78.98 | 47,727 / 79.59 | 58,557 / 81.02 |

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
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | 39,578* / 100.95* | 44,017 / 102.11 | 50,672 / 103.64 | 64,791 / 106.34 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | 39,578* / 100.95* | 40,605 / 101.37 | 44,017 / 102.11 | 50,672 / 103.64 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | 56,379* / 105.34* | 68,583 / 107.55 | 85,058 / 109.68 | 117,834 / 113.29 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | 56,379* / 105.34* | 60,171 / 106.64 | 68,583 / 107.55 | 85,058 / 109.68 |

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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | 5,838* / 12.96* | 6,488 / 13.11 | 7,765 / 13.41 | 10,316 / 13.97 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | 5,838* / 12.96* | 5,838 / 12.96 | 6,488 / 13.11 | 7,765 / 13.41 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | 5,838* / 12.96* | 6,488 / 13.11 | 7,765 / 13.41 | 10,316 / 13.97 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | 5,838* / 12.96* | 5,838 / 12.96 | 6,488 / 13.11 | 7,765 / 13.41 |

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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | 7,765 / 13.41 | 26,075 / 17.57 | 105,059 / 29.44 | 213,605 / 41.56 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | 6,488 / 13.11 | 16,207 / 15.41 | 46,560 / 22.17 | 105,059 / 29.44 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | 7,765 / 13.41 | 26,075 / 17.57 | 105,059 / 29.44 | 213,605 / 41.56 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | 6,488 / 13.11 | 16,207 / 15.41 | 46,560 / 22.17 | 105,059 / 29.44 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int2×fp16 mul + 8·v × fp16 add | 17,785 / 52.66 | 26,678 / 78.99 | 31,124 / 92.16 | 35,570 / 105.33 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 8·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·16b, 1R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 2R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 8·16b, 1R] + 16 × fp16 add | 11,675* / 25.92* | 12,976 / 26.22 | 15,530 / 26.82 | 20,631 / 27.94 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·16b, 1R] + 16 × fp16 add | 11,675* / 25.92* | 11,675 / 25.92 | 12,976 / 26.22 | 15,530 / 26.82 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 2R] + 16 × fp16 add | 15,964* / 26.55* | 18,187 / 26.83 | 22,594 / 27.43 | 31,319 / 28.50 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 2R] + 16 × fp16 add | 15,964* / 26.55* | 15,964 / 26.55 | 18,187 / 26.83 | 22,594 / 27.43 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int3×fp16 mul + 8·v × fp16 add | 22,543 / 67.59 | 33,814 / 101.39 | 39,450 / 118.28 | 45,086 / 135.18 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 8·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·16b, 1R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 3R] + 24 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 8·16b, 1R] + 24 × fp16 add | 17,513* / 38.89* | 19,463 / 39.33 | 23,295 / 40.23 | 30,947 / 41.90 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·16b, 1R] + 24 × fp16 add | 17,513* / 38.89* | 17,513 / 38.89 | 19,463 / 39.33 | 23,295 / 40.23 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 3R] + 24 × fp16 add | 24,693* / 40.29* | 28,045 / 40.68 | 34,657 / 41.55 | 47,769 / 43.10 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 3R] + 24 × fp16 add | 24,693* / 40.29* | 24,693 / 40.29 | 28,045 / 40.68 | 34,657 / 41.55 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int4×fp16 mul + 8·v × fp16 add | 23,632 / 70.04 | 35,447 / 105.06 | 41,355 / 122.57 | 47,263 / 140.08 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 8·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·16b, 1R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 4R] + 32 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 8·16b, 1R] + 32 × fp16 add | 23,350* / 51.85* | 25,951 / 52.44 | 31,060 / 53.65 | 41,262 / 55.87 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·16b, 1R] + 32 × fp16 add | 23,350* / 51.85* | 23,350 / 51.85 | 25,951 / 52.44 | 31,060 / 53.65 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 4R] + 32 × fp16 add | 33,516* / 54.35* | 37,977 / 54.88 | 46,727 / 56.06 | 64,113 / 58.17 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 4R] + 32 × fp16 add | 33,516* / 54.35* | 33,516 / 54.35 | 37,977 / 54.88 | 46,727 / 56.06 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int6×fp16 mul + 8·v × fp16 add | 26,587 / 79.76 | 39,881 / 119.64 | 46,527 / 139.58 | 53,174 / 159.52 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 8·16b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·16b, 1R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 6R] + 48 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 8·16b, 1R] + 48 × fp16 add | 35,025* / 77.77* | 38,927 / 78.66 | 46,591 / 80.47 | 61,894 / 83.81 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·16b, 1R] + 48 × fp16 add | 35,025* / 77.77* | 35,025 / 77.77 | 38,927 / 78.66 | 46,591 / 80.47 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 6R] + 48 × fp16 add | 55,329* / 83.45* | 62,943 / 84.33 | 77,856 / 86.29 | 107,533 / 89.77 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 6R] + 48 × fp16 add | 55,329* / 83.45* | 55,329 / 83.45 | 62,943 / 84.33 | 77,856 / 86.29 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 8·v × fp16 mul + 8·v × fp16 add | 28,760 / 83.01 | 43,140 / 124.51 | 50,330 / 145.26 | 57,521 / 166.01 |
| MAC opt | 8·v × int8×fp16 mul + 8·v × fp16 add | 29,333 / 84.32 | 43,999 / 126.48 | 51,332 / 147.56 | 58,666 / 168.64 |
| MAC int8 | 8·v × int8 mul + 8·v × int16 add | 5,600 / 9.52 | 8,401 / 14.28 | 9,801 / 16.66 | 11,201 / 19.04 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 8·16b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·16b, 1R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 8R] + 64 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 8·16b, 1R] + 64 × fp16 add | 46,700* / 103.70* | 51,903 / 104.88 | 62,121 / 107.29 | 82,525 / 111.75 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·16b, 1R] + 64 × fp16 add | 46,700* / 103.70* | 46,700 / 103.70 | 51,903 / 104.88 | 62,121 / 107.29 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 8R] + 64 × fp16 add | 80,914* / 113.89* | 92,457 / 115.20 | 115,132 / 118.10 | 160,244 / 123.28 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 8R] + 64 × fp16 add | 80,914* / 113.89* | 80,914 / 113.89 | 92,457 / 115.20 | 115,132 / 118.10 |
