"""single source of truth for all repo paths, compiler flags, alert/output locations.

each repo dict contains the following keys:
  name        : short id used in filenames and logs
  display     : human-readable "owner/repo" label
  repo_dir    : path to cloned/downloaded source tree (under scripts/repos/)
  alerts_json : path to alerts file for repo
  out_dir     : where patched files are written
  extra_args  : extra compiler flags forwarded to clang-tidy (scan scripts)
  includes    : extra include dirs forwarded to clang-tidy (scan scripts)
  slug        : github slug "owner/repo" for git-cloned repos
  url         : download URL for single-file repos
  zip_entry   : path inside zip to extract
"""

from pathlib import Path

# base paths
SCRIPTS   = Path(__file__).parent
ROOT      = SCRIPTS.parent
REPOS_DIR = SCRIPTS / "repos"
_RW       = ROOT / "test_suite" / "real_world"

#per-pattern output bases (used by run scripts and as base paths in repo dicts below)
SUSPICIOUS_REALLOC_OUT_BASE    = _RW / "suspicious_realloc"
MISSING_NULL_CHECK_OUT_BASE    = _RW / "missing_null_check"
INDEX_CHECK_AFTER_USE_OUT_BASE = _RW / "index_check_after_use"
SPRINTF_UNBOUNDED_OUT_BASE     = _RW / "sprintf_snprintf"

# Shorter aliases for use in repo dicts below
_SR  = SUSPICIOUS_REALLOC_OUT_BASE
_MNC = MISSING_NULL_CHECK_OUT_BASE
_ICU = INDEX_CHECK_AFTER_USE_OUT_BASE
_SPR = SPRINTF_UNBOUNDED_OUT_BASE


# Repo lists ------------------------

SUSPICIOUS_REALLOC_REPOS = [
    {
        "name":        "mpc",
        "display":     "orangeduck/mpc",
        "slug":        "orangeduck/mpc",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "orangeduck__mpc",
        "alerts_json": _SR / "mpc/alerts.json",
        "out_dir":     _SR / "mpc/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "libtexprintf",
        "display":     "bartp5/libtexprintf",
        "slug":        "bartp5/libtexprintf",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "bartp5__libtexprintf",
        "alerts_json": _SR / "libtexprintf/alerts.json",
        "out_dir":     _SR / "libtexprintf/patched",
        "extra_args":  ["-std=c11"],
        "includes":    [],
    },
    {
        "name":        "libretro-prboom",
        "display":     "libretro/libretro-prboom",
        "slug":        "libretro/libretro-prboom",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "libretro__libretro-prboom",
        "alerts_json": _SR / "libretro-prboom/alerts.json",
        "out_dir":     _SR / "libretro-prboom/patched",
        "extra_args":  ["-std=c99", "-DHAVE_CONFIG_H"],
        "includes":    [],
    },
    {
        "name":        "heirloom-doctools",
        "display":     "n-t-roff/heirloom-doctools",
        "slug":        "n-t-roff/heirloom-doctools",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "n-t-roff__heirloom-doctools",
        "alerts_json": _SR / "heirloom-doctools/alerts.json",
        "out_dir":     _SR / "heirloom-doctools/patched",
        "extra_args":  [],
        "includes":    [],
    },
]

MISSING_NULL_CHECK_REPOS = [
    {
        "name":        "the_algorithms_c",
        "display":     "TheAlgorithms/C",
        "slug":        "TheAlgorithms/C",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "the_algorithms_c",
        "alerts_json": _MNC / "the_algorithms_c/alerts.json",
        "out_dir":     _MNC / "the_algorithms_c/patched",
        "extra_args":  [],
        "includes":    [],
    },
]

INDEX_CHECK_AFTER_USE_REPOS = [
    {
        "name":        "mongoose",
        "display":     "cesanta/mongoose",
        "slug":        "cesanta/mongoose",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "cesanta__mongoose",
        "alerts_json": _ICU / "mongoose/alerts.json",
        "out_dir":     _ICU / "mongoose/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "radare2",
        "display":     "radareorg/radare2",
        "slug":        "radareorg/radare2",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "radareorg__radare2",
        "alerts_json": _ICU / "radare2/alerts.json",
        "out_dir":     _ICU / "radare2/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "vim",
        "display":     "vim/vim",
        "slug":        "vim/vim",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "vim__vim",
        "alerts_json": _ICU / "vim/alerts.json",
        "out_dir":     _ICU / "vim/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "netdata",
        "display":     "netdata/netdata",
        "slug":        "netdata/netdata",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "netdata__netdata",
        "alerts_json": _ICU / "netdata/alerts.json",
        "out_dir":     _ICU / "netdata/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "spatterlight",
        "display":     "angstsmurf/spatterlight",
        "slug":        "angstsmurf/spatterlight",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "angstsmurf__spatterlight",
        "alerts_json": _ICU / "spatterlight/alerts.json",
        "out_dir":     _ICU / "spatterlight/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "sqlite_3420000",
        "display":     "sqlite/sqlite (3.42.0)",
        "slug":        None,
        "url":         "https://www.sqlite.org/2023/sqlite-amalgamation-3420000.zip",
        "zip_entry":   "sqlite-amalgamation-3420000/sqlite3.c",
        "repo_dir":    REPOS_DIR / "sqlite_3420000",
        "alerts_json": _ICU / "sqlite_3420000/alerts.json",
        "out_dir":     _ICU / "sqlite_3420000/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "sqlite_3410200",
        "display":     "sqlite/sqlite (3.41.2)",
        "slug":        None,
        "url":         "https://www.sqlite.org/2023/sqlite-amalgamation-3410200.zip",
        "zip_entry":   "sqlite-amalgamation-3410200/sqlite3.c",
        "repo_dir":    REPOS_DIR / "sqlite_3410200",
        "alerts_json": _ICU / "sqlite_3410200/alerts.json",
        "out_dir":     _ICU / "sqlite_3410200/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "cpython",
        "display":     "python/cpython (3.13.3)",
        "slug":        None,
        "url":         "https://raw.githubusercontent.com/python/cpython/v3.13.3/Python/lexer.c",
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "cpython",
        "alerts_json": _ICU / "cpython/alerts.json",
        "out_dir":     _ICU / "cpython/patched",
        "extra_args":  [],
        "includes":    [],
    },
]

SPRINTF_UNBOUNDED_REPOS = [
    {
        "name":        "libpng",
        "display":     "glennrp/libpng",
        "slug":        "glennrp/libpng",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "glennrp__libpng",
        "alerts_json": _SPR / "libpng/alerts.json",
        "out_dir":     _SPR / "libpng/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "netdata",
        "display":     "netdata/netdata",
        "slug":        "netdata/netdata",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "netdata__netdata",
        "alerts_json": _SPR / "netdata/alerts.json",
        "out_dir":     _SPR / "netdata/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "tdengine",
        "display":     "taosdata/TDengine",
        "slug":        "taosdata/TDengine",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "taosdata__TDengine",
        "alerts_json": _SPR / "tdengine/alerts.json",
        "out_dir":     _SPR / "tdengine/patched",
        "extra_args":  [],
        "includes":    [],
    },
    {
        "name":        "vim",
        "display":     "vim/vim",
        "slug":        "vim/vim",
        "url":         None,
        "zip_entry":   None,
        "repo_dir":    REPOS_DIR / "vim__vim",
        "alerts_json": _SPR / "vim/alerts.json",
        "out_dir":     _SPR / "vim/patched",
        "extra_args":  [],
        "includes":    [],
    },
]
