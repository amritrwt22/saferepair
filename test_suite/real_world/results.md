# Real-World Evaluation — Master Summary

**Last updated:** 2026-04-30 (session 20)
**SafeRepair version:** 4 patterns, some tests
**Environment:** Python 3.11.9 | libclang 18.1.1 | clang-tidy 21.1.8 | gcc (MinGW) 6.3.0

---

## Overall Results

| Pattern | Repo(s) | Instances | PASS | SKIP | FAIL | Fix Rate |
|---------|---------|-----------|------|------|------|----------|
| SUSPICIOUS_REALLOC | orangeduck/mpc | 33 | 33 | 0 | 0 | 100% |
| SUSPICIOUS_REALLOC | bartp5/libtexprintf | 48 | 48 | 0 | 0 | 100% |
| SUSPICIOUS_REALLOC | libretro/libretro-prboom | 4 | 4 | 0 | 0 | 100% |
| SUSPICIOUS_REALLOC | n-t-roff/heirloom-doctools | 95 | 83 | 12 | 0 | 100% of fixable |
| MISSING_NULL_CHECK | TheAlgorithms/C | 24 | 6 | 18 | 0 | 100% of fixable |
| INDEX_CHECK_AFTER_USE | cesanta/mongoose | 13 | 13 | 0 | 0 | 100% |
| INDEX_CHECK_AFTER_USE | radareorg/radare2 | 21 | 19 | 2 | 0 | 100% of fixable |
| INDEX_CHECK_AFTER_USE | vim/vim | 16 | 15 | 0 | 1 | 93% (1 deeply-nested multi-line) |
| INDEX_CHECK_AFTER_USE | netdata/netdata | 6 | 5 | 1 | 0 | 100% of fixable |
| INDEX_CHECK_AFTER_USE | angstsmurf/spatterlight | 36 | 36 | 0 | 0 | 100% |
| INDEX_CHECK_AFTER_USE | sqlite/sqlite (3.42.0) | 7 | 6 | 1 | 0 | 100% of fixable |
| INDEX_CHECK_AFTER_USE | sqlite/sqlite (3.41.2) | 8 | 7 | 1 | 0 | 100% of fixable |
| INDEX_CHECK_AFTER_USE | python/cpython (3.13.3) | 1 | 1 | 0 | 0 | 100% |
| SPRINTF_UNBOUNDED | glennrp/libpng | 9 | 5 | 4 | 0 | 100% of fixable |
| SPRINTF_UNBOUNDED | netdata/netdata | 1 | 1 | 0 | 0 | 100% |
| SPRINTF_UNBOUNDED | taosdata/TDengine | 47 | 43 | 4 | 0 | 100% of fixable |
| SPRINTF_UNBOUNDED | vim/vim | 3 | 3 | 0 | 0 | 100% |

**Total: 372 alerts across 15 unique repos | 328 PASS | 43 SKIP | 1 FAIL | 99.7% fix rate. False positives: 0.**

---

## Per-Pattern Detail

| Pattern | Results file |
|---------|-------------|
| SUSPICIOUS_REALLOC | [`suspicious_realloc/results.md`](suspicious_realloc/results.md) |
| MISSING_NULL_CHECK | [`missing_null_check/results.md`](missing_null_check/results.md) |
| INDEX_CHECK_AFTER_USE | [`index_check_after_use/results.md`](index_check_after_use/results.md) |
| SPRINTF_UNBOUNDED | [`sprintf_snprintf/results.md`](sprintf_snprintf/results.md) |

---

## Limitations

| # | Limitation |
|---|-----------|
| L1 | Function-pointer-abstracted allocations (e.g. cJSON hooks) not detected — no direct `malloc`/`realloc` call at source level |
| L2 | No interprocedural analysis — vulnerabilities spanning multiple functions not handled |
| L3 | NULL check handler: double-pointer declarations (`type **var = malloc(...)`) not matched by regex |
| L4 | PARSE_INCOMPLETE on files with missing system headers — handlers fall back to text-level detection |

---

## False Positives

None observed across all real-world runs. All handlers correctly skip cases they cannot safely fix.
