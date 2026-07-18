# MISSING_NULL_CHECK Real-World Validation Results

**Pattern:** `MISSING_NULL_CHECK`
**Handler:** `MissingNullCheckHandler`
**Repos scanned:** 1
**Total alerts:** 24
**PASS:** 6 | **SKIP:** 18 | **FAIL:** 0
**Fix rate (PASS/PASS+FAIL):** 6/6 (100%)

## Per-Repo Summary

| Repo | Alerts | PASS | SKIP | FAIL | Fix Rate |
|------|--------|------|------|------|----------|
| `TheAlgorithms/C` | 24 | 6 | 18 | 0 | 100% |

## Per-Instance Detail

| Repo | File | Line | Status | Detail | GCC |
|------|------|------|--------|--------|-----|
| `TheAlgorithms/C` | `octal_to_hexadecimal.c` | 50 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `octal_to_hexadecimal.c` | 53 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `red_black_tree.c` | 23 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `threaded_binary_trees.c` | 78 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `threaded_binary_trees.c` | 302 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `bellman_ford.c` | 25 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `bfs.c` | 116 | **PASS** | Insert NULL check for 'graph' after malloc (enclosing function 'createGraph' returns struct Graph *) | OK |
| `TheAlgorithms/C` | `bfs.c` | 104 | **SKIP** | AST analysis could not confirm the pattern | OK |
| `TheAlgorithms/C` | `dfs.c` | 91 | **PASS** | Insert NULL check for 'graph' after malloc (enclosing function 'createGraph' returns struct Graph *) | OK |
| `TheAlgorithms/C` | `dijkstra.c` | 17 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `floyd_warshall.c` | 17 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `strongly_connected_components.c` | 166 | **PASS** | Insert NULL check for 'graph' after malloc (enclosing function 'createGraph' returns struct Graph *) | OK |
| `TheAlgorithms/C` | `strongly_connected_components.c` | 153 | **SKIP** | AST analysis could not confirm the pattern | OK |
| `TheAlgorithms/C` | `topological_sort.c` | 113 | **PASS** | Insert NULL check for 'graph' after malloc (enclosing function 'createGraph' returns struct Graph *) | OK |
| `TheAlgorithms/C` | `topological_sort.c` | 101 | **SKIP** | AST analysis could not confirm the pattern | OK |
| `TheAlgorithms/C` | `main.c` | 17 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `trie.c` | 28 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `vector.c` | 149 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `vector.c` | 67 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `rselect.c` | 70 | **PASS** | Insert NULL check for 'a' after malloc (enclosing function 'main' returns int) | OK |
| `TheAlgorithms/C` | `qr_decomposition.c` | 35 | **PASS** | Insert NULL check for 'A' after malloc (enclosing function 'main' returns int) | FAIL |
| `TheAlgorithms/C` | `qr_decomposition.c` | 48 | **SKIP** | AST analysis could not confirm the pattern | FAIL |
| `TheAlgorithms/C` | `variance.c` | 12 | **SKIP** | AST analysis could not confirm the pattern | — |
| `TheAlgorithms/C` | `non_preemptive_priority_scheduling.c` | 274 | **SKIP** | AST analysis could not confirm the pattern | — |

## Notes

- **SKIP** is correct behaviour when analyze() returns None: pattern not confirmed in AST, or already fixed.
- Repos were identified via clang-analyzer-unix.Malloc scan.
