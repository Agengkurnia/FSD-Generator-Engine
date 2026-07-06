# Panduan Menambahkan Screenshot ke FSD

## Mengapa Screenshot Penting?

Screenshot dari prototype HTML akan membuat FSD lebih visual dan mudah dipahami oleh:
- Developer yang akan implement
- Business Analyst yang review
- Stakeholder yang approve

## Cara Menambahkan Screenshot

### Langkah 1: Capture Screenshot dari Browser

1. **Buka file HTML di browser** (Chrome/Edge recommended)
   ```
   - BTPIndex.html
   - BTPDetail.html
   - BTPFunctionIndex.html
   - BTPFunctionDetail.html
   - BTPFunctionMapping.html
   ```

2. **Capture screenshot** menggunakan salah satu cara:
   
   **Opsi A: Full Page Screenshot (Recommended)**
   - Chrome: F12 → Ctrl+Shift+P → ketik "screenshot" → pilih "Capture full size screenshot"
   - Edge: F12 → Ctrl+Shift+P → ketik "screenshot" → pilih "Capture full size screenshot"
   
   **Opsi B: Visible Area**
   - Windows: Win + Shift + S (Snipping Tool)
   - Atau gunakan extension: Awesome Screenshot, Nimbus Screenshot

3. **Simpan screenshot** dengan nama yang jelas:
   ```
   screenshots/
   ├── BTP_Index_Page.png
   ├── BTP_Detail_Form.png
   ├── BTP_Function_Index.png
   ├── BTP_Function_Detail.png
   ├── BTP_Function_Mapping.png
   ├── RM_Category_Index.png
   ├── RM_Category_Detail.png
   ├── RM_SubGroup_Index.png
   ├── Parameter_Index.png
   └── Parameter_Detail.png
   ```

### Langkah 2: Tambahkan ke FSD HTML

Buka file `FSD_Master_BTP.html` dan tambahkan screenshot di section yang sesuai:

```html
<h4>4.1.1 Layout Index BTP</h4>
<p><strong>Screenshot:</strong></p>
<img src="screenshots/BTP_Index_Page.png" alt="BTP Index Page" style="max-width: 100%; border: 1px solid #ccc; margin: 10px 0;">

<p><strong>Fungsi Utama:</strong></p>
<ul>
    <li>Menampilkan daftar semua BTP dalam tabel dengan DataTables</li>
    ...
</ul>
```

### Langkah 3: Tambahkan ke FSD DOCX

Setelah konversi HTML ke DOCX:

1. Buka file DOCX di Microsoft Word
2. Posisikan cursor di tempat yang sesuai (setelah judul section)
3. Insert → Pictures → pilih screenshot
4. Resize gambar (recommended: 80-90% page width)
5. Add caption: "Figure X: BTP Index Page"
6. Format: Center alignment, border optional

## Screenshot yang Dibutuhkan

### Master BTP Module

| No | File HTML | Screenshot Name | Section di FSD |
|----|-----------|-----------------|----------------|
| 1 | BTPIndex.html | BTP_Index_Page.png | 2.1.1 Layout Index BTP |
| 2 | BTPDetail.html | BTP_Detail_Form.png | 2.1.2 Layout Detail BTP |
| 3 | BTPFunctionIndex.html | BTP_Function_Index.png | 2.2.1 Layout Index BTP Function |
| 4 | BTPFunctionDetail.html | BTP_Function_Detail.png | 2.2.2 Layout Detail BTP Function |
| 5 | BTPFunctionMapping.html | BTP_Function_Mapping.png | 2.3.1 Layout BTP Function Mapping |

### Master Data Modules

| No | File HTML | Screenshot Name | Section di FSD |
|----|-----------|-----------------|----------------|
| 1 | MasterUOMIndex.html | UOM_Index_Page.png | 4.5.1 Layout Index Master UOM |
| 2 | MasterUOMDetail.html | UOM_Detail_Form.png | 4.5.2 Layout Detail Master UOM |
| 3 | RMCategoryIndex.html | RM_Category_Index.png | 4.3.1 Layout Index RM Category |
| 4 | RMCategoryDetail.html | RM_Category_Detail.png | 4.3.2 Layout Detail RM Category |
| 5 | RMCategorySubGroupMapping.html | RM_Category_Mapping.png | 4.3.2 Mapping Sub Group |
| 6 | RMSubGroupIndex.html | RM_SubGroup_Index.png | 4.4.1 Layout Index RM Sub Group |
| 7 | RMSubGroupDetail.html | RM_SubGroup_Detail.png | 4.4.2 Layout Detail RM Sub Group |
| 8 | ParameterIndex.html | Parameter_Index.png | Master Parameter Index |
| 9 | ParameterDetail.html | Parameter_Detail.png | Master Parameter Detail |

## Template HTML untuk Screenshot

Tambahkan di FSD HTML sebelum section "Fungsi Utama":

```html
<div class="screenshot-container" style="margin: 20px 0; padding: 10px; background-color: #f9f9f9; border: 1px solid #ddd;">
    <p><strong>📸 Screenshot:</strong></p>
    <img src="screenshots/[NAMA_FILE].png" 
         alt="[DESKRIPSI]" 
         style="max-width: 100%; border: 1px solid #ccc; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <p style="text-align: center; font-size: 10pt; color: #666; margin-top: 5px;">
        <em>Figure: [CAPTION]</em>
    </p>
</div>
```

## Tips Screenshot yang Baik

1. **Resolution**: Minimal 1920x1080 untuk clarity
2. **Full Page**: Capture full page, bukan hanya visible area
3. **Clean State**: 
   - Pastikan data sample terisi
   - Tidak ada error message
   - UI dalam keadaan default/clean
4. **Highlight**: Gunakan annotation tool untuk highlight fitur penting (optional)
5. **Format**: PNG untuk quality, JPG untuk file size

## Automation Script (Optional)

Jika ingin otomatis capture semua screenshot, gunakan Playwright:

```python
# install: pip install playwright
# setup: playwright install

from playwright.sync_api import sync_playwright

def capture_screenshots():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1920, 'height': 1080})
        
        pages = [
            ('BTPIndex.html', 'screenshots/BTP_Index_Page.png'),
            ('BTPDetail.html', 'screenshots/BTP_Detail_Form.png'),
            # ... add more
        ]
        
        for html_file, screenshot_path in pages:
            page.goto(f'file:///d:/Work/Source/RMSelection Hijrah/NewRMSelection/{html_file}')
            page.wait_for_load_state('networkidle')
            page.screenshot(path=screenshot_path, full_page=True)
        
        browser.close()

capture_screenshots()
```

## Checklist

- [ ] Buat folder `screenshots/` di folder FSD
- [ ] Capture screenshot semua halaman prototype
- [ ] Rename screenshot dengan nama yang jelas
- [ ] Tambahkan screenshot ke FSD HTML
- [ ] Konversi HTML ke DOCX
- [ ] Verify screenshot muncul di DOCX
- [ ] Adjust size dan alignment di Word
- [ ] Add figure captions
- [ ] Final review

## Result

Setelah menambahkan screenshot, FSD akan:
- ✅ Lebih visual dan mudah dipahami
- ✅ Menunjukkan UI/UX yang actual
- ✅ Membantu developer understand requirements
- ✅ Mempercepat review process
- ✅ Lebih professional

Selamat mendokumentasikan! 📸
