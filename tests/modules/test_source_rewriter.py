"""tests for source_rewriter.py"""

import pytest
from saferepair.source_rewriter import SourceRewriter


@pytest.fixture
def sample_file(tmp_path):
    """Create a sample 5-line C file"""
    content = (
        "line 1\n"
        "line 2\n"
        "line 3\n"
        "line 4\n"
        "line 5\n"
    )
    f = tmp_path / "test.c"
    f.write_text(content)
    return f


def test_no_edits_returns_original(sample_file):
    rw = SourceRewriter(sample_file)
    result = rw.apply()
    assert result == sample_file.read_text()


def test_replace_single_line(sample_file):
    rw = SourceRewriter(sample_file)
    rw.replace_line(3, "REPLACED\n")
    result = rw.apply()
    lines = result.splitlines()
    assert lines[0] == "line 1"
    assert lines[1] == "line 2"
    assert lines[2] == "REPLACED"
    assert lines[3] == "line 4"
    assert lines[4] == "line 5"


def test_insert_after_line(sample_file):
    rw = SourceRewriter(sample_file)
    rw.insert_after_line(2, "INSERTED\n")
    result = rw.apply()
    lines = result.splitlines()
    assert len(lines) == 6
    assert lines[0] == "line 1"
    assert lines[1] == "line 2"
    assert lines[2] == "INSERTED"
    assert lines[3] == "line 3"


def test_insert_before_line(sample_file):
    rw = SourceRewriter(sample_file)
    rw.insert_before_line(3, "BEFORE\n")
    result = rw.apply()
    lines = result.splitlines()
    assert len(lines) == 6
    assert lines[1] == "line 2"
    assert lines[2] == "BEFORE"
    assert lines[3] == "line 3"


def test_multiple_edits_reverse_order(sample_file):
    """Edits at lines 5, 3, and 1 should all apply correctly."""
    rw = SourceRewriter(sample_file)
    rw.replace_line(5, "five\n")
    rw.replace_line(3, "three\n")
    rw.replace_line(1, "one\n")
    result = rw.apply()
    lines = result.splitlines()
    assert lines[0] == "one"
    assert lines[1] == "line 2"
    assert lines[2] == "three"
    assert lines[3] == "line 4"
    assert lines[4] == "five"


def test_write_output(sample_file, tmp_path):
    rw = SourceRewriter(sample_file)
    rw.replace_line(1, "modified\n")
    output = tmp_path / "output" / "test.c"
    rw.write(output)
    assert output.exists()
    assert "modified" in output.read_text()


def test_auto_newline(sample_file):
    """text without trailing newline should have one added."""
    rw = SourceRewriter(sample_file)
    rw.replace_line(1, "no newline")  # no \n
    result = rw.apply()
    lines = result.splitlines(keepends=True)   #keeps \n 
    assert lines[0] == "no newline\n"


def test_out_of_range_edit_is_skipped(sample_file):
    """An edit targeting a line beyond the file should be silently skipped."""
    rw = SourceRewriter(sample_file)
    rw.replace_line(999, "beyond end of file\n")
    result = rw.apply()
    # file should be unchanged
    assert result == sample_file.read_text()


def test_write_creates_parent_dirs(tmp_path, sample_file):
    """write() should create missing parent directories."""
    rw = SourceRewriter(sample_file)
    deep_output = tmp_path / "a" / "b" / "c" / "out.c"
    rw.write(deep_output)
    assert deep_output.exists()
