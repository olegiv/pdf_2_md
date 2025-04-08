import os
import pytest
from pathlib import Path
from pdf_2_md.main import extract_heading_and_summary

def test_summary_generation():
    test_file = Path(__file__).resolve().parent / "../var/md/test.md"
    test_file.parent.mkdir(parents=True, exist_ok=True)  # Ensure dir exists

    with open(test_file, "w", encoding="utf-8") as f:
        f.write("# Test Document\nThis is a test document for summary extraction. It should return meaningful results.")

    title, summary, lang = extract_heading_and_summary(str(test_file))
    assert title == "Test Document"
    assert "summary" in summary.lower() or len(summary) > 10
    assert lang in {"en", "fr", "de", "es", "ru", "pt", "pl", "cs", "sl", "it"}
