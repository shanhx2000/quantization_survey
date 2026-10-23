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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,947* / 12.75* | 5,502 / 13.04 | 6,334 / 13.48 | 8,099 / 14.32 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,947* / 12.75* | 5,076 / 12.82 | 5,502 / 13.04 | 6,334 / 13.48 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,947* / 12.75* | 5,502 / 13.04 | 6,334 / 13.48 | 8,099 / 14.32 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 4,947* / 12.75* | 5,076 / 12.82 | 5,502 / 13.04 | 6,334 / 13.48 |

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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 6,077 / 13.36 | 19,209 / 20.48 | 71,287 / 39.54 | 144,895 / 63.78 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,331 / 12.95 | 12,281 / 16.68 | 33,561 / 27.74 | 71,287 / 39.54 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 6,077 / 13.36 | 19,209 / 20.48 | 71,287 / 39.54 | 144,895 / 63.78 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,331 / 12.95 | 12,281 / 16.68 | 33,561 / 27.74 | 71,287 / 39.54 |

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
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,895* / 25.50* | 11,004 / 26.08 | 12,668 / 26.96 | 16,198 / 28.63 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 9,895* / 25.50* | 10,151 / 25.63 | 11,004 / 26.08 | 12,668 / 26.96 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | 11,979* / 25.79* | 14,101 / 26.40 | 17,162 / 27.31 | 23,206 / 28.99 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 2R] + 16 × fp16 add | 11,979* / 25.79* | 12,556 / 25.98 | 14,101 / 26.40 | 17,162 / 27.31 |

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
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,842* / 38.26* | 16,506 / 39.12 | 19,002 / 40.44 | 24,297 / 42.95 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 24 × fp16 add | 14,842* / 38.26* | 15,227 / 38.45 | 16,506 / 39.12 | 19,002 / 40.44 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | 18,231* / 38.79* | 21,474 / 39.66 | 26,046 / 40.83 | 35,097 / 42.98 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 3R] + 24 × fp16 add | 18,231* / 38.79* | 19,151 / 39.11 | 21,474 / 39.66 | 26,046 / 40.83 |

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
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,789* / 51.01* | 22,009 / 52.16 | 25,336 / 53.92 | 32,395 / 57.27 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 32 × fp16 add | 19,789* / 51.01* | 20,302 / 51.27 | 22,009 / 52.16 | 25,336 / 53.92 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | 24,949* / 51.94* | 29,548 / 53.09 | 35,914 / 54.56 | 48,551 / 57.24 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 4R] + 32 × fp16 add | 24,949* / 51.94* | 26,290 / 52.41 | 29,548 / 53.09 | 35,914 / 54.56 |

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
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | 29,684* / 76.51* | 33,013 / 78.24 | 38,004 / 80.87 | 48,593 / 85.90 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 48 × fp16 add | 29,684* / 76.51* | 30,453 / 76.90 | 33,013 / 78.24 | 38,004 / 80.87 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | 39,761* / 78.67* | 47,727 / 80.53 | 58,557 / 82.70 | 80,107 / 86.61 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 6R] + 48 × fp16 add | 39,761* / 78.67* | 42,174 / 79.54 | 47,727 / 80.53 | 58,557 / 82.70 |

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
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | 39,578* / 102.01* | 44,017 / 104.32 | 50,672 / 107.83 | 64,791 / 114.53 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 1R] + 64 × fp16 add | 39,578* / 102.01* | 40,605 / 102.54 | 44,017 / 104.32 | 50,672 / 107.83 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | 56,379* / 105.97* | 68,583 / 108.72 | 85,058 / 111.73 | 117,834 / 117.11 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·(8+⌈log2 v⌉)b, 8R] + 64 × fp16 add | 56,379* / 105.97* | 60,171 / 107.36 | 68,583 / 108.72 | 85,058 / 111.73 |

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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | 5,838* / 13.21* | 6,488 / 13.58 | 7,765 / 14.31 | 10,316 / 15.74 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | 5,838* / 13.21* | 5,838 / 13.21 | 6,488 / 13.58 | 7,765 / 14.31 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 1R] + 8 × fp16 add | 5,838* / 13.21* | 6,488 / 13.58 | 7,765 / 14.31 | 10,316 / 15.74 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 1R] + 8 × fp16 add | 5,838* / 13.21* | 5,838 / 13.21 | 6,488 / 13.58 | 7,765 / 14.31 |

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
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | 7,765 / 14.31 | 26,075 / 24.04 | 105,059 / 53.12 | 213,605 / 85.37 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | 6,488 / 13.58 | 16,207 / 18.68 | 46,560 / 34.01 | 105,059 / 53.12 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 8·16b, 1R] + 8 × fp16 add | 7,765 / 14.31 | 26,075 / 24.04 | 105,059 / 53.12 | 213,605 / 85.37 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 8·16b, 1R] + 8 × fp16 add | 6,488 / 13.58 | 16,207 / 18.68 | 46,560 / 34.01 | 105,059 / 53.12 |

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
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 8·16b, 1R] + 16 × fp16 add | 11,675* / 26.42* | 12,976 / 27.16 | 15,530 / 28.62 | 20,631 / 31.47 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 8·16b, 1R] + 16 × fp16 add | 11,675* / 26.42* | 11,675 / 26.42 | 12,976 / 27.16 | 15,530 / 28.62 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 2R] + 16 × fp16 add | 15,964* / 26.95* | 18,187 / 27.55 | 22,594 / 28.79 | 31,319 / 31.14 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 2R] + 16 × fp16 add | 15,964* / 26.95* | 15,964 / 26.95 | 18,187 / 27.55 | 22,594 / 28.79 |

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
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 8·16b, 1R] + 24 × fp16 add | 17,513* / 39.63* | 19,463 / 40.74 | 23,295 / 42.94 | 30,947 / 47.21 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 8·16b, 1R] + 24 × fp16 add | 17,513* / 39.63* | 17,513 / 39.63 | 19,463 / 40.74 | 23,295 / 42.94 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 3R] + 24 × fp16 add | 24,693* / 40.78* | 28,045 / 41.55 | 34,657 / 43.16 | 47,769 / 46.19 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 3R] + 24 × fp16 add | 24,693* / 40.78* | 24,693 / 40.78 | 28,045 / 41.55 | 34,657 / 43.16 |

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
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 8·16b, 1R] + 32 × fp16 add | 23,350* / 52.84* | 25,951 / 54.32 | 31,060 / 57.25 | 41,262 / 62.95 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 8·16b, 1R] + 32 × fp16 add | 23,350* / 52.84* | 23,350 / 52.84 | 25,951 / 54.32 | 31,060 / 57.25 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 4R] + 32 × fp16 add | 33,516* / 54.95* | 37,977 / 55.91 | 46,727 / 57.93 | 64,113 / 61.72 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 4R] + 32 × fp16 add | 33,516* / 54.95* | 33,516 / 54.95 | 37,977 / 55.91 | 46,727 / 57.93 |

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
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 8·16b, 1R] + 48 × fp16 add | 35,025* / 79.26* | 38,927 / 81.47 | 46,591 / 85.87 | 61,894 / 94.42 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 8·16b, 1R] + 48 × fp16 add | 35,025* / 79.26* | 35,025 / 79.26 | 38,927 / 81.47 | 46,591 / 85.87 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 6R] + 48 × fp16 add | 55,329* / 84.31* | 62,943 / 85.71 | 77,856 / 88.70 | 107,533 / 94.26 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 6R] + 48 × fp16 add | 55,329* / 84.31* | 55,329 / 84.31 | 62,943 / 85.71 | 77,856 / 88.70 |

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
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 8·16b, 1R] + 64 × fp16 add | 46,700* / 105.68* | 51,903 / 108.63 | 62,121 / 114.50 | 82,525 / 125.89 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 8·16b, 1R] + 64 × fp16 add | 46,700* / 105.68* | 46,700 / 105.68 | 51,903 / 108.63 | 62,121 / 114.50 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 8·16b, 8R] + 64 × fp16 add | 80,914* / 115.02* | 92,457 / 116.94 | 115,132 / 121.06 | 160,244 / 128.68 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 8·16b, 8R] + 64 × fp16 add | 80,914* / 115.02* | 80,914 / 115.02 | 92,457 / 116.94 | 115,132 / 121.06 |
