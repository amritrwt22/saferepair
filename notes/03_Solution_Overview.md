# SafeRepair — The Solution (High-Level Overview)

> Topic 3 of the topic-wise notes. This file is deliberately **not** about the pipeline, the modules, or the code — that's a separate file coming next. This is the layer above that: what we decided to build, why we decided to build *that* instead of something else, and the principles that shaped every downstream decision. This is the "so what did you actually design" answer in an interview, before anyone asks "okay, now show me how it works."

---

## 1. The Core Idea, In One Move

Topic 1 established the gap: detection is automated, repair is manual, and that manual step is where known, already-flagged bugs go to die in a backlog. The core idea is simple to state:

> **Take a static-analysis alert and a source file, and produce a verified, safe patch — with no human in the loop at all.**

That's the whole ambition in one sentence. Everything else in this file is *why* it had to be built the specific way it was, not some other way.

---

## 2. Why This *Kind* of Solution — The Real Design Fork

Before any architecture gets decided, there's a genuine fork in the road, and it's worth being able to explain it as a real decision rather than an assumed default:

**Option A — Probabilistic repair** (an LLM, or a model trained on historical patches). Generalizes to far more bug types without hand-written rules. The cost: you cannot *prove* a given patch is correct, only estimate how likely it is to be — and that estimate comes from training data, needs GPU infrastructure, and produces different output on different runs.

**Option B — Deterministic, rule-based repair**, where a fix is only ever produced when it can be shown to be correct from the immediate context, using rules a human can read and verify. The cost: narrower scope — you can only cover bug patterns where such a rule is actually possible to write. The benefit: a correctness argument that holds regardless of which repo, which run, or which day it is.

**The deciding question we used:** *does this tool need to run with zero human review, ever?* If yes, "probably correct" isn't an acceptable answer no matter how high the probability is — a wrong patch applied silently is strictly worse than no patch. That single requirement is what forced Option B. This isn't "we didn't think of using an LLM" — it's "we evaluated the fork and picked the side that matches the actual constraint we set for ourselves."

*(If you want to go deeper on this specific tradeoff live in an interview — the literature comparison, where a hybrid would make sense, etc. — that's already covered in your STAR notes; this file just needs the decision and the reasoning behind it.)*

---

## 3. The Governing Principle: Right-or-Silent

Everything downstream traces back to one rule, stated at the concept level (not the code level):

> **A fix is only ever produced when it can be proven correct from the immediately available context. If it can't be proven, nothing happens — the source is left exactly as it was.**

There is no third option. Not "apply it and flag it for review," not "apply the most likely fix." Confirm-and-fix, or touch nothing.

**Why this specific principle, and not a "best effort with a confidence score" approach:** a confidence score is still a probability — it just moves the probabilistic guess from "is this a bug" to "is this the right fix," which doesn't actually solve the zero-false-positive requirement, it just relocates where the guessing happens. Right-or-silent removes guessing from the equation entirely by design, not by tuning a threshold well.

**The direct consequence:** coverage is deliberately traded for trust. A system built this way will always skip some real bugs it can't confirm strongly enough to act on — and that's treated as the *correct*, safe outcome, not a shortfall to apologize for.

---

## 4. Key Decision 1 — Scope Narrowly to Bugs Where the Fix Is Mechanically Unambiguous

Rather than aiming at "as many CWEs as possible," the project deliberately picked a small number of bug patterns with one specific property: **the correct fix doesn't depend on what the original developer was trying to do.** A buffer overflow, a leaked reallocation, a missing null guard — nobody ever intended any of these. There's no competing "valid alternative fix" to weigh against the obvious one.

**Why this matters as a decision, not just a detail:** most bugs *do* depend on intent, and for those, a human genuinely has to decide what "correct" even means here — that's not a gap in the tool, that's a category of problem the tool was never meant to own. Scoping to the mechanically-unambiguous subset is what makes the right-or-silent principle achievable at all, instead of an aspiration that quietly breaks on the first ambiguous case.

---

## 5. Key Decision 2 — Ground Truth Has to Be Program Structure, Not Surface Text

The principle: any claim of "this bug is really here" has to be checked against what a compiler itself would see — real program structure — never against the raw characters of the source file.

**Why:** text can say things that aren't true about the program. The word `realloc` can appear inside a comment, inside a string literal, inside a macro that never actually expands the way it reads. A rule that trusts text alone will eventually act on something that isn't really there. Structure doesn't have that failure mode — if something is confirmed as a real function call in the actual parsed program, it's real, full stop.

*(How that structural check is actually implemented — libclang, AST cursors, the specific traversal functions — is implementation detail for the next file. The point here is only the principle: verify against structure, never against text alone.)*

---

## 6. Key Decision 3 — Validation Has to Be Independent of the Reasoning That Produced the Fix

The principle: the same piece of reasoning that decided a fix is correct should not also be the thing that signs off on it. Something *external* and *differently derived* has to independently agree.

**Why:** any single reasoning process — however carefully designed — can have a blind spot that's invisible to itself. An outside check, built on a genuinely separate implementation, catches a different class of mistake than "check your own work twice." This is a fairly universal engineering idea (it's the same logic behind independent code review, or a second compiler in a safety-critical build) applied here to program repair specifically.

---

## 7. Key Decision 4 — Detection and Repair Stay Decoupled

The principle: the repair engine should never need to know or care *which* tool produced an alert, or how. It only needs a stable, minimal contract — roughly "here's a file, here's a line, here's what kind of bug this is claimed to be."

**Why:** coupling repair logic to one specific detector's internals would mean every new static analyzer, or every version upgrade of an existing one, risks breaking the repair side too. Keeping them decoupled means the detection layer is swappable — today it's one specific analyzer, tomorrow it could be a different one entirely, and the repair engine's logic doesn't change at all. This is a deliberate separation-of-concerns choice, not an accident of how the code happened to get organized.

---

## 8. Key Decision 5 — No Training Data, No Model File, Fully Reproducible

The principle: the exact same alert, fed in today or five years from now, on any machine, should produce the exact same output — no model weights, no GPU, no internet connection, no drift between runs.

**Why this was treated as a hard requirement and not a nice-to-have:** the target context is security-relevant code, potentially inside a CI pipeline. Reproducibility and auditability aren't bonus features there — a patch that can't be explained the same way twice is a patch nobody can fully trust, no matter how good its track record looks so far.

---

## 9. The Bar We Actually Held Ourselves To

It's worth being precise about what "success" meant for this project, because it's not the obvious answer:

> **Not:** the highest possible fix rate.
> **Actually:** the highest fix rate achievable *without ever compromising* a zero-false-positive guarantee.

Those sound similar but they're not the same optimization target. Chasing raw fix rate alone would eventually pressure the design toward guessing on ambiguous cases. Holding the false-positive guarantee as the non-negotiable constraint, and *then* maximizing fix rate underneath it, is what actually produced a defensible result instead of an impressive-looking but fragile one.

**One-line mantra worth having ready:** *coverage yields to trust.*

---

## 10. The Five Principles, Together

```
 THE FORK               THE PRINCIPLE            THE DECISIONS UNDER IT
 ---------------        -------------------      ------------------------------
 Provable fix       ->  Right-or-silent      ->  1. Narrow, unambiguous scope
 over probable                                   2. Structure, not text, is truth
 fix                                              3. Independent validation
                                                   4. Detection/repair decoupled
                                                   5. No training data, reproducible

                                |
                                v
                    Coverage yields to trust
```

---

## One-Paragraph Version (for quick recall)

> The real design decision wasn't "how do we build this" — it was "probabilistic repair or deterministic repair," and the requirement of running with zero human review forced the deterministic side. Everything follows from one governing principle: a fix only ever gets produced if it can be proven correct from context, otherwise nothing happens at all — no partial fixes, no confidence scores, no guessing relocated to a different step. That principle only works if the scope stays narrow to bugs where the fix doesn't depend on intent, if "confirmed" means checked against real program structure rather than surface text, if validation comes from something independent of the reasoning that produced the fix, if detection and repair stay decoupled from each other, and if the whole thing stays fully deterministic and reproducible with no training data. The bar we held ourselves to wasn't the highest fix rate possible — it was the highest fix rate achievable without ever giving up the false-positive guarantee. Coverage yields to trust.
