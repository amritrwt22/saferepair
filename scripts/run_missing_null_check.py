"""Real-world validation of MissingNullCheckHandler on confirmed CWE-690 instances"""

import logging
import sys
from config import MISSING_NULL_CHECK_REPOS as REPOS, MISSING_NULL_CHECK_OUT_BASE as OUT_BASE
from script_utils import process_repo, setup_logging
from saferepair.reporter import generate_run_report

logger = logging.getLogger(__name__)


def main():
    setup_logging()

    logger.info("=" * 60)
    logger.info("  SafeRepair — MISSING_NULL_CHECK real-world validation")
    logger.info("=" * 60)

    #all repos processed
    all_results = [process_repo(cfg) for cfg in REPOS]

    #results.md generated for pattern
    out_path = generate_run_report(
        all_results,
        "MISSING_NULL_CHECK",
        "MissingNullCheckHandler",
        OUT_BASE,
        notes=["Repos found via grep.app, Sourcegraph, already-cloned repos.."],
    )
    logger.info(f"\nResults written to: {out_path}")

    sys.exit(1 if any(r["failed"] > 0 for r in all_results) else 0)


if __name__ == "__main__":           ##main() only runs when executed directly, not when imported
    main()
