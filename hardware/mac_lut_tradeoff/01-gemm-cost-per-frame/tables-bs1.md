# 01 — MAC-GEMM vs LUT-GEMM cost, batch size 1

Generated 2026-10-28 by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. `#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6.
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × 1.

## wq = int1, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,103 / 6.18 | 3,155 / 9.27 | 3,681 / 10.81 | 4,206 / 12.36 |
| MAC opt | v × fp16 add | 2,103 / 6.18 | 3,155 / 9.27 | 3,681 / 10.81 | 4,206 / 12.36 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 972 / 1.70 | 2,392 / 1.90 | 4,216 / 2.06 | 7,906 / 2.31 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 760 / 1.66 | 1,476 / 1.78 | 2,392 / 1.90 | 4,216 / 2.06 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 972 / 1.70 | 2,392 / 1.90 | 4,216 / 2.06 | 7,906 / 2.31 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 760 / 1.66 | 1,476 / 1.78 | 2,392 / 1.90 | 4,216 / 2.06 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 666* / 1.62* | 768 / 1.65 | 978 / 1.71 | 1,316 / 1.79 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 666* / 1.62* | 666 / 1.62 | 768 / 1.65 | 978 / 1.71 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 666* / 1.62* | 768 / 1.65 | 978 / 1.71 | 1,316 / 1.79 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 666* / 1.62* | 666 / 1.62 | 768 / 1.65 | 978 / 1.71 |

## wq = ter, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,103 / 6.18 | 3,155 / 9.27 | 3,681 / 10.81 | 4,206 / 12.36 |
| MAC opt | v × fp16 add | 2,103 / 6.18 | 3,155 / 9.27 | 3,681 / 10.81 | 4,206 / 12.36 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 3,916 / 2.03 | 30,056 / 4.04 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 2,239 / 1.87 | 15,280 / 2.94 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 3,916 / 2.03 | 30,056 / 4.04 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 2,239 / 1.87 | 15,280 / 2.94 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 978 / 1.71 | 3,306 / 2.21 | 14,631 / 3.51 | 24,370 / 5.04 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 768 / 1.65 | 2,093 / 1.93 | 6,121 / 2.92 | 14,631 / 3.51 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 978 / 1.71 | 3,306 / 2.21 | 14,631 / 3.51 | 24,370 / 5.04 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × (8+⌈log2 v⌉)b, 1R] + 1 × fp16 add | 768 / 1.65 | 2,093 / 1.93 | 6,121 / 2.92 | 14,631 / 3.51 |

## wq = int2, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int2×int8 mul + v × fp16 add | 2,237 / 6.55 | 3,356 / 9.83 | 3,915 / 11.47 | 4,475 / 13.11 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,945 / 3.40 | 4,783 / 3.79 | 8,432 / 4.11 | 15,812 / 4.63 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,520 / 3.32 | 2,953 / 3.56 | 4,783 / 3.79 | 8,432 / 4.11 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,603 / 3.36 | 3,285 / 3.61 | 5,444 / 3.80 | 9,822 / 4.11 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,348 / 3.30 | 2,207 / 3.47 | 3,285 / 3.61 | 5,444 / 3.80 |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,331* / 3.24* | 1,536 / 3.29 | 1,955 / 3.41 | 2,632 / 3.59 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 2 × fp16 add | 1,331* / 3.24* | 1,331 / 3.24 | 1,536 / 3.29 | 1,955 / 3.41 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,551* / 3.26* | 1,948 / 3.30 | 2,588 / 3.43 | 3,880 / 3.62 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 2R] + 2 × fp16 add | 1,551* / 3.26* | 1,551 / 3.26 | 1,948 / 3.30 | 2,588 / 3.43 |

## wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int3×int8 mul + v × fp16 add | 2,293 / 6.62 | 3,440 / 9.93 | 4,013 / 11.58 | 4,586 / 13.23 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 2,917 / 5.10 | 7,175 / 5.69 | 12,649 / 6.17 | 23,719 / 6.94 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 2,279 / 4.98 | 4,429 / 5.34 | 7,175 / 5.69 | 12,649 / 6.17 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,230 / 5.03 | 4,178 / 5.37 | 6,672 / 5.62 | 11,736 / 5.99 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 1,935 / 4.94 | 2,931 / 5.18 | 4,178 / 5.37 | 6,672 / 5.62 |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,997* / 4.86* | 2,304 / 4.94 | 2,933 / 5.12 | 3,948 / 5.38 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 3 × fp16 add | 1,997* / 4.86* | 1,997 / 4.86 | 2,304 / 4.94 | 2,933 / 5.12 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,335* / 4.91* | 2,951 / 4.96 | 3,914 / 5.17 | 5,867 / 5.44 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 3R] + 3 × fp16 add | 2,335* / 4.91* | 2,335 / 4.91 | 2,951 / 4.96 | 3,914 / 5.17 |

## wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int4×int8 mul + v × fp16 add | 2,360 / 6.65 | 3,540 / 9.98 | 4,130 / 11.65 | 4,720 / 13.31 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,889 / 6.80 | 9,567 / 7.58 | 16,865 / 8.22 | 31,625 / 9.25 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 3,039 / 6.64 | 5,906 / 7.13 | 9,567 / 7.58 | 16,865 / 8.22 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 2,858 / 6.70 | 5,074 / 7.13 | 7,900 / 7.44 | 13,651 / 7.88 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 2,523 / 6.58 | 3,656 / 6.90 | 5,074 / 7.13 | 7,900 / 7.44 |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,662* / 6.48* | 3,072 / 6.59 | 3,910 / 6.82 | 5,264 / 7.17 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 4 × fp16 add | 2,662* / 6.48* | 2,662 / 6.48 | 3,072 / 6.59 | 3,910 / 6.82 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 3,171* / 6.56* | 4,057 / 6.63 | 5,415 / 6.92 | 8,154 / 7.29 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 4R] + 4 × fp16 add | 3,171* / 6.56* | 3,171 / 6.56 | 4,057 / 6.63 | 5,415 / 6.92 |

## wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int6×int8 mul + v × fp16 add | 2,529 / 6.99 | 3,793 / 10.48 | 4,425 / 12.23 | 5,057 / 13.98 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 5,834 / 10.20 | 14,350 / 11.38 | 25,297 / 12.33 | 47,437 / 13.88 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 4,559 / 9.96 | 8,859 / 10.69 | 14,350 / 11.38 | 25,297 / 12.33 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 4,115 / 10.05 | 6,856 / 10.66 | 10,356 / 11.08 | 17,487 / 11.66 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 3,698 / 9.87 | 5,107 / 10.33 | 6,856 / 10.66 | 10,356 / 11.08 |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,993* / 9.72* | 4,609 / 9.88 | 5,866 / 10.24 | 7,895 / 10.76 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 6 × fp16 add | 3,993* / 9.72* | 3,993 / 9.72 | 4,609 / 9.88 | 5,866 / 10.24 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 5,011* / 9.91* | 6,546 / 10.02 | 8,871 / 10.52 | 14,798 / 11.59 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 6R] + 6 × fp16 add | 5,011* / 9.91* | 5,011 / 9.91 | 6,546 / 10.02 | 8,871 / 10.52 |

## wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int8×int8 mul + v × fp16 add | 2,679 / 7.23 | 4,018 / 10.84 | 4,688 / 12.65 | 5,358 / 14.45 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 7,779 / 13.60 | 19,134 / 15.17 | 33,730 / 16.44 | 63,250 / 18.50 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 6,078 / 13.28 | 11,812 / 14.25 | 19,134 / 15.17 | 33,730 / 16.44 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 5,362 / 13.39 | 8,643 / 14.18 | 12,810 / 14.72 | 21,332 / 15.45 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 4,873 / 13.15 | 6,547 / 13.76 | 8,643 / 14.18 | 12,810 / 14.72 |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,324* / 12.96* | 6,145 / 13.17 | 7,821 / 13.65 | 10,527 / 14.35 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 1R] + 8 × fp16 add | 5,324* / 12.96* | 5,324 / 12.96 | 6,145 / 13.17 | 7,821 / 13.65 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 7,052* / 13.31* | 9,378 / 13.47 | 13,297 / 14.33 | 21,901 / 15.83 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × (8+⌈log2 v⌉)b, 8R] + 8 × fp16 add | 7,052* / 13.31* | 7,052 / 13.31 | 9,378 / 13.47 | 13,297 / 14.33 |

## wq = int1, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,103 / 6.18 | 3,155 / 9.27 | 3,681 / 10.81 | 4,206 / 12.36 |
| MAC opt | v × fp16 add | 2,103 / 6.18 | 3,155 / 9.27 | 3,681 / 10.81 | 4,206 / 12.36 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,207 / 1.76 | 3,148 / 1.97 | 5,717 / 2.13 | 10,904 / 2.41 |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 883 / 1.71 | 1,859 / 1.84 | 3,148 / 1.97 | 5,717 / 2.13 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 1,207 / 1.76 | 3,148 / 1.97 | 5,717 / 2.13 | 10,904 / 2.41 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 883 / 1.71 | 1,859 / 1.84 | 3,148 / 1.97 | 5,717 / 2.13 |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 666* / 1.62* | 768 / 1.65 | 978 / 1.71 | 1,316 / 1.79 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 666* / 1.62* | 666 / 1.62 | 768 / 1.65 | 978 / 1.71 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 1R] + 1 × fp16 add | 666* / 1.62* | 768 / 1.65 | 978 / 1.71 | 1,316 / 1.79 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 1R] + 1 × fp16 add | 666* / 1.62* | 666 / 1.62 | 768 / 1.65 | 978 / 1.71 |

## wq = ter, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 add | 2,103 / 6.18 | 3,155 / 9.27 | 3,681 / 10.81 | 4,206 / 12.36 |
| MAC opt | v × fp16 add | 2,103 / 6.18 | 3,155 / 9.27 | 3,681 / 10.81 | 4,206 / 12.36 |
| MAC int8 | v × int16 add | 131 / 0.21 | 197 / 0.32 | 229 / 0.37 | 262 / 0.42 |
| LUT reg dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,717 / 2.13 | 42,002 / 4.14 | — | — |
| LUT reg dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,148 / 1.97 | 21,258 / 3.03 | — | — |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 5,717 / 2.13 | 42,002 / 4.14 | — | — |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 3,148 / 1.97 | 21,258 / 3.03 | — | — |
| LUT SRAM dup, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 978 / 1.71 | 3,306 / 2.21 | 14,631 / 3.51 | 24,370 / 5.04 |
| LUT SRAM dup, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 768 / 1.65 | 2,093 / 1.93 | 6,121 / 2.92 | 14,631 / 3.51 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^⌈log2 3^v⌉ × 16b, 1R] + 1 × fp16 add | 978 / 1.71 | 3,306 / 2.21 | 14,631 / 3.51 | 24,370 / 5.04 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^⌈log2 ⌊3^v/2⌋⌉ × 16b, 1R] + 1 × fp16 add | 768 / 1.65 | 2,093 / 1.93 | 6,121 / 2.92 | 14,631 / 3.51 |

## wq = int2, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int2×fp16 mul + v × fp16 add | 2,266 / 6.64 | 3,399 / 9.97 | 3,965 / 11.63 | 4,532 / 13.29 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 2,415 / 3.52 | 6,296 / 3.94 | 11,435 / 4.27 | 21,809 / 4.81 |
| LUT reg dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,766 / 3.42 | 3,718 / 3.68 | 6,296 / 3.94 | 11,435 / 4.27 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | 1,894 / 3.48 | 4,190 / 3.74 | 7,234 / 3.96 | 13,393 / 4.30 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | 1,503 / 3.42 | 2,668 / 3.58 | 4,190 / 3.74 | 7,234 / 3.96 |
| LUT SRAM dup, pre-ignore | 2 × LUT[2^v × 16b, 1R] + 2 × fp16 add | 1,331* / 3.24* | 1,536 / 3.29 | 1,955 / 3.41 | 2,632 / 3.59 |
| LUT SRAM dup, pre-ignore+symm | 2 × LUT[2^v/2 × 16b, 1R] + 2 × fp16 add | 1,331* / 3.24* | 1,331 / 3.24 | 1,536 / 3.29 | 1,955 / 3.41 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 2R] + 2 × fp16 add | 1,551* / 3.26* | 1,948 / 3.30 | 2,588 / 3.43 | 3,880 / 3.62 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 2R] + 2 × fp16 add | 1,551* / 3.26* | 1,551 / 3.26 | 1,948 / 3.30 | 2,588 / 3.43 |

## wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int3×fp16 mul + v × fp16 add | 2,861 / 8.51 | 4,291 / 12.76 | 5,006 / 14.89 | 5,721 / 17.02 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 3,622 / 5.28 | 9,444 / 5.92 | 17,152 / 6.40 | 32,713 / 7.22 |
| LUT reg dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 2,649 / 5.13 | 5,577 / 5.52 | 9,444 / 5.92 | 17,152 / 6.40 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | 2,578 / 5.22 | 5,233 / 5.57 | 8,751 / 5.86 | 15,884 / 6.28 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | 2,123 / 5.12 | 3,473 / 5.35 | 5,233 / 5.57 | 8,751 / 5.86 |
| LUT SRAM dup, pre-ignore | 3 × LUT[2^v × 16b, 1R] + 3 × fp16 add | 1,997* / 4.86* | 2,304 / 4.94 | 2,933 / 5.12 | 3,948 / 5.38 |
| LUT SRAM dup, pre-ignore+symm | 3 × LUT[2^v/2 × 16b, 1R] + 3 × fp16 add | 1,997* / 4.86* | 1,997 / 4.86 | 2,304 / 4.94 | 2,933 / 5.12 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 3R] + 3 × fp16 add | 2,335* / 4.91* | 2,951 / 4.96 | 3,914 / 5.17 | 5,867 / 5.44 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 3R] + 3 × fp16 add | 2,335* / 4.91* | 2,335 / 4.91 | 2,951 / 4.96 | 3,914 / 5.17 |

## wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int4×fp16 mul + v × fp16 add | 2,997 / 8.82 | 4,495 / 13.22 | 5,244 / 15.43 | 5,994 / 17.63 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 4,830 / 7.04 | 12,592 / 7.89 | 22,870 / 8.54 | 43,618 / 9.63 |
| LUT reg dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 3,532 / 6.85 | 7,436 / 7.35 | 12,592 / 7.89 | 22,870 / 8.54 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | 3,261 / 6.95 | 6,275 / 7.40 | 10,269 / 7.76 | 18,380 / 8.26 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | 2,744 / 6.82 | 4,277 / 7.12 | 6,275 / 7.40 | 10,269 / 7.76 |
| LUT SRAM dup, pre-ignore | 4 × LUT[2^v × 16b, 1R] + 4 × fp16 add | 2,662* / 6.48* | 3,072 / 6.59 | 3,910 / 6.82 | 5,264 / 7.17 |
| LUT SRAM dup, pre-ignore+symm | 4 × LUT[2^v/2 × 16b, 1R] + 4 × fp16 add | 2,662* / 6.48* | 2,662 / 6.48 | 3,072 / 6.59 | 3,910 / 6.82 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 4R] + 4 × fp16 add | 3,171* / 6.56* | 4,057 / 6.63 | 5,415 / 6.92 | 8,154 / 7.29 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 4R] + 4 × fp16 add | 3,171* / 6.56* | 3,171 / 6.56 | 4,057 / 6.63 | 5,415 / 6.92 |

## wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int6×fp16 mul + v × fp16 add | 3,366 / 10.03 | 5,049 / 15.05 | 5,891 / 17.55 | 6,732 / 20.06 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 7,245 / 10.56 | 18,888 / 11.83 | 34,304 / 12.80 | 65,427 / 14.44 |
| LUT reg dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 5,298 / 10.27 | 11,153 / 11.03 | 18,888 / 11.83 | 34,304 / 12.80 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | 4,627 / 10.41 | 8,359 / 11.06 | 13,305 / 11.56 | 23,364 / 12.21 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | 3,984 / 10.23 | 5,886 / 10.66 | 8,359 / 11.06 | 13,305 / 11.56 |
| LUT SRAM dup, pre-ignore | 6 × LUT[2^v × 16b, 1R] + 6 × fp16 add | 3,993* / 9.72* | 4,609 / 9.88 | 5,866 / 10.24 | 7,895 / 10.76 |
| LUT SRAM dup, pre-ignore+symm | 6 × LUT[2^v/2 × 16b, 1R] + 6 × fp16 add | 3,993* / 9.72* | 3,993 / 9.72 | 4,609 / 9.88 | 5,866 / 10.24 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 6R] + 6 × fp16 add | 5,011* / 9.91* | 6,546 / 10.02 | 8,871 / 10.52 | 14,798 / 11.59 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 6R] + 6 × fp16 add | 5,011* / 9.91* | 5,011 / 9.91 | 6,546 / 10.02 | 8,871 / 10.52 |

## wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,694 / 10.47 | 5,541 / 15.70 | 6,465 / 18.32 | 7,389 / 20.94 |
| MAC opt | v × int8×fp16 mul + v × fp16 add | 3,709 / 10.60 | 5,564 / 15.90 | 6,492 / 18.55 | 7,419 / 21.20 |
| MAC int8 | v × int8 mul + v × int16 add | 707 / 1.26 | 1,060 / 1.89 | 1,237 / 2.20 | 1,413 / 2.52 |
| LUT reg dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 9,660 / 14.08 | 25,184 / 15.78 | 45,739 / 17.07 | 87,235 / 19.26 |
| LUT reg dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 7,064 / 13.69 | 14,871 / 14.71 | 25,184 / 15.78 | 45,739 / 17.07 |
| LUT reg multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | 5,994 / 13.87 | 10,444 / 14.72 | 16,340 / 15.37 | 28,345 / 16.17 |
| LUT reg multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | 5,224 / 13.63 | 7,494 / 14.20 | 10,444 / 14.72 | 16,340 / 15.37 |
| LUT SRAM dup, pre-ignore | 8 × LUT[2^v × 16b, 1R] + 8 × fp16 add | 5,324* / 12.96* | 6,145 / 13.17 | 7,821 / 13.65 | 10,527 / 14.35 |
| LUT SRAM dup, pre-ignore+symm | 8 × LUT[2^v/2 × 16b, 1R] + 8 × fp16 add | 5,324* / 12.96* | 5,324 / 12.96 | 6,145 / 13.17 | 7,821 / 13.65 |
| LUT SRAM multi-port, pre-ignore | 1 × LUT[2^v × 16b, 8R] + 8 × fp16 add | 7,052* / 13.31* | 9,378 / 13.47 | 13,297 / 14.33 | 21,901 / 15.83 |
| LUT SRAM multi-port, pre-ignore+symm | 1 × LUT[2^v/2 × 16b, 8R] + 8 × fp16 add | 7,052* / 13.31* | 7,052 / 13.31 | 9,378 / 13.47 | 13,297 / 14.33 |
