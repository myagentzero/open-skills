---
name: doc-converter
version: 1.1.0
author: myagentzero
tags: [document, converter, markdown, pdf, word, powerpoint, excel, html, images, audio]
description: Convert documents (PDF, Word, PowerPoint, Excel, HTML, images, audio, etc.) to Markdown using markitdown.
---


# Skill: doc-converter

Convert documents (PDF, Word, PowerPoint, Excel, HTML, images, audio, etc.) to Markdown using markitdown.

## When to Use
- A `[Document: <name>] <path>` attachment marker appears in the message
- User wants to read/summarize a non-text file (PDF, DOCX, PPTX, XLSX, etc.)
- User says "convert this file", "read this PDF", "extract text from", "turn this into markdown"

## Supported Formats
| Format | Extension(s) |
|--------|-------------|
| PDF | .pdf |
| Word | .docx, .doc |
| PowerPoint | .pptx, .ppt |
| Excel | .xlsx, .xls |
| HTML | .html, .htm |
| CSV | .csv |
| JSON | .json |
| XML | .xml |
| Images (OCR) | .png, .jpg, .jpeg, .gif, .bmp, .tiff, .webp |
| Audio (transcribe) | .mp3, .wav, .m4a, .ogg, .flac |
| ZIP | .zip (recursively converts contents) |
| EPUB | .epub |

## Steps

### 1. Identify the file path
- If the message contains `[Document: <name>] <path>`, use `<path>` directly.
- If the user provides a path, resolve it relative to workspace.
- If no file is provided, ask: "Please share the file you'd like converted."

### 2. Ensure markitdown is installed
Use the shell tool:
```bash
markitdown -v
```

### 3. Validate the file exists
Use file_read or glob_search tool to confirm the file is present at the specified path. If not found, prompt the user to check the path. Slack will automatically upload files to `workspace/slack_files/` when shared, so check there if the path is relative.

### 4. Run markitdown conversion
Use the shell tool:
```bash
markitdown "/path/to/input/file.pdf"
```
This outputs Markdown to stdout.

To save the output:
```bash
markitdown "/path/to/input/file.pdf" > "/path/to/output/file.md"
```

**Output path convention:** Same directory as input, same filename, `.md` extension.
Example: `/workspace/slack_files/report.pdf` → `/workspace/slack_files/report.md`

### 4. Handle errors
- `command not found`: Run `pip3 install markitdown --break-system-packages`
- `File not found`: Confirm path with user
- Empty output: Try with `--use-llm` flag if LLM integration is available
- Unsupported format: Inform user of supported types

### 5. Return results
- If saving to file: Report the output path and a brief summary of the content.
- If displaying inline: Return the full Markdown (truncate at ~200 lines for very large docs, offer to save).
- Always mention page/slide count or file size if notable.

## Examples

**User:** "Convert this PDF to markdown [Document: report.pdf] /workspace/slack_files/report.pdf"
```bash
markitdown "/workspace/slack_files/report.pdf" > "/workspace/slack_files/report.md"
```
→ "Converted to `/workspace/slack_files/report.md` — 12 pages, 3,400 words."

**User:** "Read this PowerPoint [Document: deck.pptx] /workspace/slack_files/deck.pptx"
```bash
markitdown "/workspace/slack_files/deck.pptx"
```
→ Display inline Markdown content

**User:** "Extract text from this Excel file [Document: data.xlsx] /workspace/slack_files/data.xlsx"
```bash
markitdown "/workspace/slack_files/data.xlsx" > "/workspace/slack_files/data.md"
```
→ "Converted to `/workspace/slack_files/data.md` — 3 sheets."

## Notes
- markitdown preserves structure: headings, tables, lists, code blocks
- For images, OCR requires `markitdown[image]` extras: `pip3 install 'markitdown[image]' --break-system-packages`
- For audio transcription: `pip3 install 'markitdown[audio]' --break-system-packages`
- Large files (>50MB) may be slow — warn the user
- Always prefer saving to file over dumping raw output for docs >50 lines
- Files in /workspace/slack_files will automatically clean up after 30 days

