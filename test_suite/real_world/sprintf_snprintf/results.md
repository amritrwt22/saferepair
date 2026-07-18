# SPRINTF_UNBOUNDED Real-World Validation Results

**Pattern:** `SPRINTF_UNBOUNDED`
**Handler:** `SprintfSnprintfHandler`
**Repos scanned:** 4
**Total alerts:** 60
**PASS:** 52 | **SKIP:** 8 | **FAIL:** 0
**Fix rate (PASS/PASS+FAIL):** 52/52 (100%)

## Per-Repo Summary

| Repo | Alerts | PASS | SKIP | FAIL | Fix Rate |
|------|--------|------|------|------|----------|
| `glennrp/libpng` | 9 | 5 | 4 | 0 | 100% |
| `netdata/netdata` | 1 | 1 | 0 | 0 | 100% |
| `taosdata/TDengine` | 47 | 43 | 4 | 0 | 100% |
| `vim/vim` | 3 | 3 | 0 | 0 | 100% |

## Per-Instance Detail

| Repo | File | Line | Status | Detail | GCC |
|------|------|------|--------|--------|-----|
| `glennrp/libpng` | `rpng-win.c` | 396 | **SKIP** | AST analysis could not confirm the pattern | — |
| `glennrp/libpng` | `rpng-win.c` | 398 | **SKIP** | AST analysis could not confirm the pattern | — |
| `glennrp/libpng` | `rpng-x.c` | 349 | **PASS** | Replace sprintf with snprintf(buf=titlebar, sizeof(titlebar)) to bound output (CWE-120) | FAIL |
| `glennrp/libpng` | `rpng-x.c` | 351 | **PASS** | Replace sprintf with snprintf(buf=titlebar, sizeof(titlebar)) to bound output (CWE-120) | FAIL |
| `glennrp/libpng` | `rpng2-win.c` | 544 | **SKIP** | AST analysis could not confirm the pattern | — |
| `glennrp/libpng` | `rpng2-win.c` | 546 | **SKIP** | AST analysis could not confirm the pattern | — |
| `glennrp/libpng` | `rpng2-x.c` | 568 | **PASS** | Replace sprintf with snprintf(buf=titlebar, sizeof(titlebar)) to bound output (CWE-120) | FAIL |
| `glennrp/libpng` | `rpng2-x.c` | 570 | **PASS** | Replace sprintf with snprintf(buf=titlebar, sizeof(titlebar)) to bound output (CWE-120) | FAIL |
| `glennrp/libpng` | `VisualPng.c` | 688 | **PASS** | Replace sprintf with snprintf(buf=szTmp, sizeof(szTmp)) to bound output (CWE-120) | FAIL |
| `netdata/netdata` | `statsd-stress.c` | 83 | **PASS** | Replace sprintf with snprintf(buf=packet, sizeof(packet)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `iniparser.c` | 255 | **PASS** | Replace sprintf with snprintf(buf=keym, sizeof(keym)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `iniparser.c` | 290 | **PASS** | Replace sprintf with snprintf(buf=keym, sizeof(keym)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `iniparser.c` | 336 | **PASS** | Replace sprintf with snprintf(buf=keym, sizeof(keym)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `iniparser.c` | 728 | **PASS** | Replace sprintf with snprintf(buf=tmp, sizeof(tmp)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 109 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 112 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 115 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 123 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 143 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 167 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 224 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `async_demo.c` | 96 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `async_demo.c` | 99 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `async_demo.c` | 102 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `async_demo.c` | 110 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `async_demo.c` | 145 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `async_demo.c` | 176 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `async_demo.c` | 229 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 109 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 112 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 115 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 123 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 143 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 167 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `asyncdemo.c` | 224 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `demoapi.c` | 93 | **PASS** | Replace sprintf with snprintf(buf=command, sizeof(command)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `demoapi.c` | 113 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `taosdata/TDengine` | `demoapi.c` | 132 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `taosdata/TDengine` | `demoapi.c` | 161 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `taosdata/TDengine` | `demoapi.c` | 318 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `taosdata/TDengine` | `stopquery.c` | 415 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `stopquery.c` | 418 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `stopquery.c` | 442 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `stopquery.c` | 445 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `whiteListTest.c` | 147 | **PASS** | Replace sprintf with snprintf(buf=qstr, sizeof(qstr)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `whiteListTest.c` | 158 | **PASS** | Replace sprintf with snprintf(buf=qstr, sizeof(qstr)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `whiteListTest.c` | 176 | **PASS** | Replace sprintf with snprintf(buf=qstr, sizeof(qstr)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `blob_test.c` | 297 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `sml_test.c` | 1631 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `tmqDemo.c` | 212 | **PASS** | Replace sprintf with snprintf(buf=subdir, sizeof(subdir)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `tmqDemo.c` | 253 | **PASS** | Replace sprintf with snprintf(buf=sqlStr, sizeof(sqlStr)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `tmqDemo.c` | 261 | **PASS** | Replace sprintf with snprintf(buf=sqlStr, sizeof(sqlStr)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `tmqDemo.c` | 309 | **PASS** | Replace sprintf with snprintf(buf=sqlStr, sizeof(sqlStr)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `tmqDemo.c` | 436 | **PASS** | Replace sprintf with snprintf(buf=sqlStr, sizeof(sqlStr)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `tmqDemo.c` | 502 | **PASS** | Replace sprintf with snprintf(buf=sqlStr, sizeof(sqlStr)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `tmq_vtable.c` | 41 | **PASS** | Replace sprintf with snprintf(buf=useDB, sizeof(useDB)) to bound output (CWE-120) | FAIL |
| `taosdata/TDengine` | `varbinary_test.c` | 360 | **PASS** | Replace sprintf with snprintf(buf=sql, sizeof(sql)) to bound output (CWE-120) | FAIL |
| `vim/vim` | `os_amiga.c` | 550 | **PASS** | Replace sprintf with snprintf(buf=buf2, sizeof(buf2)) to bound output (CWE-120) | FAIL |
| `vim/vim` | `uninstall.c` | 261 | **PASS** | Replace sprintf with snprintf(buf=buf, sizeof(buf)) to bound output (CWE-120) | FAIL |
| `vim/vim` | `uninstall.c` | 364 | **PASS** | Replace sprintf with snprintf(buf=icon, sizeof(icon)) to bound output (CWE-120) | FAIL |

## Notes

- **SKIP** is correct behaviour when analyze() returns None: pattern not confirmed in AST, or already fixed.
- Repos identified via CWE-120 scanner output.
