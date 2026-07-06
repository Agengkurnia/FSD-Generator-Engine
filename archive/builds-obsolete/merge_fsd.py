import re

def fix_table_numbering(text, start_num=5):
    """Dynamically renumber 4.3.x sections since v2.0 ended at 4.3.4 for step 1."""
    current_num = start_num
    
    def repl(m):
        nonlocal current_num
        res = f"**4.3.{current_num} {m.group(1)}**"
        current_num += 1
        return res
        
    return re.sub(r'\*\*4\.3\.\d+\s+(`[^`]+`)\*\*', repl, text)

with open('FSD_New_RM_Sample_v1.9.md', 'r', encoding='utf-8') as f:
    t19 = f.read()

with open('FSD_New_RM_Sample_v2.0.md', 'r', encoding='utf-8') as f:
    t20 = f.read()

# -------------------------------------------------------------
# Part A: Up to STEP 2 Header from v2.0
# -------------------------------------------------------------
match_a = re.search(r'#### STEP 2 – Document Sample \(2 Tabel\)', t20)
if not match_a:
    print("Match A failed", t20[500:600])

part_a = t20[:match_a.end()] + '\n\n'

# -------------------------------------------------------------
# Part B: Tables from v1.9 (Step 2 to 4)
# -------------------------------------------------------------
match_b_start = re.search(r'\*\*4\.3\.6\s+`trSamplePurpose_Header`\*\*', t19)
match_b_end = re.search(r'### 4\.4 Tabel Master yang Digunakan', t19)

part_b_raw = t19[match_b_start.start():match_b_end.start()]

# Terminology replacements logic:
# 1. "Document Sample" -> "Document Registration"
# 2. "Sample Purpose" -> "Document Sample"
# 3. Add temporary marker for "Document Sample" so it's not replaced twice.
part_b = part_b_raw.replace('Document Sample', '___DOC_REG___')
part_b = part_b.replace('Sample Purpose', 'Document Sample')
part_b = part_b.replace('___DOC_REG___', 'Document Registration')

# Fix Table Numbering
part_b = fix_table_numbering(part_b, start_num=5)

# -------------------------------------------------------------
# Part C: From 4.4 Table Master to Appendix A's A.4 section end in v2.0
# -------------------------------------------------------------
match_c_start = re.search(r'### 4\.4 Tabel Master yang Digunakan', t20)
match_c_end = re.search(r'\*End of Appendix A\*', t20)

part_c_raw = t20[match_c_start.start():match_c_end.start()]

# We want to insert the missing SQL scripts from v1.9 right BEFORE A.4 in v2.0 (A.4 is Seed Data)
# Wait, actually A.3 in v2.0 is Alter script. A.4 is Seed data.
# The missing scripts from v1.9 are:
# A.3 Child Tables Step 1
# A.4 Step 2
# A.5 Step 3
# A.6 Step 4
# Let's insert them into t20 right before "### A.3 Script Alter" and renumber them to A.3..A.6
# Then the old A.3 (Alter) becomes A.7, A.4 (Seed) becomes A.8.

match_v2_appendix = re.search(r'## Appendix A:', part_c_raw)
match_v2_a3_alter = re.search(r'### A\.3 Script Alter', part_c_raw)

# Extract missing Appendix A tables from v1.9
match_v1_a3 = re.search(r'### A\.3 Child Tables Step 1', t19)
match_v1_rm_db = re.search(r'## Modul RM Database', t19)

app_tables_raw = t19[match_v1_a3.start():match_v1_rm_db.start()]
app_tables = app_tables_raw.replace('A.3 Child Tables', 'A.3 Child Tables')
app_tables = app_tables.replace('A.4 Step 2', 'A.4 Step 2')
app_tables = app_tables.replace('A.5 Step 3', 'A.5 Step 3')
app_tables = app_tables.replace('A.6 Step 4', 'A.6 Step 4')
app_tables = app_tables.replace('Document Sample', '___DOC_REG___')
app_tables = app_tables.replace('Sample Purpose', 'Document Sample')
app_tables = app_tables.replace('___DOC_REG___', 'Document Registration')

# Change A.3 Alter and A.4 Seed in v2.0 to A.7 and A.8
part_c_tail = part_c_raw[match_v2_a3_alter.start():]
part_c_tail = part_c_tail.replace('### A.3 Script Alter', '### A.7 Script Alter')
part_c_tail = part_c_tail.replace('### A.4 Seed Data', '### A.8 Seed Data')

part_c_head = part_c_raw[:match_v2_a3_alter.start()]
part_c = part_c_head + app_tables + part_c_tail

# -------------------------------------------------------------
# Part G: Modul RM Database from v1.9
# -------------------------------------------------------------
part_g = t19[match_v1_rm_db.start():]

full_text = part_a + part_b + part_c + "\n\n*End of Appendix A*\n\n" + part_g

# Change heading and revision history
full_text = full_text.replace('FSD_New_RM_Sample_v2.0.md', 'FSD_New_RM_Sample_v2.1.md')
full_text = full_text.replace(
    '## Riwayat Revisi\n\n| Versi | Tanggal | Deskripsi |\n|---|---|---|\n| 2.0 | 06-Apr-2026 | Perombakan terminologi wizard (Document Server -> Document Registration), relokasi field Shipping & Organik |',
    '## Riwayat Revisi\n\n| Versi | Tanggal | Deskripsi |\n|---|---|---|\n| 2.1 | 08-Apr-2026 | Full fungsional spesifikasi beserta skema dan DDL database |\n| 2.0 | 06-Apr-2026 | Perombakan terminologi wizard, relokasi field |'
)
full_text = full_text.replace('![New RM Sample Business Flow Diagram v2.0]', '![New RM Sample Business Flow Diagram v2.1]')
full_text = full_text.replace('![New RM Sample ERD v2.0]', '![New RM Sample ERD v2.1]')

with open('FSD_New_RM_Sample_v2.1.md', 'w', encoding='utf-8') as f:
    f.write(full_text)

print("Merge completed! check FSD_New_RM_Sample_v2.1.md")
