# SafeRepair — Interview Study Notes (Master Doc)

> Source of truth used for this doc: the final project report (`docs/project_report/chapters/*.tex`) and the actual pipeline code in `saferepair-repo/saferepair/`. Numbers here are verified against `ch4_results.tex` — this supersedes any different numbers in your older `SafeRepair Study Guide.md` / `Code Structure Study.md` (those had a stale "17 repos / 354 alerts" draft figure floating around).
>
> **⚠️ One thing only you can fill in:** every git commit in the repo is under a teammate's name, and you mentioned the code itself was AI-assisted. That's fine and increasingly normal — but it means I cannot write your "Action" section for you. Wherever you see `[PERSONALIZE: ...]` below, replace it with what *you* actually drove: pattern selection? the verification methodology? running the 15-repo evaluation? the report/results analysis? Don't skip this — it's the part of STAR an interviewer will drill into hardest, and it's the one part I have no way to know.

---

## Part 0 — The 20-Second Cold Open

Use this when someone says "walk me through a project on your resume":

> "SafeRepair is an automated program repair tool for C. You give it a source file and a list of static-analysis alerts, and for four specific memory-safety bug patterns, it parses the AST with libclang, confirms the bug is real, and writes a deterministic fix — no LLM, no training data. We ran it on 372 real alerts across 15 open-source C projects like vim, sqlite, and cpython, and it correctly repaired 328 of 329 confirmed vulnerabilities with zero false positives."

Memorize this cold. Everything else is elaboration on demand.

---

## Part 1 — Full STAR Narrative (~90 seconds)

**Situation.**
Static analysis tools like clang-tidy are good at *detecting* memory-safety bugs in C at scale — buffer overflows, null derefs, leaks. But detection isn't the bottleneck. Every alert still needs a human to read it and hand-write a fix. On a real codebase with dozens of instances of the same bug class, that turns into repetitive manual work, and known, flagged vulnerabilities sit unpatched for months simply because nobody's gotten to them.

**Task.**
For our B.Tech project at DTU, we set out to close that gap: build a tool that goes from "static analyzer alert" to "verified safe patch" with zero human involvement — but specifically *without* the failure modes that make people distrust automated patching (silent false positives, semantically-wrong rewrites, non-determinism).

**Action.**
`[PERSONALIZE: your specific slice — e.g. "I drove the pattern-selection methodology and the real-world evaluation" / "I designed and ran the verification pipeline that decided which 4 bug patterns were worth building handlers for" / "I owned the results analysis and wrote the report" — say what's true.]`

The design decisions that make the project defensible:
- **Right-or-silent architecture.** Every handler either confirms the vulnerability directly in the AST and emits a fix, or returns nothing and leaves the file byte-for-byte untouched. There's no partial or best-guess patch — that's *the* thing that gives a zero-false-positive guarantee by construction, not by luck.
- **AST-based, not regex-based.** We use libclang — the same parser Clang itself uses — so a handler can, e.g., confirm a `realloc` call actually exists as a `CALL_EXPR` node at that line (not inside a comment or a macro), or look up the enclosing function's real return type to generate a correctly-typed `return` statement after a null-check insertion.
- **We scoped deliberately narrow.** Only 4 CWE patterns, chosen specifically because the correct fix is *mechanically unambiguous* given local context — not "pick a plausible patch," but "there is exactly one correct rewrite."
- **Independent compiler validation.** Every patch is run through `gcc -fsyntax-only` before being written — a safety net independent of the tool's own reasoning.
- **Rigorous pattern selection, not vibes.** Before writing a handler, we ran a 4-stage verification process (pre-screen against existing tools → breadth search → libclang-confirmed depth search → only proceed if ≥5 real unfixed instances exist). We actually burned time on this the hard way once — chose a well-known pattern (memset/sizeof misuse), scanned 13 major repos, and found **zero** unfixed real instances, because every serious project had already patched it. That's what taught us to verify a pattern is real *and currently unfixed* before investing in a handler, instead of picking patterns that sound impressive.

**Result.**
Evaluated on 15 real open-source C repositories (vim, sqlite, cpython, radare2, TDengine, netdata, libpng, and others) with **no repo-specific tuning**: 372 alerts processed, **328 of 329 confirmed vulnerabilities repaired (99.7%)**, and **zero false positives** — the 43 skips all left source files unchanged rather than risk a wrong patch, and the single failure (a multi-line ternary condition in vim) was a known, explainable text-matching edge case, not a wrong patch. We wrote this up as a full project report positioning it against prior APR literature (GenProg, TBar, Prophet, VulRepair, VulMaster, and the closest comparable, Redemption from CMU/SEI).

---

## Part 1b — The Pitch, Broken Into Points (study this, don't just read the paragraph)

The flowing paragraph in Part 1 is the *script*. This is the *outline* — study this form first, so you're reconstructing the story from its logical skeleton rather than reciting memorized sentences. If you go blank mid-interview, this is what you fall back to. Rough timing included so you can self-pace to 2–3 minutes; cut deepest-nested sub-points first if you're running long, never cut a top-level point.

### SITUATION — the problem (~30–40 sec)
- C still runs the critical stuff — OS kernels, databases, network daemons, embedded firmware — because direct memory access is fast and gives low-level control.
  - That same direct access is exactly what creates the bug class: buffer overflows, null-pointer derefs, bad reallocs.
- These bugs have been exploited for decades, and defenses like ASLR/DEP/stack canaries only slow attackers down — they get routed around, they don't remove the underlying bug.
- The detection side is basically solved: tools like clang-tidy can flag these patterns reliably across huge codebases.
- The repair side is not solved: every single alert still needs a human to read it and hand-write a fix.
- In practice that means the same fix gets applied over and over across a project, and known, already-flagged bugs sit unpatched for months simply because nobody's gotten to them yet.

### TASK — what we set out to do (~20–30 sec)
- Close the gap between "alert" and "verified safe patch" — with zero human involvement in the loop.
- Self-imposed constraints, on purpose: no LLM, no training data, no GPU.
- The non-negotiable one: it must never introduce a false positive. A silently wrong patch is worse than no patch at all — especially in a world where this could land in a CI pipeline before any human reviews it.
- `[PERSONALIZE: one line on your specific slice of this task — e.g. "my piece of this was deciding which bug patterns were even worth targeting" / "mine was running the real-world evaluation and making sense of the results."]`

### ACTION — what we actually built (~45–60 sec, the meat of the pitch)
- Built SafeRepair: a rule-based automated program repair (APR) tool targeting 4 specific CWE patterns.
  - Chosen deliberately narrow — each one has exactly one mechanically correct fix, no guessing at developer intent required.
- Core design principle — **right-or-silent**: every handler either confirms the bug directly in the AST and emits a deterministic fix, or returns nothing and leaves the file byte-for-byte untouched.
  - No partial fixes, no best-guess patches — that's the one design choice the whole zero-false-positive result comes from.
- AST-based, not regex-based: uses libclang (the same parser Clang itself uses) so a handler can confirm, e.g., that a flagged `realloc` call is a real function call in real code — not sitting inside a comment or a macro — and can read the enclosing function's actual return type to generate a correctly-typed fix.
- Every patch also runs through `gcc -fsyntax-only` before being written — an independent safety net on top of the AST-level reasoning.
- Before writing any handler, ran a real verification process to confirm each pattern was still genuinely unfixed in live code — not just picking a CWE because it sounded impressive.
  - (Optional if there's time/interest: the one time we skipped this discipline — picked a well-known pattern, scanned 13 major repos, found zero real unfixed instances because it was already handled everywhere — that's what forced the rigor into the process.)
- `[PERSONALIZE: the concrete thing you personally did here.]`

### RESULT — what it produced (~20–30 sec)
- Evaluated on 15 real open-source C repositories — vim, sqlite, cpython, radare2, TDengine, netdata, libpng, and others — deliberately with no repo-specific tuning.
- 372 real alerts processed.
- 328 of 329 confirmed vulnerabilities correctly repaired — 99.7%.
- Zero false positives: the 43 skips all left source files unchanged rather than risk a wrong patch; the single failure was a known, explainable text-matching edge case in vim, not a wrong patch.
- Wrote the whole thing up as a formal project report positioned against prior automated-program-repair literature.

---

## Part 2 — The First 5 Follow-Ups (rapid fire, have these instant)

**"What does 99.7% mean exactly — repaired out of what?"**
> Of 372 total alerts, 43 were safely skipped (not failures — a skip means "couldn't confirm, so did nothing"), leaving 329 confirmed vulnerabilities. 328 of those 329 were correctly repaired = 99.7%. If you count skips as non-repairs (the conservative, honest framing), the overall rate is 88.2%. I lead with 99.7% because it's the accuracy *on cases the tool actually acted on* — the metric that matters for "when it acts, is it right."

**"Zero false positives — how do you know that's not just because it didn't do much?"**
> It's the flip side of the same design: the tool did act on 328 cases, all verifiable and gcc-validated, and it explicitly declined on 43 more where it couldn't confirm the pattern. Zero false positives isn't "the tool was cautious to the point of uselessness" — it repaired 88% of everything it saw. It's zero false positives *with* a high fix rate, which is the actual hard part.

**"What's the one failure?"**
> vim, INDEX_CHECK pattern. The loop condition spanned multiple lines with nested ternary operators, and the text-level `&&`-operand search didn't correctly span the indentation/newline variation. It's a text-matching limitation, not a logic error — future work item is doing the operand swap at the AST/token level via libclang instead of text search, which would fix this class entirely.

**"Why not just use an LLM to generate the fix?"**
> LLMs are probabilistic — for a fix that lands in a CI pipeline before human review, "probably right" isn't good enough, and you can't audit *why* a specific token sequence was generated. Rule-based repair gives a correctness argument you can read in under a minute: this fix is right because the C standard guarantees X. It's also literally microseconds per patch vs. an inference call, and needs no training data or GPU.

**"Is this really 'AI' or automated program repair — did you use AI to build it?"**
> `[Be straightforward here — see Part 10 below for exact framing.]` Short version: yes, I used AI-assisted tooling to help implement it, the same way most engineers do in 2026 — but the design decisions (which 4 patterns, the right-or-silent principle, the verification methodology, what counts as "confirmed") were the actual project, and that's what I can defend in depth.

---

## Part 3 — Architecture Deep Dive

**The pipeline (6 modules, one job each):**

```
alerts.json + source dir
      │
      ▼
alert_parser.py       — JSON → Alert objects (resolves file paths, drops malformed entries)
      │
      ▼
pattern_detector.py   — rule_id → RepairPattern enum (maps clang-tidy / custom-scanner /
      │                  Clang-static-analyzer rule names for the SAME bug to ONE pattern)
      ▼
ast_analyzer.py        — libclang parses the file into a TranslationUnit (one Index,
      │                  reused across the whole run)
      ▼
pipeline.py            — groups alerts by file, parses AST once per file, dispatches
      │                  each alert to its handler
      ▼
handlers/*.py           — analyze(alert, tu) → context dict or None
      │                   generate_fix(alert, context, rewriter) → queues an edit
      ▼
source_rewriter.py      — applies ALL queued edits to an in-memory line buffer at once
      │                  (so multiple fixes to one file don't shift each other's line numbers)
      ▼
validator.py            — gcc -fsyntax-only on the patched file → PASS / FAIL
      ▼
Output: patched .c file, PASS/SKIP/FAIL per alert
```

**Why "parse the AST once per file, not once per alert":** cost stays fixed regardless of how many alerts land in the same file — you're not re-parsing a 250k-line file 40 times because it has 40 alerts.

**The right-or-silent principle** (this is the single most important idea to be able to explain unprompted):
Every handler does exactly one of two things — confirm the pattern via AST and produce a fix, or return `None` and touch nothing. There is no third path (no "best effort" patch, no partial fix). This is *why* zero false positives is a structural guarantee, not an empirical accident of this one evaluation run — a future run on a different codebase would have the same guarantee, because it comes from the architecture, not from getting lucky on these 15 repos.

**Two-phase handler contract**, shared by all four handlers:
- `analyze(alert, tu)` — regex-matches the source line first (cheap), *then* confirms against the actual libclang AST (e.g., "does a CALL_EXPR named `realloc` really exist at this line, not inside a comment/macro"). Read-only, no side effects. Returns `None` on any failed precondition.
- `generate_fix(alert, context, rewriter)` — builds the replacement text using only what `analyze()` already confirmed, queues it via `rewriter.replace_line()` / `insert_after_line()`.

---

## Part 4 — The Four Bug Patterns (know each cold)

| # | CWE | Pattern | Fix | Alerts | PASS | SKIP | FAIL | Rate (confirmed) |
|---|-----|---------|-----|-------:|-----:|-----:|-----:|------:|
| 1 | CWE-401/690 | Suspicious `realloc` self-assignment | Route through temp pointer, only reassign on success | 180 | 168 | 12 | 0 | 100% |
| 2 | CWE-690 | Missing NULL check after `malloc` | Insert type-correct guard (`return NULL;` / `return -1;` / `return;`) | 24 | 6 | 18 | 0 | 100% |
| 3 | CWE-125/787 (PVS V781) | Index-before-bounds-check in loop condition | Swap `&&` operands so bounds check runs first | 108 | 102 | 5 | 1 | 99% |
| 4 | CWE-120 | Unbounded `sprintf` with `%s` | Replace with `snprintf` + insert `sizeof(buf)` | 60 | 52 | 8 | 0 | 100% |
| | | **Total** | | **372** | **328** | **43** | **1** | **99.7%** |

*(Overall rate treating skips as non-repairs: 88.2% — the conservative number, use it if asked "including everything.")*

### 1. Suspicious Realloc (CWE-401/690)
- **Bug:** `p = realloc(p, size)` — if `realloc` fails it returns `NULL`, which overwrites `p`. The original allocation is now unreachable (leaked) *and* your only pointer to it is gone.
- **Detection:** clang-tidy's `bugprone-suspicious-realloc-usage`. Handler regex-matches plain (`p = realloc(p, ...)`) and struct-member (`s->f = realloc(s->f, ...)`) forms, tolerates an optional cast, then confirms a real `realloc` `CALL_EXPR` exists at that AST line.
- **Fix:**
  ```c
  /* before */
  i->marks = realloc(i->marks, sizeof(mpc_state_t) * i->marks_slots);
  /* after */
  {
    void *_sr_tmp = realloc(i->marks, sizeof(mpc_state_t) * i->marks_slots);
    if (_sr_tmp != NULL) { i->marks = _sr_tmp; }
    /* else: realloc failed, i->marks still valid */
  }
  ```
- **Why it's provably correct:** the C standard guarantees `realloc` leaves the original pointer untouched on failure. On success the reassignment is identical to the original code; on failure the original pointer survives. Nothing about this depends on the surrounding program's intent.

### 2. Missing NULL Check (CWE-690)
- **Bug:** dereferencing `malloc`'s return value without checking for `NULL` first → undefined behavior (null deref) if allocation fails.
- **Detection:** clang-tidy `clang-analyzer-unix.Malloc` + custom CWE-690 scanner. Handler checks the next 3 lines for any of 6 existing null-check phrasings (skips if already guarded — avoids double-inserting), then calls `find_enclosing_function` to read the containing function's return type.
- **Fix:** inserts a guard using the *correct* return value for that function — `return NULL;` for pointer-returning functions, `return -1;` for int-returning, bare `return;` for void.
- **Why the skip rate is high (75%):** when the enclosing function returns something outside those 3 shapes (e.g. a struct by value), there's no safe universal sentinel to return, so the handler correctly declines rather than guessing. This is the best "shows you understand the tool's own boundaries" example.

### 3. Index Check After Use / V781 (CWE-125/787)
- **Bug:** `for (j = 0; p[j] && j < N; j++)` — evaluates the array access *before* the bounds check due to left-to-right `&&` evaluation. When `j == N`, `p[j]` is an out-of-bounds read that happens *before* the very check meant to prevent it.
- **Detection:** custom libclang scanner (this is the PVS-Studio V781 pattern). Handler reads up to 10 lines to join multi-line conditions, splits at *top-level* `&&` (not nested in parens/brackets), checks left has array subscript + right has a bound check on the same index var. Skips if the left side has a side effect (`++`/`--`) — swapping would change loop semantics.
- **Fix:** swap the operands: `for (j = 0; j < N && p[j]; j++)`.
- **Why correct:** `&&` is commutative for truth values on side-effect-free operands, and short-circuit evaluation now protects the array access instead of exposing it.
- **This is where the one FAIL happened** (vim: nested ternaries + multi-line spanning broke the text-level operand extraction — not a logic bug, a text-matching reach limit).

### 4. Sprintf Unbounded (CWE-120)
- **Bug:** `sprintf(buf, fmt, ...)` with a `%s` and a runtime string arg has no bound — if the formatted output exceeds `buf`'s capacity, it overflows.
- **Detection:** custom scanner + clang-tidy's `clang-analyzer-security.insecureAPI.DeprecatedOrUnsafeBufferHandling`. Skips immediately if `snprintf` already present. Extracts buffer name via regex, confirms a real `sprintf` `CALL_EXPR` exists at that line.
- **Fix:** `sprintf(keym, "%s:", s);` → `snprintf(keym, sizeof(keym), "%s:", s);`
- **Why the skips happen (dynamically-sized buffers, libpng + TDengine):** if the destination is a heap pointer rather than a stack array, `sizeof(buf)` would return the *pointer width* (8 bytes), not the real buffer size — so the fix would be actively wrong. The handler checks the AST type of the buffer argument and declines if it's a pointer. This is a great "know your tool's limits" answer.

---

## Part 5 — How the 4 Patterns Were Chosen (great "process/rigor" story)

Don't undersell this — "how did you decide what to build" is a real signal of engineering maturity, and you have a genuinely good answer with a real mistake-and-correction in it.

**The 4-stage verification methodology**, applied before writing any handler:
1. **Stage 0 — Pre-screen.** Reject any candidate pattern already covered by PVS-Studio, clang-tidy's free checks, or default GCC/Clang warnings — if it's already caught, every maintained repo has already fixed it, and you'll get zero real instances no matter how many repos you scan.
2. **Stage 1 — Breadth search.** Sourcegraph structural search + grep.app + Semgrep registry to find candidate repos where the pattern might still exist unfixed.
3. **Stage 2 — Depth verify.** Actually clone candidates and run a libclang AST scan with `TypeKind`-level checks (not just text matching) to confirm real, currently-unfixed instances.
4. **Stage 3 — Verdict.** ≥5 confirmed instances → build the handler. <2 → the pattern is too rare/extinct, pick a different one.

**The lesson that makes this credible:** the team's first candidate pattern was `memset(ptr, 0, sizeof(ptr))` misuse (V512) — a well-known, named PVS-Studio pattern. Skipped Stage 0. Cloned 13 major repos (openssl, postgres, FFmpeg, curl, redis, vim, netdata, libpng, the Linux kernel, etc.), found 2,221 *textual* candidates, and confirmed **zero** real unfixed instances via libclang — every single one turned out to be a stack array (`sizeof(arr)` is correct there), because every serious maintained C project had already fixed this exact pattern years ago. That's what forced the pre-screening stage into the process: **pick patterns real tools don't already catch**, not patterns that sound impressive by name.

> Good line to say out loud: *"We actually burned a full scan cycle on a pattern that turned out to be extinct in maintained code — that's what taught us to verify a pattern is both real and currently unfixed before investing engineering time in a handler for it."*

---

## Part 6 — Objection Handling (pre-empt these, don't wait to be asked)

**"Static analyzers have false positives — isn't auto-fixing them dangerous?"**
> Agreed in the general case — that's exactly why SafeRepair never trusts the alert alone. `analyze()` independently re-confirms the bug in the AST before any patch is generated. 43 of 372 alerts were correctly skipped this way. Zero false-positive *patches* across all 372.

**"The correct fix often depends on developer intent — how do you avoid guessing wrong?"**
> That's true for arbitrary bugs, which is exactly why we scoped to only 4 patterns where the fix is *mechanically unambiguous* regardless of intent — nobody ever intends a buffer overflow or a leaked realloc pointer, so there's no competing "valid" interpretation to guess between.

**"Couldn't a rewrite silently change program behavior?"**
> Two independent safeguards: (1) it's AST-based, not text-based — the tool reasons about real program structure, e.g. reading the enclosing function's actual return type rather than guessing; (2) every patch is compiled with `gcc -fsyntax-only` as an independent check before being written to disk.

**"Why not just rely on runtime sanitizers (ASan, Valgrind)?"**
> Different layer, not a replacement. Sanitizers catch input-specific bugs at runtime but only for the inputs you actually exercise, at real overhead cost. Static analysis + APR catches the mechanically-fixable subset of *pattern-based* bugs across all code paths, cheaply, before the code ever runs. The realistic picture is a defense-in-depth stack: static analysis → APR for the mechanical subset → sanitizers → human review for anything requiring judgment. This is the same layered model shops like NVIDIA already run internally (Coverity + ASan/Compute Sanitizer + human review).

---

## Part 7 — Positioning Against Prior Work (condensed table — know the 2-3 closest ones well, others just by name)

| Work | Approach | Headline number | Key contrast with SafeRepair |
|---|---|---|---|
| **Redemption** (Svoboda et al., CMU/SEI 2025) | Rule-based, AST-guided, C/C++ | 94.4% repair/dismiss on one analyzer/codebase | **Closest prior work.** Redemption *will* patch a probable false positive if the cost of being wrong seems low (e.g. a superfluous null check). SafeRepair refuses unless the AST confirms — different risk posture, different target use case (human-reviewed vs. fully automated CI). |
| **VulRepair** (Fu et al., 2022) | Fine-tuned T5, learned from CVE patches | 43.7% exact match | Learned, no AST awareness, needs GPU + training data, non-deterministic. Generalizes to more bug types, but most patches are still wrong. |
| **VulMaster** (Zhou et al., 2024) | Transformer + AST encoding + CWE labels | 20.3% exact match on 5,800 functions | Better context handling than VulRepair, still probabilistic, 4/5 patches wrong. |
| **GenProg** (Le Goues et al., 2012) | Genetic programming, test-suite-scored mutations | 55/105 real bugs, ~$8/repair | Needs a test suite that actually *triggers* the bug — rare for memory-safety bugs in production code. Non-deterministic. |
| **TBar** (Liu et al., 2019) | Template patterns, Java, Defects4J | 43–74 bugs depending on fault localization | Java only; bottlenecked by fault localization, not the patterns themselves. |
| **Prophet** (Long & Rinard, 2016) | Learned ranking over generate-and-validate candidates | 15/69 real bugs | Needs a historical human-patch corpus; still test-suite-bound. |

**The one-sentence differentiator to say out loud:**
> "ML-based APR treats repair as sequence-to-sequence translation — it generalizes further but is probabilistic, so it can produce syntactically valid but semantically wrong patches. SafeRepair is deterministic by design: given a confirmed pattern, there's exactly one output, and that's what makes a zero-false-positive guarantee possible at all. The tradeoff is scope — 4 patterns, not arbitrary CWEs — but on those 4, the ceiling isn't ~20-45%, it's 99.7%."

---

## Part 8 — Limitations & Future Work (own these before they're asked)

Naming your own boundaries unprompted reads as engineering maturity, not weakness.

| Limitation | Why it happens | What would fix it |
|---|---|---|
| **Macro-expanded pointers** (12 skips, all heirloom-doctools) | Realloc pointer passes through a preprocessor macro; regex can't match the unexpanded source text | Resolve macro tokens via libclang's token-expansion API before rewriting |
| **Return-type ambiguity** (18/24 MISSING_NULL skips) | Function returns a struct or non-standard error code that doesn't map to any of the 3 supported sentinels | Would need interprocedural analysis / doc lookup — acknowledged as a *hard* limit, not just unimplemented |
| **Dynamically-sized buffers** (8 SPRINTF skips) | Destination is heap-allocated; `sizeof(ptr)` would return pointer width, not real size | Needs pointer-provenance analysis to recover allocation size — also a hard limit, beyond local AST inspection |
| **The one FAIL** (vim, INDEX_CHECK) | Multi-line condition with nested ternaries broke text-level operand extraction | AST-level (not text-level) operand swap via `get_tokens()` |
| **No interprocedural analysis at all** | Every handler reasons within one function body only | A lightweight same-file interprocedural pass would extend the detection boundary |
| **Only 4 patterns / C only** | Deliberate scope choice for the evaluation | CWE-476, CWE-415, CWE-190 have similar local structural signatures and need *no pipeline changes*, just new handlers. libclang already parses C++ natively — extension is mostly about reference-type/RAII-aware pattern detectors. |

**"What would you do differently with more time?"** — good answer: pick one of the above (AST-level operand swap for INDEX_CHECK is the cleanest, since it fixes the one FAIL *and* reduces macro-expansion skips) and go deep on it, rather than a vague "add more patterns."

---

## Part 9 — Interview-Framing Questions Beyond the Academic Viva

These are the kind of questions a SWE interviewer (not a thesis committee) is more likely to ask — practice these specifically, since your existing notes were written for a professor, not a hiring panel.

**"How would you productionize this — e.g. as a CI/CD step?"**
> Package it as a GitHub Actions step (or equivalent in an internal CI system): run the static analyzer, feed alerts.json into SafeRepair, and auto-open a PR for every PASS result with the patch + a diff + which rule triggered it, for human merge approval. SKIPs and FAILs get surfaced as-is for manual triage — nothing silently disappears.

**"What's the biggest technical risk in scaling this to a much larger codebase, or to C++?"**
> Two things: (1) interprocedural cases — right now everything is single-function scope, so a much larger codebase will surface more of the "vulnerability confirmable only by tracing across a call boundary" category, which currently just gets skipped; (2) libclang parses C++ natively, but pattern detectors would need updating for reference types and RAII patterns — a `realloc`-style handler doesn't map cleanly onto smart-pointer idioms, for example.

**"How does this connect to the compiler/dev-tools work you did at NVIDIA?"**
> Both are about building *deterministic, trustworthy automation on top of a verification signal* rather than building a black box: SafeRepair turns a static-analysis alert into a verified patch instead of a person doing it by hand; the NVIDIA local-reproduction framework turned a failed remote GPU regression into an instantly-reproducible local environment instead of someone manually chasing down artifacts. The common thread is caring about what a tool is confidently *allowed* to automate vs. where it should hand control back to a human — same reasoning that produced the right-or-silent design here.
> `[This is a genuinely strong bridge — use it if you get "why does this project matter to you / how does it relate to the role."]`

**"Is this actually novel, or re-implementing known ideas?"**
> The individual ideas (AST-guided rule-based repair) aren't new — Redemption (CMU/SEI, 2025) does the same class of thing. What's specific here: a stricter right-or-silent policy than Redemption's (which will patch probable-false-positives when cost is low), a documented pattern-selection methodology instead of picking well-known CWEs by name, and a real-world evaluation across 15 genuinely diverse codebases with no per-repo tuning. It's a rigorous, well-evaluated instance of an existing idea family, not a brand-new algorithm — and that's a fine, honest thing to say.

---

## Part 10 — If Asked About AI-Assisted Development

This is a completely normal question in 2026 and being straightforward about it lands far better than dodging.

> "I used AI-assisted tooling heavily for implementation — that's standard practice at this point. What I can walk you through in depth is the actual engineering: why these 4 patterns and not others, why the right-or-silent architecture rather than a best-effort one, how we verified patterns were real before building handlers for them, and what the evaluation results mean and don't mean. That's the part that required judgment, and it's what I'd defend in a design review."

Don't over-apologize for it, don't over-claim "I wrote every line" either — both read as evasive. State it plainly once, then move straight back to substance.

---

## Part 11 — One-Page Cheat Sheet (memorize this table)

**Numbers:**
- 15 repos, 372 alerts, 328 PASS, 43 SKIP, 1 FAIL
- 99.7% of confirmed (329) repaired · 88.2% overall (conservative, skips = non-repair)
- 0 false positives, 0 wrong patches, 0 broken compiles

**4 patterns → fix:**
- Suspicious realloc → temp-pointer pattern (180 alerts, 100%)
- Missing NULL after malloc → typed guard insert (24 alerts, 100% of confirmed, but 75% skip rate — struct-return ambiguity)
- Index-before-bounds (V781) → swap `&&` operands (108 alerts, 99% — the 1 FAIL is here)
- Unbounded sprintf → snprintf + sizeof (60 alerts, 100% of confirmed, skips = heap-buffer cases)

**6 modules:** alert_parser → pattern_detector → ast_analyzer → pipeline (dispatcher) → source_rewriter → validator

**Core principle:** right-or-silent — confirm-and-fix or return None, never a best-effort patch.

**Closest prior work:** Redemption (CMU/SEI) — 94.4%, but patches probable-false-positives; SafeRepair doesn't.

**Repos tested (name-drop a few):** vim, sqlite (2 versions), cpython, radare2, TDengine, netdata, libpng, mongoose, TheAlgorithms/C, mpc.
