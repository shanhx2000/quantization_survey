# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 2

Generated 2026-10-28 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 2.

## wq = binary, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,206 / 12.36 | 6,310 / 18.54 | 7,361 / 21.63 | 8,413 / 24.72 |
| MAC opt | 2·v × fp16 add | 4,206 / 12.36 | 6,310 / 18.54 | 7,361 / 21.63 | 8,413 / 24.72 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,922 / 3.37 | 4,697 / 3.68 | 8,281 / 3.93 | 15,513 / 4.35 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,508 / 3.30 | 2,912 / 3.50 | 4,697 / 3.68 | 8,281 / 3.93 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,922 / 3.37 | 4,697 / 3.68 | 8,281 / 3.93 | 15,513 / 4.35 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,508 / 3.30 | 2,912 / 3.50 | 4,697 / 3.68 | 8,281 / 3.93 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,263* / 3.20* | 1,400 / 3.24 | 1,684 / 3.31 | 2,168 / 3.44 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,263* / 3.20* | 1,263 / 3.20 | 1,400 / 3.24 | 1,684 / 3.31 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,263* / 3.20* | 1,400 / 3.24 | 1,684 / 3.31 | 2,168 / 3.44 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,263* / 3.20* | 1,263 / 3.20 | 1,400 / 3.24 | 1,684 / 3.31 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,206 / 12.36 | 6,310 / 18.54 | 7,361 / 21.63 | 8,413 / 24.72 |
| MAC opt | 2·v × fp16 add | 4,206 / 12.36 | 6,310 / 18.54 | 7,361 / 21.63 | 8,413 / 24.72 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 7,683 / 3.90 | 58,712 / 7.04 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 4,397 / 3.65 | 29,950 / 5.31 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 7,683 / 3.90 | 58,712 / 7.04 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 4,397 / 3.65 | 29,950 / 5.31 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,684 / 3.31 | 5,430 / 4.18 | 20,074 / 5.89 | 37,224 / 9.15 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,400 / 3.24 | 3,210 / 3.63 | 9,355 / 5.09 | 20,074 / 5.89 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,684 / 3.31 | 5,430 / 4.18 | 20,074 / 5.89 | 37,224 / 9.15 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·(8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,400 / 3.24 | 3,210 / 3.63 | 9,355 / 5.09 | 20,074 / 5.89 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int2×int8 mul + 2·v × fp16 add | 4,475 / 13.11 | 6,712 / 19.66 | 7,830 / 22.94 | 8,949 / 26.21 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,845 / 6.73 | 9,395 / 7.35 | 16,563 / 7.86 | 31,027 / 8.71 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,017 / 6.60 | 5,824 / 7.00 | 9,395 / 7.35 | 16,563 / 7.86 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,526* / 6.40* | 2,801 / 6.47 | 3,367 / 6.62 | 4,336 / 6.87 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,526* / 6.40* | 2,526 / 6.40 | 2,801 / 6.47 | 3,367 / 6.62 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | 2,860* / 6.44* | 3,386 / 6.50 | 4,464 / 6.65 | 6,085 / 6.94 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 2R] + 4 × fp16 add | 2,860* / 6.44* | 2,860 / 6.44 | 3,386 / 6.50 | 4,464 / 6.65 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int3×int8 mul + 2·v × fp16 add | 4,586 / 13.23 | 6,880 / 19.85 | 8,026 / 23.16 | 9,173 / 26.47 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 5,767 / 10.10 | 14,092 / 11.03 | 24,844 / 11.80 | 46,540 / 13.06 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 4,525 / 9.90 | 8,736 / 10.50 | 14,092 / 11.03 | 24,844 / 11.80 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,789* / 9.60* | 4,201 / 9.71 | 5,051 / 9.94 | 6,504 / 10.31 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,789* / 9.60* | 3,789 / 9.60 | 4,201 / 9.71 | 5,051 / 9.94 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | 4,314* / 9.69* | 5,125 / 9.76 | 6,762 / 9.99 | 9,209 / 10.43 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 3R] + 6 × fp16 add | 4,314* / 9.69* | 4,314 / 9.69 | 5,125 / 9.76 | 6,762 / 9.99 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int4×int8 mul + 2·v × fp16 add | 4,720 / 13.31 | 7,081 / 19.96 | 8,261 / 23.29 | 9,441 / 26.62 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,690 / 13.47 | 18,790 / 14.71 | 33,125 / 15.73 | 62,053 / 17.42 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 6,033 / 13.20 | 11,647 / 14.00 | 18,790 / 14.71 | 33,125 / 15.73 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,052* / 12.80* | 5,602 / 12.94 | 6,735 / 13.25 | 8,672 / 13.75 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,052* / 12.80* | 5,052 / 12.80 | 5,602 / 12.94 | 6,735 / 13.25 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | 5,849* / 12.95* | 7,012 / 13.05 | 9,598 / 13.56 | 13,337 / 14.09 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 4R] + 8 × fp16 add | 5,849* / 12.95* | 5,849 / 12.95 | 7,012 / 13.05 | 9,598 / 13.56 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int6×int8 mul + 2·v × fp16 add | 5,057 / 13.98 | 7,586 / 20.97 | 8,850 / 24.46 | 10,114 / 27.96 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 11,534 / 20.20 | 28,184 / 22.06 | 49,688 / 23.59 | 93,080 / 26.13 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 9,050 / 19.81 | 17,471 / 21.00 | 28,184 / 22.06 | 49,688 / 23.59 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,578* / 19.21* | 8,403 / 19.42 | 10,102 / 19.87 | 13,008 / 20.62 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 12 × fp16 add | 7,578* / 19.21* | 7,578 / 19.21 | 8,403 / 19.42 | 10,102 / 19.87 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | 9,177* / 19.54* | 11,191 / 19.70 | 15,463 / 20.57 | 21,729 / 21.44 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 6R] + 12 × fp16 add | 9,177* / 19.54* | 9,177 / 19.54 | 11,191 / 19.70 | 15,463 / 20.57 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int8×int8 mul + 2·v × fp16 add | 5,358 / 14.45 | 8,036 / 21.68 | 9,376 / 25.29 | 10,715 / 28.90 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 15,379 / 26.93 | 37,579 / 29.41 | 66,251 / 31.46 | 124,107 / 34.84 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 12,067 / 26.41 | 23,295 / 28.01 | 37,579 / 29.41 | 66,251 / 31.46 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 10,104* / 25.61* | 11,204 / 25.89 | 13,470 / 26.50 | 17,343 / 27.50 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 1R] + 16 × fp16 add | 10,104* / 25.61* | 10,104 / 25.61 | 11,204 / 25.89 | 13,470 / 26.50 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | 12,827* / 26.22* | 15,890 / 26.47 | 22,203 / 27.77 | 31,634 / 29.07 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·(8+⌈log2 v⌉)b, 8R] + 16 × fp16 add | 12,827* / 26.22* | 12,827 / 26.22 | 15,890 / 26.47 | 22,203 / 27.77 |

## wq = binary, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,206 / 12.36 | 6,310 / 18.54 | 7,361 / 21.63 | 8,413 / 24.72 |
| MAC opt | 2·v × fp16 add | 4,206 / 12.36 | 6,310 / 18.54 | 7,361 / 21.63 | 8,413 / 24.72 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 2,395 / 3.49 | 6,206 / 3.83 | 11,274 / 4.11 | 21,517 / 4.55 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,755 / 3.41 | 3,679 / 3.62 | 6,206 / 3.83 | 11,274 / 4.11 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 2,395 / 3.49 | 6,206 / 3.83 | 11,274 / 4.11 | 21,517 / 4.55 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,755 / 3.41 | 3,679 / 3.62 | 6,206 / 3.83 | 11,274 / 4.11 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 1,336* / 3.23* | 1,510 / 3.27 | 1,861 / 3.36 | 2,639 / 3.49 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,336* / 3.23* | 1,336 / 3.23 | 1,510 / 3.27 | 1,861 / 3.36 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 1R] + 2 × fp16 add | 1,336* / 3.23* | 1,510 / 3.27 | 1,861 / 3.36 | 2,639 / 3.49 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 1R] + 2 × fp16 add | 1,336* / 3.23* | 1,336 / 3.23 | 1,510 / 3.27 | 1,861 / 3.36 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 add | 4,206 / 12.36 | 6,310 / 18.54 | 7,361 / 21.63 | 8,413 / 24.72 |
| MAC opt | 2·v × fp16 add | 4,206 / 12.36 | 6,310 / 18.54 | 7,361 / 21.63 | 8,413 / 24.72 |
| MAC int8 | 2·v × int16 add | 262 / 0.42 | 393 / 0.64 | 459 / 0.74 | 524 / 0.85 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 11,274 / 4.11 | 83,063 / 7.50 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 6,206 / 3.83 | 41,913 / 5.54 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 11,274 / 4.11 | 83,063 / 7.50 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 6,206 / 3.83 | 41,913 / 5.54 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 1,861 / 3.36 | 6,714 / 4.52 | 25,555 / 6.75 | 54,186 / 10.74 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 1,510 / 3.27 | 3,861 / 3.79 | 12,123 / 5.73 | 25,555 / 6.75 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 2·16b, 1R] + 2 × fp16 add | 1,861 / 3.36 | 6,714 / 4.52 | 25,555 / 6.75 | 54,186 / 10.74 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 2·16b, 1R] + 2 × fp16 add | 1,510 / 3.27 | 3,861 / 3.79 | 12,123 / 5.73 | 25,555 / 6.75 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int2×fp16 mul + 2·v × fp16 add | 4,532 / 13.29 | 6,798 / 19.93 | 7,931 / 23.25 | 9,064 / 26.57 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 2·16b, 1R] + 4 × fp16 add | 4,790 / 6.98 | 12,413 / 7.65 | 22,548 / 8.22 | 43,033 / 9.11 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·16b, 1R] + 4 × fp16 add | 3,510 / 6.83 | 7,358 / 7.24 | 12,413 / 7.65 | 22,548 / 8.22 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 2R] + 4 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 2·16b, 1R] + 4 × fp16 add | 2,673* / 6.46* | 3,020 / 6.55 | 3,722 / 6.72 | 5,278 / 6.99 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 2·16b, 1R] + 4 × fp16 add | 2,673* / 6.46* | 2,673 / 6.46 | 3,020 / 6.55 | 3,722 / 6.72 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 2R] + 4 × fp16 add | 3,129* / 6.52* | 3,764 / 6.59 | 5,063 / 6.77 | 7,842 / 7.26 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 2R] + 4 × fp16 add | 3,129* / 6.52* | 3,129 / 6.52 | 3,764 / 6.59 | 5,063 / 6.77 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int3×fp16 mul + 2·v × fp16 add | 5,721 / 17.02 | 8,582 / 25.53 | 10,012 / 29.78 | 11,443 / 34.04 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 2·16b, 1R] + 6 × fp16 add | 7,185 / 10.47 | 18,619 / 11.48 | 33,822 / 12.33 | 64,550 / 13.66 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·16b, 1R] + 6 × fp16 add | 5,265 / 10.24 | 11,038 / 10.86 | 18,619 / 11.48 | 33,822 / 12.33 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 3R] + 6 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 2·16b, 1R] + 6 × fp16 add | 4,009* / 9.70* | 4,530 / 9.82 | 5,583 / 10.09 | 7,918 / 10.48 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 2·16b, 1R] + 6 × fp16 add | 4,009* / 9.70* | 4,009 / 9.70 | 4,530 / 9.82 | 5,583 / 10.09 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 3R] + 6 × fp16 add | 4,719* / 9.82* | 5,701 / 9.91 | 7,666 / 10.19 | 11,823 / 10.92 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 3R] + 6 × fp16 add | 4,719* / 9.82* | 4,719 / 9.82 | 5,701 / 9.91 | 7,666 / 10.19 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int4×fp16 mul + 2·v × fp16 add | 5,994 / 17.63 | 8,990 / 26.45 | 10,489 / 30.85 | 11,987 / 35.26 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 2·16b, 1R] + 8 × fp16 add | 9,580 / 13.96 | 24,825 / 15.31 | 45,096 / 16.44 | 86,067 / 18.21 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·16b, 1R] + 8 × fp16 add | 7,020 / 13.65 | 14,717 / 14.48 | 24,825 / 15.31 | 45,096 / 16.44 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 4R] + 8 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 2·16b, 1R] + 8 × fp16 add | 5,346* / 12.93* | 6,040 / 13.09 | 7,444 / 13.45 | 10,557 / 13.98 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 2·16b, 1R] + 8 × fp16 add | 5,346* / 12.93* | 5,346 / 12.93 | 6,040 / 13.09 | 7,444 / 13.45 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 4R] + 8 × fp16 add | 6,429* / 13.15* | 7,829 / 13.27 | 10,587 / 13.65 | 16,378 / 14.67 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 4R] + 8 × fp16 add | 6,429* / 13.15* | 6,429 / 13.15 | 7,829 / 13.27 | 10,587 / 13.65 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int6×fp16 mul + 2·v × fp16 add | 6,732 / 20.06 | 10,099 / 30.09 | 11,782 / 35.11 | 13,465 / 40.12 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 2·16b, 1R] + 12 × fp16 add | 14,370 / 20.93 | 37,238 / 22.96 | 67,645 / 24.65 | 129,100 / 27.32 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·16b, 1R] + 12 × fp16 add | 10,530 / 20.48 | 22,075 / 21.72 | 37,238 / 22.96 | 67,645 / 24.65 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 6R] + 12 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 2·16b, 1R] + 12 × fp16 add | 8,019* / 19.39* | 9,060 / 19.64 | 11,165 / 20.17 | 15,835 / 20.97 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 2·16b, 1R] + 12 × fp16 add | 8,019* / 19.39* | 8,019 / 19.39 | 9,060 / 19.64 | 11,165 / 20.17 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 6R] + 12 × fp16 add | 10,199* / 19.89* | 12,618 / 20.10 | 17,374 / 20.72 | 27,180 / 22.46 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 6R] + 12 × fp16 add | 10,199* / 19.89* | 10,199 / 19.89 | 12,618 / 20.10 | 17,374 / 20.72 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | 2·v × fp16 mul + 2·v × fp16 add | 7,389 / 20.94 | 11,083 / 31.41 | 12,930 / 36.64 | 14,777 / 41.87 |
| MAC opt | 2·v × int8×fp16 mul + 2·v × fp16 add | 7,419 / 21.20 | 11,128 / 31.80 | 12,983 / 37.10 | 14,838 / 42.40 |
| MAC int8 | 2·v × int8 mul + 2·v × int16 add | 1,413 / 2.52 | 2,120 / 3.77 | 2,473 / 4.40 | 2,826 / 5.03 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 2·16b, 1R] + 16 × fp16 add | 19,160 / 27.91 | 49,650 / 30.62 | 90,193 / 32.87 | 172,133 / 36.43 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·16b, 1R] + 16 × fp16 add | 14,040 / 27.30 | 29,434 / 28.95 | 49,650 / 30.62 | 90,193 / 32.87 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 8R] + 16 × fp16 add | # / # | # / # | # / # | # / # |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 2·16b, 1R] + 16 × fp16 add | 10,692* / 25.86* | 12,080 / 26.19 | 14,887 / 26.90 | 21,113 / 27.96 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 2·16b, 1R] + 16 × fp16 add | 10,692* / 25.86* | 10,692 / 25.86 | 12,080 / 26.19 | 14,887 / 26.90 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 2·16b, 8R] + 16 × fp16 add | 15,076* / 26.84* | 18,493 / 27.18 | 25,409 / 28.14 | 40,225 / 30.64 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 2·16b, 8R] + 16 × fp16 add | 15,076* / 26.84* | 15,076 / 26.84 | 18,493 / 27.18 | 25,409 / 28.14 |
