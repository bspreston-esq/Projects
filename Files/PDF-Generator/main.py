#!/usr/bin/env python3
"""Write a valid PDF from plain text or HTML-ish input using only the stdlib."""
import argparse
import os
import re
import tempfile

PAGE_WIDTH, PAGE_HEIGHT = 595, 842   # A4 in points
MARGIN, LEADING, FONT_SIZE = 50, 14, 11
MAX_CHARS = 85

def escape(text: str) -> str:
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")

def wrap(line: str):
    if not line:
        return [""]
    words, rows, current = line.split(), [], ""
    for word in words:
        if len(current) + len(word) + 1 <= MAX_CHARS:
            current = (current + " " + word).strip()
        else:
            rows.append(current); current = word
    rows.append(current)
    return rows

def text_from_source(source: str) -> str:
    if source.lower().endswith((".html", ".htm")):
        with open(source, encoding="utf-8", errors="replace") as fh:
            html = fh.read()
        html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.S | re.I)
        html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
        html = re.sub(r"</(p|div|h[1-6]|li|tr)>", "\n", html, flags=re.I)
        html = re.sub(r"<[^>]+>", "", html)
        import html as html_module
        return html_module.unescape(html)
    with open(source, encoding="utf-8", errors="replace") as fh:
        return fh.read()

def build_pdf(text: str, title: str = "Document") -> bytes:
    lines = []
    for raw in text.splitlines():
        lines.extend(wrap(raw.expandtabs(4).rstrip()))
    per_page = int((PAGE_HEIGHT - 2 * MARGIN) // LEADING)
    pages = [lines[i:i + per_page] for i in range(0, len(lines), per_page)] or [[""]]

    objects = []

    def add(body: str) -> int:
        objects.append(body)
        return len(objects)

    font_id = add("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    page_ids, content_ids = [], []
    for page_lines in pages:
        commands = ["BT", f"/F1 {FONT_SIZE} Tf", f"{MARGIN} {PAGE_HEIGHT - MARGIN} Td", f"{LEADING} TL"]
        for line in page_lines:
            commands.append(f"({escape(line)}) Tj T*")
        commands.append("ET")
        stream = "\n".join(commands).encode("latin-1", "replace")
        content_ids.append(add(f"<< /Length {len(stream)} >>\nstream\n" + stream.decode("latin-1") + "\nendstream"))
        page_ids.append(None)  # placeholder, filled once kids are known

    pages_id = len(objects) + len(pages) + 1
    for index, content_id in enumerate(content_ids):
        page_ids[index] = add(
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_id} 0 R >>")
    kids = " ".join(f"{pid} 0 R" for pid in page_ids)
    actual_pages_id = add(f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>")
    assert actual_pages_id == pages_id
    catalog_id = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, body in enumerate(objects, 1):
        offsets.append(len(output))
        output += f"{number} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref_at = len(output)
    output += f"xref\n0 {len(objects) + 1}\n".encode()
    output += b"0000000000 65535 f \n"
    for offset in offsets[1:]:
        output += f"{offset:010d} 00000 n \n".encode()
    output += (f"trailer\n<< /Size {len(objects) + 1} /Root {catalog_id} 0 R /Info << /Title ({escape(title)}) >> >>\n"
               f"startxref\n{xref_at}\n%%EOF\n").encode()
    return bytes(output)

def demo() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        source = os.path.join(tmp, "input.txt")
        output = os.path.join(tmp, "output.pdf")
        with open(source, "w", encoding="utf-8") as fh:
            fh.write("PDF Generator\n\n" + "This paragraph demonstrates wrapping and pagination. " * 150 + "\n\nEnd of document.")
        data = build_pdf(open(source).read(), "Demo PDF")
        open(output, "wb").write(data)
        print(f"wrote {output}: {len(data):,} bytes")
        print("header:", data[:8].decode("latin-1"))
        print("pages:", data.count(b"/Type /Page "), "| xref present:", b"xref" in data, "| eof:", data.rstrip().endswith(b"%%EOF"))

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input")
    parser.add_argument("--output", default="output.pdf")
    parser.add_argument("--title", default="Generated PDF")
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo or not args.input:
        demo(); return
    text = text_from_source(args.input)
    data = build_pdf(text, args.title)
    with open(args.output, "wb") as fh:
        fh.write(data)
    print(f"wrote {args.output} ({len(data):,} bytes)")

if __name__ == "__main__":
    main()
