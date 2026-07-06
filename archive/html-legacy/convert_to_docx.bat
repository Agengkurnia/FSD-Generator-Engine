@echo off
REM Batch script untuk konversi FSD HTML ke DOCX menggunakan Pandoc
REM Pastikan Pandoc sudah terinstall dan ada di PATH

echo ============================================================
echo FSD HTML to DOCX Converter (Batch Version)
echo ============================================================
echo.

REM Check if pandoc is installed
where pandoc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Pandoc tidak ditemukan!
    echo.
    echo Silakan install Pandoc terlebih dahulu:
    echo   1. Download dari: https://pandoc.org/installing.html
    echo   2. Install dan restart terminal
    echo   3. Jalankan script ini lagi
    echo.
    pause
    exit /b 1
)

echo Pandoc ditemukan! Memulai konversi...
echo.

REM Convert FSD_Master_BTP.html
if exist "FSD_Master_BTP.html" (
    echo [1/3] Converting FSD_Master_BTP.html...
    pandoc "FSD_Master_BTP.html" -o "FSD_Master_BTP.docx" --toc --toc-depth=3
    if %ERRORLEVEL% EQU 0 (
        echo       SUCCESS: FSD_Master_BTP.docx
    ) else (
        echo       FAILED: FSD_Master_BTP.html
    )
    echo.
)

REM Convert FSD_Master_Data.html
if exist "FSD_Master_Data.html" (
    echo [2/3] Converting FSD_Master_Data.html...
    pandoc "FSD_Master_Data.html" -o "FSD_Master_Data.docx" --toc --toc-depth=3
    if %ERRORLEVEL% EQU 0 (
        echo       SUCCESS: FSD_Master_Data.docx
    ) else (
        echo       FAILED: FSD_Master_Data.html
    )
    echo.
)

REM Convert FSD_Draft_Import.html
if exist "FSD_Draft_Import.html" (
    echo [3/3] Converting FSD_Draft_Import.html...
    pandoc "FSD_Draft_Import.html" -o "FSD_Draft_Import.docx" --toc --toc-depth=3
    if %ERRORLEVEL% EQU 0 (
        echo       SUCCESS: FSD_Draft_Import.docx
    ) else (
        echo       FAILED: FSD_Draft_Import.html
    )
    echo.
)

echo ============================================================
echo Konversi selesai!
echo ============================================================
echo.
echo File DOCX telah dibuat di folder ini.
echo Silakan buka dengan Microsoft Word untuk review.
echo.
pause
