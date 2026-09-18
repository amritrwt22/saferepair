# SafeRepair Interview Prep — Build Guide

**What this file is:** instructions for building your actual study notes — not the notes themselves. This defines the structure to follow, tells you which existing file/section to pull content from for each part, and flags the parts that genuinely don't exist yet and need to be written fresh. Follow this file to build the real notes next.

**Where the content already lives:**
- `Interview_STAR_Notes.md` — the pitch, architecture summary, pattern deep-dives, objections, comparisons, limitations. Verified against the actual repo code.
- `SafeRepair Study Guide.md`, `Code Structure Study.md`, `SafeRepair BTP notes.md`, `points.md` — your older raw material. Useful as source text to mine, but contains stale numbers (17 repos/354 alerts — wrong, ignore) and is written for a professor/viva audience, not an interview. Don't study these directly; pull specific sections into the new notes as noted below.
- The actual code in `saferepair-repo/saferepair/` — ground truth. Anything in the notes that contradicts the code is wrong; the code wins.

---

## The 3-Layer Structure Your Notes Should Follow

This is the order you actually use in an interview, so it's the order to build and study in.

```
Layer 1: The Pitch           (2-3 min, spoken, STAR)
Layer 2: Architecture 0→100  (what's built, why, how it helps — the deep walkthrough)
Layer 3: Question Bank       (3a: fundamentals, 3b: project-specific, 3c: meta/behavioral)
```

---

## Layer 1 — The Pitch (2-3 minutes)

**What it must contain:** Situation (the problem — detection is solved, repair isn't, and why that gap matters), Task (what we set out to build and the constraint we held ourselves to — no LLM, no training data, no false positives), Action (the core design idea in one or two sentences — right-or-silent, AST-confirmed, 4 narrow patterns), Result (the numbers).

**Source to build from:** `Interview_STAR_Notes.md` Part 0 (20-sec cold open) and Part 1 (90-sec STAR) are already written and verified. For a full 2–3 minutes, read Part 1 at a natural speaking pace with one or two extra sentences of elaboration — don't pad with new content, just don't rush it.

**Still open:** the `[PERSONALIZE: ...]` bracket in Part 1's Action section — fill this in with what you actually drove (methodology / evaluation / report) before you memorize this layer. Everything downstream assumes this is filled in honestly.

**Target when done:** deliverable is one paragraph, ~350–450 spoken words, that you can say without notes.

---

## Layer 2 — Architecture From 0 to 100

This is the deep walkthrough: not just "what exists" but **what problem each piece solves and why it was built that way**. This is the layer where "I don't know anything about this project" gets fixed for real — it's the difference between reciting Part 3/4 of the STAR notes and actually understanding them.

**Build it in this order** (matches the real data flow, so it teaches itself):

1. **The input.** What's an `Alert`? Where does `alerts.json` come from (clang-tidy / custom libclang scanner / Clang Static Analyzer output, normalized into one schema)? Why does the project even start from a JSON file instead of running the analyzer itself? (Source: `models.py` `Alert` dataclass; `ch3_methodology.tex` §Alert Ingestion; `Interview_STAR_Notes.md` Part 3.)

2. **Each of the 6 pipeline modules, one at a time** — for every module answer three things: *what it is, why it needs to exist as its own module (what would break if you merged it into another one), how it helps the end goal.*
   - `alert_parser.py` — JSON → `Alert` objects. Why separate from classification? (a scanner's raw output format is not the tool's concern of the rest of the pipeline — separation of concerns)
   - `pattern_detector.py` — rule_id → `RepairPattern` enum. Why a dictionary mapping multiple rule_ids to one pattern? (different scanners name the same bug differently — this is what makes the tool scanner-agnostic)
   - `ast_analyzer.py` — libclang parsing + traversal helpers (`find_call_expr_at_line`, `find_enclosing_function`, `get_line_text`). Why libclang and not just regex? (this is the crux of the whole project — see Layer 3a)
   - `pipeline.py` — orchestration: groups alerts by file, parses AST once per file, dispatches to handlers. Why group by file first? (parse cost stays fixed regardless of alert count per file)
   - `source_rewriter.py` — queues edits, applies all at once. Why queue instead of editing immediately? (so multiple fixes to the same file don't shift each other's line numbers mid-run — read the actual queuing logic, it's a real "why" not a guess)
   - `validator.py` — `gcc -fsyntax-only` safety net. What exactly does this prove and NOT prove? (this is a common trick question — see Layer 3a "Validation" entry)
   - (Source for all of the above: `Interview_STAR_Notes.md` Part 3, verified line-by-line against `pipeline.py`, `models.py`, `ast_analyzer.py`, `handlers/base.py` — already read and confirmed matching the report. Still need to personally read: `alert_parser.py`, `pattern_detector.py`, `source_rewriter.py`, `validator.py`, and 3 of the 4 handlers — only `suspicious_realloc.py` has been read against the notes so far.)

3. **The two-phase handler contract** (`RepairHandler` base class — `can_handle()`, `analyze()`, `generate_fix()`). Why split analysis from fix generation into two methods instead of one? (analysis is read-only / side-effect-free; this is what makes "return None = touch nothing" a clean, enforceable rule rather than a convention someone could violate by accident.) Source: `handlers/base.py`, read and confirmed.

4. **Each of the 4 handlers**, in increasing complexity order (realloc → null-check → sprintf → index-check, roughly easy to hardest): vulnerability → detection (regex prefilter + AST confirm) → fix → why the fix is provably correct → what makes it skip. Source: `Interview_STAR_Notes.md` Part 4, verified against `handlers/suspicious_realloc.py` already; verify the other 3 against their actual files the same way before treating them as solid.

5. **Tie it together: the right-or-silent principle.** This is the idea that makes the whole architecture make sense as *one thing* rather than four unrelated handlers — every piece above exists in service of "confirm-and-fix or touch nothing, no middle state." Practice explaining the architecture by starting from this principle and showing how each module serves it, rather than listing modules first and bolting the principle on at the end.

**Gate before moving to Layer 3:** pick any module or handler at random and explain what/why/how without looking. If you can't, that module needs its source file read (see the "still need to personally read" list above), not more time re-reading the STAR notes.

---

## Layer 3 — The Question Bank

Three different kinds of questions get asked, and they need different prep:

### 3a. Fundamentals (CS/tooling concepts — asked regardless of this specific project)

**These are the real gap.** Your existing notes cover static analysis and AST reasonably well already, but the others below aren't written anywhere yet — they need to be authored fresh as part of the actual notes build. Listed here with what a good answer needs to hit, so whoever builds the notes (you, or me if you ask) knows the bar:

- **What is memory in C/C++, and why is it dangerous?** Needs: stack vs. heap, manual allocation/free (no garbage collector), what a pointer actually is (an address, not a checked reference), why that combination is what creates the entire bug class this project exists to fix. This is the "set up the stakes" question — answering it well makes everything downstream make sense.
- **What is memory safety, and why does it matter?** Needs: spatial safety (don't access outside a valid allocation — buffer overflows) vs. temporal safety (don't access memory outside its valid lifetime — use-after-free, double-free). Good supporting fact already in your report: Szekeres et al.'s survey (cited in `ch1_introduction.tex`/`ch2_literature_review.tex`) showing every deployed mitigation (ASLR, DEP, stack canaries) has eventually been worked around — memory-safety bugs are a persistent, not solved, class of problem, and full enforcement costs ~67% runtime overhead, which is why source-level repair (this project's angle) is still worth doing.
- **What is a static analyzer, and how does it actually work?** Partially in `SafeRepair Study Guide.md` (its "Stage 3, Concept 1" section) — data-flow analysis, control-flow graph traversal, AST pattern matching, all without executing the code. Contrast with dynamic analysis (Valgrind/ASan — instruments a running binary). Pull that section into the new notes and tighten it.
- **What is libclang, specifically — how does it relate to Clang and LLVM?** Not written anywhere yet — needs fresh content. The layering: LLVM is the compiler backend (IR, optimization, codegen); Clang is the C/C++/Objective-C frontend that turns source into LLVM IR; libclang is a stable C API (with Python bindings) that exposes Clang's frontend — lexer, parser, semantic analysis, and the resulting AST — for tools to introspect, without needing to run a full compile. That's why this project can get a real, semantically-aware AST for a `.c` file even without all its headers resolved (`PARSE_INCOMPLETE`), and why it's a stronger foundation than hand-rolled parsing.
- **What is an AST, and why did you specifically need one here instead of just regex?** Well covered already in `SafeRepair Study Guide.md` (Stage 3, Concept 2) and `points.md`. The sharpest version of the answer, grounded in actual code: regex can't tell a real `realloc(...)` call from one sitting inside a comment or a macro-generated string — `find_call_expr_at_line()` in `ast_analyzer.py` walks real `CALL_EXPR` nodes, so it only matches code the compiler itself would treat as a live function call. Also: the AST is what lets `find_enclosing_function()` read a function's actual declared return type to generate a correctly-typed `return` statement — something no text-only approach could do at all.
- **What is a CWE?** Not written anywhere yet — needs fresh content. CWE = Common Weakness Enumeration, MITRE's catalog of general classes of software weaknesses (e.g. CWE-120 = buffer overflow via unbounded copy, CWE-690 = unchecked return value leading to NULL deref). Contrast with CVE, which is a specific vulnerability instance in a specific piece of software — a CWE is the *category*, a CVE is an *incident*. Useful line: each of this project's 4 handlers is scoped to one or two specific CWE IDs, which is what "narrow, well-characterized pattern" concretely means.
- **You validate before/after fixing — what exactly do you use, why that tool, and how does it guarantee correctness?** This one has a trap in it, and the honest answer is more impressive than the naive one: SafeRepair runs `gcc -fsyntax-only` on the patched file. This proves the patch is **syntactically valid C** — it compiles. It does **not** prove semantic correctness on its own. The actual correctness guarantee comes from the *design*: each handler's fix is argued correct by construction (e.g. the C standard guarantees `realloc` leaves the original pointer untouched on failure, so the temp-pointer pattern is sound regardless of what gcc says). GCC is an independent safety net that would catch a broken patch, not the source of the correctness claim. Getting this distinction right in an answer is a strong signal — don't just say "we validate with gcc" and stop there.

### 3b. Project-specific technical questions

Already built. Use: `Interview_STAR_Notes.md` Part 2 (rapid-fire first follow-ups), Part 4 (per-pattern deep dives), Part 6 (the 4 objections), Part 7 (comparison to prior work), Part 8 (limitations/future work).

### 3c. Meta / behavioral

Already built. Use: `Interview_STAR_Notes.md` Part 9 (SWE-framed questions, incl. the NVIDIA bridge) and Part 10 (how to honestly frame the AI-assisted development).

---

## What to Actually Do Next

1. Read the remaining source files listed in Layer 2 step 2 (you said you'd read the code — this is the checklist for that).
2. Fill in the `[PERSONALIZE]` bracket in Layer 1.
3. Tell me to write the fresh content for Layer 3a (the fundamentals — memory/memory-safety/libclang/CWE/validation) into a real notes section, since that's the one piece that doesn't exist anywhere yet. Everything else in Layers 1–3b/3c can be pulled from `Interview_STAR_Notes.md` largely as-is.
4. Once all three layers exist as real written notes (not just this blueprint), move to drilling: blank-page recall, and mock interviews with me.
