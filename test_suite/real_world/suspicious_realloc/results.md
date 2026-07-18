# SUSPICIOUS_REALLOC Real-World Validation Results

**Pattern:** `SUSPICIOUS_REALLOC`
**Handler:** `SuspiciousReallocHandler`
**Repos scanned:** 4
**Total alerts:** 180
**PASS:** 168 | **SKIP:** 12 | **FAIL:** 0
**Fix rate (PASS/PASS+FAIL):** 168/168 (100%)

## Per-Repo Summary

| Repo | Alerts | PASS | SKIP | FAIL | Fix Rate |
|------|--------|------|------|------|----------|
| `orangeduck/mpc` | 33 | 33 | 0 | 0 | 100% |
| `bartp5/libtexprintf` | 48 | 48 | 0 | 0 | 100% |
| `libretro/libretro-prboom` | 4 | 4 | 0 | 0 | 100% |
| `n-t-roff/heirloom-doctools` | 95 | 83 | 12 | 0 | 100% |

## Per-Instance Detail

| Repo | File | Line | Status | Detail | GCC |
|------|------|------|--------|--------|-----|
| `orangeduck/mpc` | `mpc.c` | 309 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 310 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 334 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 335 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 459 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 1522 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 1706 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 1783 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2371 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2374 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2384 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2390 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2399 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2576 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2585 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2613 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 2624 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 3027 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 3034 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 3043 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 3050 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 3522 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 3547 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4001 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4014 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4044 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4045 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4062 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4063 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4094 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4095 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4112 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `orangeduck/mpc` | `mpc.c` | 4113 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `boxes.c` | 49 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `boxes.c` | 490 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `boxes.c` | 491 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `drawbox.c` | 86 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `drawbox.c` | 99 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `drawbox.c` | 105 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 88 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 106 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 559 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 642 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 1052 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 1092 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 1107 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 1201 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2085 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2124 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2181 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2201 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2216 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2233 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2264 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2292 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `lexer.c` | 2303 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `main.c` | 186 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 345 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 379 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 418 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 472 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1127 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1180 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1288 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1360 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1376 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1401 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1430 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1486 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1502 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1527 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 1564 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 2095 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `parser.c` | 2157 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `stringutils.c` | 274 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `stringutils.c` | 438 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `texprintf.c` | 46 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `texprintf.c` | 102 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `texprintf.c` | 145 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `texprintf.c` | 190 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `bartp5/libtexprintf` | `utf2unicode.c` | 79 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `libretro/libretro-prboom` | `rd_util.c` | 38 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `libretro/libretro-prboom` | `fluid_defsfont.c` | 546 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `libretro/libretro-prboom` | `d_server.c` | 397 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `libretro/libretro-prboom` | `d_server.c` | 398 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `checknr.c` | 189 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `input.c` | 529 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `main.c` | 177 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `input.c` | 548 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `main.c` | 220 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `main.c` | 237 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `ptx.c` | 449 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `refer7.c` | 136 | **SKIP** | AST analysis could not confirm the pattern | — |
| `n-t-roff/heirloom-doctools` | `soelim.c` | 121 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | OK |
| `n-t-roff/heirloom-doctools` | `tb.c` | 72 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `tb.c` | 124 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `hnjalloc.c` | 84 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n1.c` | 244 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n1.c` | 1776 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n1.c` | 1849 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n1.c` | 1945 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n1.c` | 2228 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n1.c` | 2305 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n2.c` | 193 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 291 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 1171 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 1183 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 1198 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 1206 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 1804 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 1911 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 1981 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 2285 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 2329 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 2359 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n3.c` | 2372 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n5.c` | 298 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n5.c` | 419 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n5.c` | 973 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n5.c` | 1225 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n5.c` | 1257 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n5.c` | 1261 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n5.c` | 1262 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3189 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3190 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3191 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3192 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3193 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3194 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3195 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3196 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3197 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3198 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3199 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3200 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3201 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3202 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3203 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3204 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3205 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3206 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3207 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3208 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3209 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3279 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n7.c` | 3385 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n8.c` | 540 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 756 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 1117 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 1292 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 1294 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 1295 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 1298 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 1300 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 1302 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `n9.c` | 1305 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `dpost.c` | 1739 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `dpost.c` | 1985 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `dpost.c` | 2231 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `dpost.c` | 4474 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `dpost.c` | 4556 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `makedev.c` | 258 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `otf.c` | 2074 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `otf.c` | 2882 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `otf.c` | 2883 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `otf.c` | 3042 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `otf.c` | 3057 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 144 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 146 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 148 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 150 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 152 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 156 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 158 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 162 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 164 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t10.c` | 166 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t6.c` | 2138 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `n-t-roff/heirloom-doctools` | `t6.c` | 2250 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |
| `n-t-roff/heirloom-doctools` | `t6.c` | 2912 | **PASS** | Wrap realloc in temp pointer to prevent memory leak on failure | FAIL |

## Notes

- **SKIP** is correct behaviour when analyze() returns None: pattern not confirmed in AST, or already fixed.
- Repos identified via Sourcegraph structural search + grep.app cross-check.
