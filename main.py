__version__ = "0.0.2"

import os
import argparse
from pdfminer.high_level import extract_text

import nltk
from langdetect import detect
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.utils import get_stop_words

# Ensure 'punkt' is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    print("Downloading NLTK 'punkt' tokenizer...")
    nltk.download("punkt")

from pathlib import Path
from dotenv import load_dotenv

# Load .env if it exists
dotenv_path = Path(__file__).resolve().parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

env_lang = os.getenv("LANG_OVERRIDE")
PDF_DIR = os.getenv("PDF_DIR", "var/pdf")
MD_DIR = os.getenv("MD_DIR", "var/md")
SUMMARY_SENTENCES = int(os.getenv("SUMMARY_SENTENCES", "10"))
SUMMARY_CHAR_LIMIT = int(os.getenv("SUMMARY_CHAR_LIMIT", "4096"))

# --- Config validation ---
BASE_DIR = Path(__file__).resolve().parent
PDF_DIR = BASE_DIR / PDF_DIR
MD_DIR = BASE_DIR / MD_DIR

if not PDF_DIR.exists() or not PDF_DIR.is_dir():
    raise FileNotFoundError(f"PDF input directory does not exist: {PDF_DIR}")

if not isinstance(SUMMARY_SENTENCES, int) or SUMMARY_SENTENCES < 1:
    raise ValueError("SUMMARY_SENTENCES must be a positive integer")

if not isinstance(SUMMARY_CHAR_LIMIT, int) or SUMMARY_CHAR_LIMIT < 100:
    raise ValueError("SUMMARY_CHAR_LIMIT must be an integer >= 100")

SUPPORTED_LANGUAGES = {
    'en', 'fr', 'de', 'es', 'ru', 'pt', 'pl', 'cs', 'sl', 'it'
}

def convert_pdf_to_markdown(pdf_path, output_dir):
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    md_path = os.path.join(output_dir, base_name + '.md')

    print(f"Converting: {pdf_path}")
    text = extract_text(pdf_path)

    lines = text.splitlines()
    md_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            md_lines.append("")
            continue

        if stripped.isupper() and len(stripped.split()) < 10:
            md_lines.append(f"# {stripped}")
        elif stripped.startswith("- ") or stripped[0].isdigit():
            md_lines.append(f"- {stripped}")
        else:
            md_lines.append(stripped)

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_lines))

    print(f"Saved: {md_path}")

def extract_heading_and_summary(filepath, max_chars=SUMMARY_CHAR_LIMIT, forced_lang=None):
    title = os.path.splitext(os.path.basename(filepath))[0]
    full_text = ""

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#") and title == os.path.splitext(os.path.basename(filepath))[0]:
                title = stripped.strip("#").strip()
            full_text += stripped + " "

    lang = forced_lang or "en"
    detected = False
    if not forced_lang:
        try:
            lang = detect(full_text)
            detected = True
        except:
            lang = "en"

    if lang not in SUPPORTED_LANGUAGES:
        if detected:
            print(f"Language '{lang}' not supported. Falling back to English for {title}.")
        lang = "en"

    parser = PlaintextParser.from_string(full_text, Tokenizer(lang))
    summarizer = TextRankSummarizer()
    summarizer.stop_words = get_stop_words(lang)
    summary_sentences = summarizer(parser.document, SUMMARY_SENTENCES)

    summary = " ".join(str(s) for s in summary_sentences)
    if len(summary) > max_chars:
        summary = summary[:max_chars].rsplit(".", 1)[0] + "."

    return title, summary, lang

def generate_toc(md_dir, forced_lang=None):
    md_files = sorted([
        f for f in os.listdir(md_dir)
        if f.endswith('.md') and f.lower() != 'toc.md'
    ])

    toc_path = os.path.join(md_dir, 'TOC.md')
    with open(toc_path, 'w', encoding='utf-8') as toc:
        toc.write("# Table of Contents\n\n")
        for filename in md_files:
            full_path = os.path.join(md_dir, filename)
            title, summary, lang = extract_heading_and_summary(full_path, forced_lang=forced_lang)
            toc.write(f"- [{title}]({filename}) _(language: {lang})_\n")
            toc.write(f"{summary}\n\n")

    print(f"TOC generated: {toc_path}")

def ensure_output_dir():
    if not os.path.exists(MD_DIR):
        os.makedirs(MD_DIR)

def main():
    parser = argparse.ArgumentParser(description="Convert PDFs to Markdown and generate TOC with NLP summaries.")
    parser.add_argument("--lang", type=str, help="Force language code for summarization (e.g. en, fr, de)")
    parser.add_argument("--version", action="store_true", help="Show app version and exit")
    args = parser.parse_args()

    if args.version:
        print(f"PDF to Markdown Converter version {__version__}")
        return

    ensure_output_dir()

    pdf_files = sorted([
        os.path.join(PDF_DIR, f)
        for f in os.listdir(PDF_DIR)
        if f.endswith('.pdf')
    ])

    if not pdf_files:
        print(f"No PDF files found in: {PDF_DIR}")
        return

    for pdf_file in pdf_files:
        convert_pdf_to_markdown(pdf_file, MD_DIR)

    generate_toc(MD_DIR, forced_lang=args.lang or env_lang)

if __name__ == "__main__":
    main()
