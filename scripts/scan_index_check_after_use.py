"""Scan all index_check_after_use repos (using plain text extractions) & write their alerts.json files."""

import argparse
import logging
import re
from pathlib import Path
from config import INDEX_CHECK_AFTER_USE_REPOS
from script_utils import get_relative_path, setup_logging, write_alerts_json
from saferepair.handlers.index_check_after_use import (
    blank_string_literals,
    strip_line_comment,
    paren_closed,
    for_middle_segment,
    split_top_level_and,
    subscript_index_vars,
    is_bound_check,
)


logger = logging.getLogger(__name__)


_CONTROL_RE = re.compile(r"\b(while|if|for)\s*\(")     #matches while (, if (, for (


def extract_condition(lines, start_idx):
    """extract the condition text of a while/if/for starting at lines[start_idx].
       returns: (keyword, condition_text, end_line_idx) or (None, None, start_idx).
    """

    #builds while(...)/if(...)/for(...) one line at a time
    combined = ""
    end_idx = start_idx
    for j in range(start_idx, min(start_idx + 10, len(lines))):
        combined += " " + strip_line_comment(lines[j])
        end_idx = j
        if paren_closed(combined):
            break
    combined_clean = blank_string_literals(combined)

    #searching for stuff in the combined block
    m = _CONTROL_RE.search(combined_clean)
    if not m:
        return None, None, start_idx
    keyword = m.group(1)        # "while", "if", or "for"
    open_pos = m.end() - 1      # index of '('

    #extracting actual condition text at 0depth brackets
    depth = 0
    body_chars = []
    i = open_pos
    while i < len(combined_clean):
        c = combined_clean[i]
        if c == "(":
            depth += 1
            if depth > 1:
                body_chars.append(combined[i])
        elif c == ")":
            depth -= 1
            if depth == 0:
                break
            body_chars.append(combined[i])
        else:
            if depth >= 1:
                body_chars.append(combined[i])
        i += 1
    if depth != 0:
        return None, None, start_idx
    full_body = "".join(body_chars).strip()
    cond = for_middle_segment(full_body) if keyword == "for" else full_body

    return keyword, cond, end_idx


def is_false_positive(left, right, var):
    if var in subscript_index_vars(right):    #right oprnd also has var as arr-index
        return True
    if is_bound_check(left, var):     #already has bound chekc
        return True
    return False


def scan_content(content, filepath_str, verbose=False):
    """Scan full file content for V781 instances
       returns: list of alert dicts.
    """

    lines = content.splitlines()
    alerts = []
    seen_lines = set()

    i = 0
    while i < len(lines):
        line = lines[i]

        #skip lines that dont even have wjile/for/if
        if not re.search(r"\b(?:while|if|for)\b", line):
            i += 1
            continue

        #skip if no && found till 4 lines ahead 
        window = " ".join(lines[i:min(i + 4, len(lines))])
        if "&&" not in window:
            i += 1
            continue

        #extract condition text
        keyword, condition, end_idx = extract_condition(lines, i)
        if not condition or "&&" not in condition:
            i = end_idx + 1
            continue

        if verbose:
            logger.debug(f"  [CAND] line {i + 1} ({keyword}): {condition[:100]}")

        #skip if top level && doesnt have oprs. in both left & right
        parts = split_top_level_and(condition)
        if len(parts) < 2:
            i = end_idx + 1
            continue

        #loops over consequetive pairs (of left & right oprs)
        for pi in range(len(parts) - 1):
            left = parts[pi]
            right = parts[pi + 1]

            #skip if no var. being used as an array index in left opr.
            idx_vars = subscript_index_vars(left)
            if not idx_vars:
                if verbose:
                    logger.debug("    [no-index] left=%s" % left[:60])
                continue
            
            #check if bound check exists on right for each index subscript found on left
            for var in idx_vars:
                if not is_bound_check(right, var):
                    continue
                if is_false_positive(left, right, var):
                    if verbose:
                        logger.debug(f"    [skip-fp] var={var}")
                    continue

                line_num = i + 1  #0-based to 1-based
                if line_num in seen_lines:
                    continue
                seen_lines.add(line_num)

                arr_match = re.search(r"\b(\w+)\s*\[", left)    #extracts array name from buf[i]
                arr_name = arr_match.group(1) if arr_match else "arr"
                message = (
                    f"V781: '{arr_name}[{var}]' used before '{var}' bound check "
                    f"in {keyword} condition -- swap && operands"
                )
                alerts.append({
                    "rule_id": "V781",
                    "file":    filepath_str,
                    "line":    line_num,
                    "column":  0,
                    "message": message,
                })

        i = end_idx + 1

    return alerts


def scan_repo(repo_dir: Path, verbose: bool = False) -> list[dict]:
    """"scans full repo content for index_check_after_use.
        returns: alerts in a dict.
    """

    all_alerts = []
    c_files = sorted(repo_dir.rglob("*.c")) 
    logger.info(f"Scanning {len(c_files)} .c files in {repo_dir.name}...")

    #scans each .c file found
    for cf in c_files:
        try:
            #fast check: convert to raw bytes & skip if &&, while, for, if not found
            raw = cf.read_bytes()
            if b"&&" not in raw or b"[" not in raw:
                continue
            if not (b"while" in raw or b"if" in raw or b"for" in raw):
                continue
            #cdecodes to text if passed pre-filter
            content = raw.decode("utf-8", errors="replace")
        except Exception as e:
            logger.debug(f"  SKIP (read error) {cf}: {e}")
            continue

        #scans decoded content & gets back alerts dict.
        filepath_rel = get_relative_path(cf, repo_dir)
        file_alerts = scan_content(content, filepath_rel, verbose=verbose)
        if file_alerts:
            logger.info(f"  {filepath_rel}: {len(file_alerts)} hit(s)")
        
        all_alerts.extend(file_alerts)

    return all_alerts


def main():
    p = argparse.ArgumentParser(description="scan all index-check-after-use repos")
    p.add_argument("--verbose", "-v", action="store_true") #syntax for adding flag
    args = p.parse_args()

    setup_logging(args.verbose)

    #scans all repos & writes their alerts.json
    for cfg in INDEX_CHECK_AFTER_USE_REPOS:
        repo_dir: Path = cfg["repo_dir"]
        if not repo_dir.is_dir():
            logger.warning(f"[SKIP] repo not found: {repo_dir}")
            continue
        alerts = scan_repo(repo_dir, verbose=args.verbose)
        logger.info(f"\nTotal: {len(alerts)} V781 instance(s) in {cfg['display']}")
        write_alerts_json(alerts, cfg["alerts_json"])


if __name__ == "__main__":                    #main() only runs when executed directly, not when imported
    main()
