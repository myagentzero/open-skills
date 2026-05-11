#!/usr/bin/env python3
"""
convert_document.py — Batch document-to-Markdown converter using markitdown.

Usage:
    # Convert a single file (output to stdout)
    python convert_document.py document.pdf

    # Convert a single file to a specific output file
    python convert_document.py document.pdf -o output.md

    # Convert a single file into an output directory
    python convert_document.py document.pdf -d output_dir/

    # Convert all supported files in a directory
    python convert_document.py input_dir/ -d output_dir/

    # Convert with specific extensions only
    python convert_document.py input_dir/ -d output_dir/ --ext .pdf .docx .pptx
"""

import argparse
import os
import sys
from pathlib import Path

from markitdown import MarkItDown

SUPPORTED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".xls",
    ".html", ".htm", ".csv", ".json", ".xml",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".wav", ".mp3",
    ".zip", ".epub", ".msg",
}


def convert_file(md: MarkItDown, input_path: Path, output_path: Path | None = None) -> tuple[bool, str]:
    """Convert a single file to Markdown. Returns (success, message)."""
    try:
        result = md.convert(str(input_path))
        text = result.text_content

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text, encoding="utf-8")
            return True, f"✅ {input_path.name} → {output_path}"
        else:
            print(text)
            return True, f"✅ {input_path.name} (stdout)"

    except Exception as e:
        msg = f"❌ {input_path.name}: {e}"
        print(msg, file=sys.stderr)
        return False, msg


def find_files(input_dir: Path, extensions: set[str] | None = None) -> list[Path]:
    """Recursively find convertible files in a directory."""
    exts = extensions or SUPPORTED_EXTENSIONS
    files = []
    for p in sorted(input_dir.rglob("*")):
        if p.is_file() and p.suffix.lower() in exts:
            files.append(p)
    return files


def main():
    parser = argparse.ArgumentParser(description="Convert documents to Markdown using markitdown")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("-o", "--output", help="Output file path (single file mode)")
    parser.add_argument("-d", "--output-dir", help="Output directory (batch mode)")
    parser.add_argument("--ext", nargs="+", help="File extensions to process (e.g. .pdf .docx)")
    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error: {input_path} does not exist", file=sys.stderr)
        sys.exit(1)

    md = MarkItDown(enable_plugins=False)

    # Single file mode
    if input_path.is_file():
        output_path = None
        if args.output:
            output_path = Path(args.output)
        elif args.output_dir:
            out_dir = Path(args.output_dir)
            output_path = out_dir / (input_path.stem + ".md")

        success, msg = convert_file(md, input_path, output_path)
        print(msg, file=sys.stderr)
        sys.exit(0 if success else 1)

    # Directory mode
    if input_path.is_dir():
        if not args.output_dir:
            print("Error: --output-dir (-d) is required for directory input", file=sys.stderr)
            sys.exit(1)

        out_dir = Path(args.output_dir)
        extensions = {e if e.startswith(".") else f".{e}" for e in args.ext} if args.ext else None
        files = find_files(input_path, extensions)

        if not files:
            print(f"No supported files found in {input_path}", file=sys.stderr)
            sys.exit(1)

        print(f"Found {len(files)} file(s) to convert...\n", file=sys.stderr)

        results = {"success": 0, "failed": 0, "messages": []}

        for f in files:
            # Preserve relative directory structure
            relative = f.relative_to(input_path)
            output_path = out_dir / relative.with_suffix(".md")
            success, msg = convert_file(md, f, output_path)
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
            results["messages"].append(msg)

        # Summary
        print("\n--- Conversion Summary ---", file=sys.stderr)
        for m in results["messages"]:
            print(m, file=sys.stderr)
        print(f"\nTotal: {results['success']} succeeded, {results['failed']} failed", file=sys.stderr)
        sys.exit(1 if results["failed"] > 0 else 0)


if __name__ == "__main__":
    main()
