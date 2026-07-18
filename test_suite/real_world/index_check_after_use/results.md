# INDEX_CHECK_AFTER_USE Real-World Validation Results

**Pattern:** `INDEX_CHECK_AFTER_USE`
**Handler:** `IndexCheckAfterUseHandler`
**Repos scanned:** 8
**Total alerts:** 108
**PASS:** 102 | **SKIP:** 5 | **FAIL:** 1
**Fix rate (PASS/PASS+FAIL):** 102/103 (99%)

## Per-Repo Summary

| Repo | Alerts | PASS | SKIP | FAIL | Fix Rate |
|------|--------|------|------|------|----------|
| `cesanta/mongoose` | 13 | 13 | 0 | 0 | 100% |
| `radareorg/radare2` | 21 | 19 | 2 | 0 | 100% |
| `vim/vim` | 16 | 15 | 0 | 1 | 93% |
| `netdata/netdata` | 6 | 5 | 1 | 0 | 100% |
| `angstsmurf/spatterlight` | 36 | 36 | 0 | 0 | 100% |
| `sqlite/sqlite (3.42.0)` | 7 | 6 | 1 | 0 | 100% |
| `sqlite/sqlite (3.41.2)` | 8 | 7 | 1 | 0 | 100% |
| `python/cpython (3.13.3)` | 1 | 1 | 0 | 0 | 100% |

## Per-Instance Detail

| Repo | File | Line | Status | Detail | GCC |
|------|------|------|--------|--------|-----|
| `cesanta/mongoose` | `mlan_join.c` | 154 | **PASS** | Swap && operands: move bound check 'i < rate2_size' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `mlan_join.c` | 156 | **PASS** | Swap && operands: move bound check 'j < rate1_size' before array access 'j[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `rtos_wpa_supp_if.c` | 648 | **PASS** | Swap && operands: move bound check 'i < WIFI_SCAN_MAX_NUM_CHAN' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `rtos_wpa_supp_if.c` | 816 | **PASS** | Swap && operands: move bound check 'i < WIFI_SCAN_MAX_NUM_CHAN' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `mlan_api.c` | 5414 | **PASS** | Swap && operands: move bound check 'k < rateIndex' before array access 'k[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `mlan_join.c` | 154 | **PASS** | Swap && operands: move bound check 'i < rate2_size' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `mlan_join.c` | 156 | **PASS** | Swap && operands: move bound check 'j < rate1_size' before array access 'j[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `rtos_wpa_supp_if.c` | 721 | **PASS** | Swap && operands: move bound check 'i < WIFI_SCAN_MAX_NUM_CHAN' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `rtos_wpa_supp_if.c` | 889 | **PASS** | Swap && operands: move bound check 'i < WIFI_SCAN_MAX_NUM_CHAN' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `mlan_join.c` | 154 | **PASS** | Swap && operands: move bound check 'i < rate2_size' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `mlan_join.c` | 156 | **PASS** | Swap && operands: move bound check 'j < rate1_size' before array access 'j[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `rtos_wpa_supp_if.c` | 648 | **PASS** | Swap && operands: move bound check 'i < WIFI_SCAN_MAX_NUM_CHAN' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `cesanta/mongoose` | `rtos_wpa_supp_if.c` | 816 | **PASS** | Swap && operands: move bound check 'i < WIFI_SCAN_MAX_NUM_CHAN' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `aarch64-dis.c` | 1957 | **SKIP** | AST analysis could not confirm the pattern | — |
| `radareorg/radare2` | `m68kass.inc.c` | 1021 | **PASS** | Swap && operands: move bound check 'i < sizeof (instr_upper) - 1' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `hud.c` | 234 | **PASS** | Swap && operands: move bound check 'j < HUD_BUF_SIZE' before array access 'j[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `panels.inc.c` | 6661 | **PASS** | Swap && operands: move bound check 'i < len' before array access 'i[...]' (V781: index used before bound check) | OK |
| `radareorg/radare2` | `rtr.c` | 674 | **PASS** | Swap && operands: move bound check 'rtr_n < RTR_MAX_HOSTS - 1' before array access 'rtr_n[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `debug_bochs.c` | 85 | **PASS** | Swap && operands: move bound check 'i < lenRec - 4' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `debug_bochs.c` | 121 | **PASS** | Swap && operands: move bound check 'i < lenRec -4' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `debug_gdb.c` | 260 | **PASS** | Swap && operands: move bound check 'i < 5' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `apprentice.c` | 1296 | **SKIP** | AST analysis could not confirm the pattern | — |
| `radareorg/radare2` | `softmagic.c` | 1072 | **PASS** | Swap && operands: move bound check '++magindex < nmagic - 1' before array access 'magindex[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `rafind2.c` | 263 | **PASS** | Swap && operands: move bound check 'i < sizeof (_str) - 1' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `uds.c` | 45 | **PASS** | Swap && operands: move bound check '(j != position)' before array access 'j[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `big.c` | 180 | **PASS** | Swap && operands: move bound check 'k < 2 * R_BIG_WORD_SIZE' before array access 'k[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `big.c` | 182 | **PASS** | Swap && operands: move bound check 'z < last_z' before array access 'z[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `print.c` | 776 | **PASS** | Swap && operands: move bound check 'j < (i + 3)' before array access 'j[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `str.c` | 614 | **PASS** | Swap && operands: move bound check 'start < end' before array access 'start[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `str.c` | 1913 | **PASS** | Swap && operands: move bound check 'i < slen' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `str.c` | 2825 | **PASS** | Swap && operands: move bound check '(!left || i < left)' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `libbochs.c` | 160 | **PASS** | Swap && operands: move bound check 'i < lenRec' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `libbochs.c` | 163 | **PASS** | Swap && operands: move bound check 'i < lenRec' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `radareorg/radare2` | `libbochs.c` | 171 | **PASS** | Swap && operands: move bound check 'i < lenRec' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `diff.c` | 389 | **PASS** | Swap && operands: move bound check 'i != idx' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `diff.c` | 509 | **PASS** | Swap && operands: move bound check 'i != idx' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `diff.c` | 3226 | **PASS** | Swap && operands: move bound check 'i != idx' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `diff.c` | 4142 | **PASS** | Swap && operands: move bound check 'eap->arg + i < p' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `diff.c` | 4333 | **PASS** | Swap && operands: move bound check 'i != idx_from' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `diff.c` | 4461 | **PASS** | Swap && operands: move bound check 'i != skip_idx' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `dosinst.c` | 2418 | **PASS** | Swap && operands: move bound check 'i < argc' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `ex_docmd.c` | 9953 | **PASS** | Swap && operands: move bound check '*usedlen > off + 1' before array access 'off[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `ex_getln.c` | 4215 | **PASS** | Swap && operands: move bound check 'spos < ccline.cmdlen' before array access 'spos[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `gui_w32.c` | 4251 | **PASS** | Swap && operands: move bound check 'i < MAXPATHL - 1' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `misc1.c` | 256 | **PASS** | Swap && operands: move bound check 'j <= i' before array access 'j[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `normal.c` | 1434 | **FAIL** | swap target not found in source: 'ptr[col] != NUL && ((i == 0 ? mb_get_class(ptr + col) == this_class\n \t\t\t    : mb_get_class(ptr + col) != 0)\n \t\t    || ((find_type & FIND_EVAL)\n \t\t\t&& col <= (int)startcol\n \t\t\t&& find_is_eval_item(ptr + col, &col, &bn, FORWARD))\n \t\t)' | — |
| `vim/vim` | `search.c` | 2561 | **PASS** | Swap && operands: move bound check '(int)pos.col < comment_col' before array access 'col[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `search.c` | 2574 | **PASS** | Swap && operands: move bound check '(int)pos.col <= comment_col' before array access 'col[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `syntax.c` | 1773 | **PASS** | Swap && operands: move bound check 'current_col != 0' before array access 'current_col[...]' (V781: index used before bound check) | FAIL |
| `vim/vim` | `userfunc.c` | 3700 | **PASS** | Swap && operands: move bound check '(len < 0 || i < len)' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `netdata/netdata` | `sqlite3.c` | 37196 | **PASS** | Swap && operands: move bound check 'ALWAYS(sz>i+4)' before array access 'i[...]' (V781: index used before bound check) | OK |
| `netdata/netdata` | `sqlite3.c` | 156457 | **PASS** | Swap && operands: move bound check 'i!=pTab->iPKey' before array access 'i[...]' (V781: index used before bound check) | OK |
| `netdata/netdata` | `sqlite3.c` | 224284 | **PASS** | Swap && operands: move bound check 'sz>i+4' before array access 'i[...]' (V781: index used before bound check) | OK |
| `netdata/netdata` | `sqlite3.c` | 246653 | **SKIP** | AST analysis could not confirm the pattern | OK |
| `netdata/netdata` | `facets.c` | 90 | **PASS** | Swap && operands: move bound check '*t != id_encoding_characters[0]' before array access 't[...]' (V781: index used before bound check) | FAIL |
| `netdata/netdata` | `websocket-handshake.c` | 349 | **PASS** | Swap && operands: move bound check 'i < MCP_DEV_PREVIEW_API_KEY_LENGTH' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `gamedata.c` | 580 | **PASS** | Swap && operands: move bound check 'i<dp' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 140 | **PASS** | Swap && operands: move bound check 'i<MAXINPUT' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 152 | **PASS** | Swap && operands: move bound check 'i<MAXINPUT' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 1019 | **PASS** | Swap && operands: move bound check 'ip<MAXINPUT' before array access 'ip[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 1294 | **PASS** | Swap && operands: move bound check 'np!=pp' before array access 'np[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `instance.c` | 835 | **PASS** | Swap && operands: move bound check 'i != HERO' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `params.c` | 197 | **PASS** | Swap && operands: move bound check 'i < MAXINSTANCE' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `hecugel.c` | 1538 | **PASS** | Swap && operands: move bound check 'i != guilty_bastards_graphics_win' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 1613 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 1736 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 1743 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 1748 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 1752 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 1900 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 2189 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 2221 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `interpreter.c` | 2302 | **PASS** | Swap && operands: move bound check 'counter < MAX_WORDS' before array access 'counter[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 461 | **PASS** | Swap && operands: move bound check 'index < MAX_WORDS' before array access 'index[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 512 | **PASS** | Swap && operands: move bound check 'index < MAX_WORDS' before array access 'index[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 546 | **PASS** | Swap && operands: move bound check 'index < MAX_WORDS' before array access 'index[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 633 | **PASS** | Swap && operands: move bound check 'index < MAX_WORDS' before array access 'index[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 728 | **PASS** | Swap && operands: move bound check 'wp < MAX_WORDS' before array access 'wp[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 856 | **PASS** | Swap && operands: move bound check 'index < MAX_WORDS' before array access 'index[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 887 | **PASS** | Swap && operands: move bound check 'index < MAX_WORDS' before array access 'index[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 963 | **PASS** | Swap && operands: move bound check 'wp < MAX_WORDS' before array access 'wp[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `loader.c` | 1121 | **PASS** | Swap && operands: move bound check 'wp < MAX_WORDS' before array access 'wp[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 1919 | **PASS** | Swap && operands: move bound check 'index != parent' before array access 'index[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parseinput.c` | 281 | **PASS** | Swap && operands: move bound check 'i < length' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parseinput.c` | 464 | **PASS** | Swap && operands: move bound check 'WordIndex < WordsInInput - 1' before array access 'WordIndex[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 259 | **PASS** | Swap && operands: move bound check 'i < MAX_BUFFER' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 262 | **PASS** | Swap && operands: move bound check 'i + j < MAX_BUFFER' before array access 'j[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 266 | **PASS** | Swap && operands: move bound check 'i + j + k < MAX_BUFFER' before array access 'k[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parser.c` | 583 | **PASS** | Swap && operands: move bound check 'i < length' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `titleimage.c` | 336 | **PASS** | Swap && operands: move bound check 'pos < title_length' before array access 'pos[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `vocab.c` | 5551 | **PASS** | Swap && operands: move bound check 'lpos < listlen' before array access 'lpos[...]' (V781: index used before bound check) | FAIL |
| `angstsmurf/spatterlight` | `parseinput.c` | 62 | **PASS** | Swap && operands: move bound check 'i < length' before array access 'i[...]' (V781: index used before bound check) | FAIL |
| `sqlite/sqlite (3.42.0)` | `sqlite3.c` | 35422 | **PASS** | Swap && operands: move bound check 'ALWAYS(sz>i+4)' before array access 'i[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.42.0)` | `sqlite3.c` | 76178 | **PASS** | Swap && operands: move bound check 'ALWAYS(k<NB*2)' before array access 'k[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.42.0)` | `sqlite3.c` | 76261 | **PASS** | Swap && operands: move bound check 'ALWAYS(k<NB*2)' before array access 'k[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.42.0)` | `sqlite3.c` | 77371 | **PASS** | Swap && operands: move bound check 'ALWAYS(k<NB*2)' before array access 'k[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.42.0)` | `sqlite3.c` | 150037 | **PASS** | Swap && operands: move bound check 'i!=pTab->iPKey' before array access 'i[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.42.0)` | `sqlite3.c` | 213954 | **PASS** | Swap && operands: move bound check 'sz>i+4' before array access 'i[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.42.0)` | `sqlite3.c` | 234678 | **SKIP** | AST analysis could not confirm the pattern | OK |
| `sqlite/sqlite (3.41.2)` | `sqlite3.c` | 34495 | **PASS** | Swap && operands: move bound check 'i<8' before array access 'i[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.41.2)` | `sqlite3.c` | 35168 | **PASS** | Swap && operands: move bound check 'ALWAYS(sz>i+4)' before array access 'i[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.41.2)` | `sqlite3.c` | 75732 | **PASS** | Swap && operands: move bound check 'ALWAYS(k<NB*2)' before array access 'k[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.41.2)` | `sqlite3.c` | 75815 | **PASS** | Swap && operands: move bound check 'ALWAYS(k<NB*2)' before array access 'k[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.41.2)` | `sqlite3.c` | 76917 | **PASS** | Swap && operands: move bound check 'ALWAYS(k<NB*2)' before array access 'k[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.41.2)` | `sqlite3.c` | 149194 | **PASS** | Swap && operands: move bound check 'i!=pTab->iPKey' before array access 'i[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.41.2)` | `sqlite3.c` | 212359 | **PASS** | Swap && operands: move bound check 'sz>i+4' before array access 'i[...]' (V781: index used before bound check) | OK |
| `sqlite/sqlite (3.41.2)` | `sqlite3.c` | 232797 | **SKIP** | AST analysis could not confirm the pattern | OK |
| `python/cpython (3.13.3)` | `lexer.c` | 143 | **PASS** | Swap && operands: move bound check 'i < input_length' before array access 'i[...]' (V781: index used before bound check) | FAIL |

## Notes

- **SKIP** is correct behaviour when analyze() returns None: pattern not confirmed in AST, or already fixed.
- Pattern: array subscript `arr[i]` evaluated before bound check `i < len` in `&&` condition.
- Fix: swap `&&` operands so bound check runs first (short-circuit evaluation).
- Handler is pure text — no libclang TU needed.
- Repos found via grep.app `[i] && i <` filter, Sourcegraph, and already-cloned repos.
- Scanner: `scripts/scan_index_check_after_use.py` (text-based, no libclang).
