# Template Modul FSD

**Jangan build langsung dari folder ini.** Salin ke modul baru:

```powershell
cd "D:\Work\Source\FSD Generator Engine\modules"
Copy-Item -Recurse _template my-new-module
cd my-new-module
# Edit build.py + source/FSD_TEMPLATE.md
py build.py
```

Panduan lengkap: `docs/AI-START-HERE.md`
