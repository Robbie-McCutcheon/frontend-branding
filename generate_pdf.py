#!/usr/bin/env python3
"""
Minimal PDF generator (single page) that writes a plain-text snapshot of the branding page.
This produces `branding_page.pdf` in the same folder.

This implementation writes a very small PDF using low-level PDF objects so it has
no external dependencies and works on a default Python installation.
"""
import datetime
import os

OUT = 'branding_page.pdf'

def pdf_escape(s: str) -> str:
    """Escape parentheses and backslashes for PDF literal strings."""
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

def make_pdf(path: str):
    title = 'Robbie McCutcheon — Frontend Workshop Branding'
    lines = [
        title,
        '',
        'About:',
        'I am a frontend engineer focused on building clean, performant web experiences. This page is a professional branding sample for the FrontEndWorkshop assignment.',
        '',
        'Selected highlights:',
        '- Design systems and component libraries for accessible products',
        '- Performance-driven single-page apps',
        '- Mentoring and workshops teaching HTML/CSS/React',
        '',
        'Contact:',
        'robbiem@example.com',
        '',
        'Repository (replace with your repo URL after publishing): https://github.com/YOUR-USERNAME/YOUR-REPO',
        '',
        f'Generated: {datetime.datetime.utcnow().isoformat()} UTC'
    ]

    # Build the content stream with simple left-aligned lines
    font_size = 12
    leading = font_size + 4
    x = 72
    y_start = 720

    content_lines = [f'BT /F1 {24} Tf {x} {y_start} Td ({pdf_escape(title)}) Tj ET']
    y = y_start - leading - 8
    content_lines.append(f'BT /F1 {10} Tf {x} {y} Td ({pdf_escape("Generated: " + datetime.datetime.utcnow().strftime("%Y-%m-%d"))}) Tj ET')
    y -= leading

    content_lines.append('BT')
    content_lines.append(f'/F1 {font_size} Tf')
    content_lines.append(f'{x} {y} Td')
    for line in lines[2:]:
        esc = pdf_escape(line)
        content_lines.append(f'({esc}) Tj')
        content_lines.append(f'0 -{leading} Td')
    content_lines.append('ET')

    content_stream = '\n'.join(content_lines).encode('utf-8')

    # PDF objects
    objs = []
    # 1: Catalog
    objs.append(b'1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n')
    # 2: Pages
    objs.append(b'2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n')
    # 3: Page
    objs.append(b'3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 4 0 R >>\nendobj\n')
    # 4: Font (Helvetica)
    objs.append(b'4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n')
    # 5: Content stream (we'll add length dynamically as object 5)
    # Build content stream object
    stream = b'stream\n' + content_stream + b'\nendstream\n'
    content_obj = b'5 0 obj\n<< /Length ' + str(len(content_stream)).encode() + b' >>\n' + stream + b'endobj\n'
    objs.append(content_obj)

    # Compute xref positions
    pdf_parts = [b'%PDF-1.4\n%\xE2\xE3\xCF\xD3\n']
    offsets = []
    pos = len(b''.join(pdf_parts))
    for o in objs:
        offsets.append(pos)
        pdf_parts.append(o)
        pos += len(o)

    xref_pos = pos
    # Build xref
    pdf_parts.append(b'xref\n0 %d\n' % (len(objs) + 1))
    pdf_parts.append(b'0000000000 65535 f \n')
    for off in offsets:
        pdf_parts.append(b'%010d 00000 n \n' % off)

    trailer = b'trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n' % (len(objs) + 1, xref_pos)
    pdf_parts.append(trailer)

    with open(path, 'wb') as f:
        f.write(b''.join(pdf_parts))

    print(f'Wrote {path}')

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, OUT)
    make_pdf(out)
