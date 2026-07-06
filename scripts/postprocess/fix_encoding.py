"""
fix_encoding.py  v2
Direct string-replacement fix for known garbled UTF-8-via-Latin-1 sequences.
Handles the mixed-state file where some chars were already fixed manually.
"""
import os

path = os.path.join(os.path.dirname(__file__), 'FSD_SEAL_Project_Identity_v1.0.md')

with open(path, encoding='utf-8') as f:
    text = f.read()

# Mapping: garbled sequence -> correct Unicode character
# Garbled sequences arise when:
#   UTF-8 bytes are read as Latin-1/Windows-1252 and saved back
REPLACEMENTS = [
    # U+2014  EM DASH                  (UTF-8: E2 80 94 -> latin-1 reads: a + euro_sign + right_double_quot)
    ('\u00e2\u20ac\u201d', '\u2014'),
    # U+2013  EN DASH                  (UTF-8: E2 80 93 -> latin-1: a + euro_sign + left_double_quot)
    ('\u00e2\u20ac\u201c', '\u2013'),
    # U+2192  RIGHTWARDS ARROW         (UTF-8: E2 86 92 -> latin-1: a + dagger + right_single_quot)
    ('\u00e2\u2020\u2019', '\u2192'),
    # U+2190  LEFTWARDS ARROW          (UTF-8: E2 86 90 -> latin-1: a + dagger + tilde)
    ('\u00e2\u2020\u02dc', '\u2190'),
    # U+2713  CHECK MARK               (UTF-8: E2 9C 93 -> latin-1: a + oe + left_double_quot)
    ('\u00e2\u0153\u201c', '\u2713'),
    # U+2717  BALLOT X                 (UTF-8: E2 9C 97 -> latin-1: a + oe + em_dash)
    ('\u00e2\u0153\u2014', '\u2717'),
    # U+2022  BULLET                   (UTF-8: E2 80 A2 -> latin-1: a + euro_sign + copyright)
    ('\u00e2\u20ac\u00a2', '\u2022'),
    # U+2026  HORIZONTAL ELLIPSIS      (UTF-8: E2 80 A6 -> latin-1: a + euro_sign + broken_bar)
    ('\u00e2\u20ac\u00a6', '\u2026'),
    # U+201C  LEFT DOUBLE QUOT         (UTF-8: E2 80 9C -> latin-1: a + euro_sign + oe)
    ('\u00e2\u20ac\u0153', '\u201c'),
    # U+201D  RIGHT DOUBLE QUOT        (UTF-8: E2 80 9D -> latin-1: a + euro_sign + TM)
    ('\u00e2\u20ac\u2122', '\u201d'),
    # U+2019  RIGHT SINGLE QUOT        (UTF-8: E2 80 99 -> latin-1: a + euro_sign + trademark alt)
    ('\u00e2\u20ac\u2122', '\u2019'),
    # U+00D7  MULTIPLICATION SIGN      (UTF-8: C3 97 -> latin-1: A-tilde + em_dash)
    ('\u00c3\u2014', '\u00d7'),
]

count_total = 0
for bad, good in REPLACEMENTS:
    n = text.count(bad)
    if n:
        text = text.replace(bad, good)
        print(f"  Fixed {n}x: {repr(bad)} -> {repr(good)}")
        count_total += n

print(f"\nTotal replacements: {count_total}")

with open(path, 'w', encoding='utf-8', newline='') as f:
    f.write(text)

# Final check
import re
remaining = [(m.start(), text[max(0,m.start()-10):m.start()+15]) 
             for m in re.finditer(r'[\u00e2\u00c3]', text)]
if remaining:
    print(f"\nWARNING: {len(remaining)} potentially garbled chars still remain:")
    for pos, ctx in remaining[:10]:
        print(f"  pos {pos}: {repr(ctx)}")
else:
    print("\nAll clean! No garbled characters remain.")
print(f"Done: {path}")
