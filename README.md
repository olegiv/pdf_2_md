# PDF to Markdown Converter with TOC and NLP Summarization

## Overview

This tool converts PDF files into Markdown (`.md`) format and generates a `TOC.md` that includes:
- Titles extracted from each Markdown file
- Language-aware NLP summaries using the TextRank algorithm

## Structure

```
project/
├── main.py
├── requirements.txt
├── Makefile
├── run.sh
├── tests/
│   └── test_summary.py
├── var/
│   ├── pdf/    # Place your .pdf files here
│   └── md/     # Output .md files and TOC.md go here
└── venv/       # Virtual environment (created automatically)
```

## Usage

1. Create a virtual environment and install dependencies:

```bash
make install
```

2. Convert PDFs and generate TOC:

```bash
make run
```

3. Run tests:

```bash
make test
```

Or use the shell runner:

```bash
./run.sh --lang en
```

## Requirements

- Python 3.8+
- Packages: `pdfminer.six`, `sumy`, `nltk`, `langdetect`

## Notes

- Automatically detects document language if `--lang` is not specified.
- Falls back to English summarization if the detected language is unsupported.
