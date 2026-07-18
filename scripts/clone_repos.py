"""clone repos needed for SafeRepair real-world validation.

   Usage: python scripts/clone_repos.py
"""

import io
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path
from config import (
    INDEX_CHECK_AFTER_USE_REPOS,
    MISSING_NULL_CHECK_REPOS,
    SPRINTF_UNBOUNDED_REPOS,
    SUSPICIOUS_REALLOC_REPOS,
    REPOS_DIR,
)


ALL_REPOS = (
    SUSPICIOUS_REALLOC_REPOS
    + MISSING_NULL_CHECK_REPOS
    + INDEX_CHECK_AFTER_USE_REPOS
    + SPRINTF_UNBOUNDED_REPOS
)


def clone_repo(cfg: dict) -> str:
    """git-clone a repo to given path.
       returns: 'cloned', 'skipped', or 'error: ...'
    """

    repo_dir: Path = cfg["repo_dir"]
    if repo_dir.exists():   #already cloned
        return "skipped"
    
    try:
        result = subprocess.run(
            ["git", "clone", "--depth=1", f"https://github.com/{cfg['slug']}.git", str(repo_dir)],
            capture_output=True, text=True, timeout=300,
        )
        return "cloned" if result.returncode == 0 else f"error: {result.stderr.strip()[:200]}"
    except subprocess.TimeoutExpired:
        return "error: timeout"
    except FileNotFoundError:
        return "error: git not found in PATH"
    except Exception as e:
        return f"error: {e}"


def download_single_file(cfg: dict) -> str:
    """download a source file from a URL. 
       returns: 'downloaded', 'skipped', or 'error: ...'

       handles cases:
         - zip_entry exist: fetches zip & extracts named entry
         - no zip_entry: fetches raw file directly
    """

    filename = Path(cfg["zip_entry"] or cfg["url"]).name
    dest: Path = cfg["repo_dir"] / filename
    if dest.exists():     #already downloaded
        return "skipped"

    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(cfg["url"], timeout=60) as resp:
            data = resp.read()
    except Exception as e:
        return f"error: {e}"

    try:
        if cfg.get("zip_entry"):
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                content = zf.read(cfg["zip_entry"])
        else:
            content = data
        dest.write_bytes(content)
        return "downloaded"
    except Exception as e:
        return f"error: {e}"


def main():
    REPOS_DIR.mkdir(parents=True, exist_ok=True)

    # deduplicate by repo_dir, some repos appear in mult. patterns
    seen: set[Path] = set()
    unique: list[dict] = []
    for cfg in ALL_REPOS:
        if cfg["repo_dir"] not in seen:
            seen.add(cfg["repo_dir"])
            unique.append(cfg)

    #full clones & single-file downloads
    git_repos  = [c for c in unique if c["slug"]]
    file_repos = [c for c in unique if c["url"]]

    cloned = skipped = errors = 0

    print(f"Cloning {len(git_repos)} repos into {REPOS_DIR}\n")
    for cfg in git_repos:
        #:<40 to left-align slug in 40-char col. 
        print(f"  {cfg['slug']:<40}", end="", flush=True)      #end="" to print status on same line, flush- forcess print to appear instead of be buffered
        status = clone_repo(cfg)
        print(status)
        if status == "cloned":    cloned += 1
        elif status == "skipped": skipped += 1
        else:                     errors += 1

    print(f"\nDownloading {len(file_repos)} single-file sources\n")
    for cfg in file_repos:
        print(f"  {cfg['display']:<50}", end="", flush=True)
        status = download_single_file(cfg)
        print(status)
        if status == "downloaded": cloned += 1
        elif status == "skipped":  skipped += 1
        else:                      errors += 1

    print(f"\nDone. cloned/downloaded={cloned}  skipped={skipped}  errors={errors}")
    if errors:
        print("Re-run the script to retry failed entries.")
        sys.exit(1)


if __name__ == "__main__":              #to only run script when exec. directly, not whwwn imported
    main()
