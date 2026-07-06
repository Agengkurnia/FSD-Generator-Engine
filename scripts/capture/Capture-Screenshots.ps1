# ============================================================================
# AUTOMATED SCREENSHOT SCRIPT FOR NEW RM SAMPLE MANAGEMENT
# ============================================================================

param(
    [string]$Browser = "Chrome",
    [string]$OutputFolder = "Screenshots",
    [int]$WaitTime = 2000
)

# Configuration
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)
$IndexPage = Join-Path $ProjectRoot "NewRMSampleIndex.html"
$DetailPage = Join-Path $ProjectRoot "NewRMSampleDetail.html"
$OutputPath = Join-Path $ScriptDir $OutputFolder

# Create output folder
if (-not (Test-Path $OutputPath)) {
    New-Item -ItemType Directory -Path $OutputPath | Out-Null
    Write-Host "Created output folder: $OutputPath" -ForegroundColor Green
}

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "NEW RM SAMPLE MANAGEMENT - AUTOMATED SCREENSHOT TOOL" -ForegroundColor Cyan
Write-Host "============================================================================`n" -ForegroundColor Cyan

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Browser      : $Browser"
Write-Host "  Index Page   : $IndexPage"
Write-Host "  Detail Page  : $DetailPage"
Write-Host "  Output Folder: $OutputPath"
Write-Host "  Wait Time    : $WaitTime ms`n"

# Check if Selenium is installed
Write-Host "Checking Selenium WebDriver..." -ForegroundColor Yellow
try {
    Import-Module Selenium -ErrorAction Stop
    Write-Host "  OK Selenium module found" -ForegroundColor Green
}
catch {
    Write-Host "  X Selenium module not found. Installing..." -ForegroundColor Red
    Write-Host "  Installing Selenium PowerShell module..." -ForegroundColor Yellow
    Install-Module -Name Selenium -Force -Scope CurrentUser
    Import-Module Selenium
    Write-Host "  OK Selenium module installed" -ForegroundColor Green
}

# Initialize WebDriver
Write-Host "`nInitializing WebDriver..." -ForegroundColor Yellow
try {
    if ($Browser -eq "Edge") {
        $Driver = Start-SeEdge
        Write-Host "  OK Edge WebDriver initialized" -ForegroundColor Green
    }
    else {
        $Driver = Start-SeChrome
        Write-Host "  OK Chrome WebDriver initialized" -ForegroundColor Green
    }
    
    $Driver.Manage().Window.Maximize()
    Write-Host "  OK Browser window maximized" -ForegroundColor Green
}
catch {
    Write-Host "  X Failed to initialize WebDriver: $_" -ForegroundColor Red
    Write-Host "`nPlease ensure $Browser is installed and WebDriver is available." -ForegroundColor Red
    exit 1
}

# Helper function to take screenshot
function Take-Screenshot {
    param(
        [string]$FileName,
        [string]$Description
    )
    
    $FilePath = Join-Path $OutputPath "$FileName.png"
    
    try {
        Start-Sleep -Milliseconds $WaitTime
        $Screenshot = $Driver.GetScreenshot()
        $Screenshot.SaveAsFile($FilePath, [OpenQA.Selenium.ScreenshotImageFormat]::Png)
        Write-Host "  OK $Description" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "  X Failed: $Description - $_" -ForegroundColor Red
        return $false
    }
}

# Helper function to expand all accordions
function Expand-AllAccordions {
    try {
        $Script = "document.querySelectorAll('.collapse').forEach(function(el) { el.classList.add('show'); }); document.querySelectorAll('[data-bs-toggle=collapse]').forEach(function(btn) { btn.setAttribute('aria-expanded', 'true'); btn.classList.remove('collapsed'); }); document.querySelectorAll('details').forEach(function(el) { el.open = true; });"
        $Driver.ExecuteScript($Script)
        Start-Sleep -Milliseconds 500
    }
    catch {
        Write-Host "  Warning: Could not expand accordions" -ForegroundColor Yellow
    }
}

# Helper function to click element safely
function Click-Element {
    param([string]$Selector)
    
    try {
        $Element = $Driver.FindElementByCssSelector($Selector)
        $Element.Click()
        Start-Sleep -Milliseconds 500
        return $true
    }
    catch {
        Write-Host "  Warning: Could not click element: $Selector" -ForegroundColor Yellow
        return $false
    }
}

# Counter for screenshots
$ScreenshotCount = 0
$SuccessCount = 0

Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "CAPTURING SCREENSHOTS" -ForegroundColor Cyan
Write-Host "============================================================================`n" -ForegroundColor Cyan

# INDEX PAGE SCREENSHOTS
Write-Host "[1/2] NewRMSampleIndex.html" -ForegroundColor Cyan

try {
    $Driver.Navigate().GoToUrl("file:///$($IndexPage -replace '\\', '/')")
    Start-Sleep -Milliseconds $WaitTime
    Expand-AllAccordions
    
    $ScreenshotCount++
    if (Take-Screenshot "01_Index_Dashboard" "Screenshot $ScreenshotCount/22: Index Dashboard") {
        $SuccessCount++
    }
    
    $Driver.ExecuteScript("window.scrollTo(0, document.body.scrollHeight / 2);")
    Start-Sleep -Milliseconds 500
    
    $ScreenshotCount++
    if (Take-Screenshot "02_Index_DataTable" "Screenshot $ScreenshotCount/22: Index DataTable") {
        $SuccessCount++
    }
}
catch {
    Write-Host "  X Error loading Index page: $_" -ForegroundColor Red
}

# DETAIL PAGE SCREENSHOTS
Write-Host "`n[2/2] NewRMSampleDetail.html" -ForegroundColor Cyan

try {
    $Driver.Navigate().GoToUrl("file:///$($DetailPage -replace '\\', '/')")
    Start-Sleep -Milliseconds $WaitTime
    Expand-AllAccordions
    
    # STEP 1
    Write-Host "`n  Step 1: Document" -ForegroundColor Yellow
    $Driver.ExecuteScript("window.scrollTo(0, 0);")
    
    $ScreenshotCount++
    if (Take-Screenshot "03_Detail_Step1_Header" "Screenshot $ScreenshotCount/22: Step 1 - Header") {
        $SuccessCount++
    }
    
    $Driver.ExecuteScript("window.scrollBy(0, 400);")
    Start-Sleep -Milliseconds 300
    
    $ScreenshotCount++
    if (Take-Screenshot "04_Detail_Step1_Materials" "Screenshot $ScreenshotCount/22: Step 1 - Materials") {
        $SuccessCount++
    }
    
    $Driver.ExecuteScript("window.scrollBy(0, 400);")
    Start-Sleep -Milliseconds 300
    
    $ScreenshotCount++
    if (Take-Screenshot "05_Detail_Step1_Allergen" "Screenshot $ScreenshotCount/22: Step 1 - Allergen") {
        $SuccessCount++
    }
    
    $Driver.ExecuteScript("window.scrollBy(0, 400);")
    Start-Sleep -Milliseconds 300
    
    $ScreenshotCount++
    if (Take-Screenshot "06_Detail_Step1_BTP" "Screenshot $ScreenshotCount/22: Step 1 - BTP") {
        $SuccessCount++
    }
    
    $Driver.ExecuteScript("window.scrollBy(0, 400);")
    Start-Sleep -Milliseconds 300
    
    $ScreenshotCount++
    if (Take-Screenshot "07_Detail_Step1_Documents" "Screenshot $ScreenshotCount/22: Step 1 - Documents") {
        $SuccessCount++
    }
    
    # STEP 2
    Write-Host "`n  Step 2: Purpose" -ForegroundColor Yellow
    Click-Element "#btnNext"
    Start-Sleep -Milliseconds $WaitTime
    Expand-AllAccordions
    $Driver.ExecuteScript("window.scrollTo(0, 0);")
    
    $ScreenshotCount++
    if (Take-Screenshot "08_Detail_Step2_Category" "Screenshot $ScreenshotCount/22: Step 2 - Category") {
        $SuccessCount++
    }
    
    $Driver.ExecuteScript("window.scrollBy(0, 400);")
    Start-Sleep -Milliseconds 300
    
    $ScreenshotCount++
    if (Take-Screenshot "09_Detail_Step2_Items" "Screenshot $ScreenshotCount/22: Step 2 - Items") {
        $SuccessCount++
    }
    
    $Driver.ExecuteScript("window.scrollBy(0, 400);")
    Start-Sleep -Milliseconds 300
    
    $ScreenshotCount++
    if (Take-Screenshot "10_Detail_Step2_Products" "Screenshot $ScreenshotCount/22: Step 2 - Products") {
        $SuccessCount++
    }
    
    # STEP 3
    Write-Host "`n  Step 3: Evaluation" -ForegroundColor Yellow
    Click-Element "#btnNext"
    Start-Sleep -Milliseconds $WaitTime
    Expand-AllAccordions
    $Driver.ExecuteScript("window.scrollTo(0, 0);")
    
    $ScreenshotCount++
    if (Take-Screenshot "11_Detail_Step3_Organoleptic" "Screenshot $ScreenshotCount/22: Step 3 - Organoleptic") {
        $SuccessCount++
    }
    
    Click-Element "a[href='#nutrition-tab']"
    Start-Sleep -Milliseconds 500
    $ScreenshotCount++
    if (Take-Screenshot "12_Detail_Step3_Nutrition" "Screenshot $ScreenshotCount/22: Step 3 - Nutrition") {
        $SuccessCount++
    }
    
    Click-Element "a[href='#microbiological-tab']"
    Start-Sleep -Milliseconds 500
    $ScreenshotCount++
    if (Take-Screenshot "13_Detail_Step3_Microbiological" "Screenshot $ScreenshotCount/22: Step 3 - Microbiological") {
        $SuccessCount++
    }
    
    Click-Element "a[href='#heavymetals-tab']"
    Start-Sleep -Milliseconds 500
    $ScreenshotCount++
    if (Take-Screenshot "14_Detail_Step3_HeavyMetals" "Screenshot $ScreenshotCount/22: Step 3 - Heavy Metals") {
        $SuccessCount++
    }
    
    Click-Element "a[href='#othercontaminant-tab']"
    Start-Sleep -Milliseconds 500
    $ScreenshotCount++
    if (Take-Screenshot "15_Detail_Step3_OtherContaminant" "Screenshot $ScreenshotCount/22: Step 3 - Other Contaminant") {
        $SuccessCount++
    }
    
    Click-Element "a[href='#foodcategory-tab']"
    Start-Sleep -Milliseconds 500
    $ScreenshotCount++
    if (Take-Screenshot "16_Detail_Step3_FoodCategory" "Screenshot $ScreenshotCount/22: Step 3 - Food Category") {
        $SuccessCount++
    }
    
    # STEP 4
    Write-Host "`n  Step 4: Disposition" -ForegroundColor Yellow
    Click-Element "#btnNext"
    Start-Sleep -Milliseconds $WaitTime
    Expand-AllAccordions
    $Driver.ExecuteScript("window.scrollTo(0, 0);")
    
    $ScreenshotCount++
    if (Take-Screenshot "17_Detail_Step4_Disposition" "Screenshot $ScreenshotCount/22: Step 4 - Disposition") {
        $SuccessCount++
    }
    
    $Driver.ExecuteScript("window.scrollTo(0, document.body.scrollHeight);")
    Start-Sleep -Milliseconds 300
    
    $ScreenshotCount++
    if (Take-Screenshot "18_Detail_Step4_Actions" "Screenshot $ScreenshotCount/22: Step 4 - Actions") {
        $SuccessCount++
    }
    
    # MODALS
    Write-Host "`n  Modals" -ForegroundColor Yellow
    $Driver.Navigate().GoToUrl("file:///$($DetailPage -replace '\\', '/')")
    Start-Sleep -Milliseconds $WaitTime
    
    if (Click-Element "button[data-bs-target='#addAttachmentModal']") {
        Start-Sleep -Milliseconds 500
        $ScreenshotCount++
        if (Take-Screenshot "19_Modal_AddDocument" "Screenshot $ScreenshotCount/22: Modal - Add Document") {
            $SuccessCount++
        }
        $Driver.ExecuteScript("document.querySelector('#addAttachmentModal .btn-close').click();")
        Start-Sleep -Milliseconds 500
    }
    
    if (Click-Element "button[data-bs-target='#lovTypeModal']") {
        Start-Sleep -Milliseconds 500
        $ScreenshotCount++
        if (Take-Screenshot "20_Modal_LOV_TypeDocument" "Screenshot $ScreenshotCount/22: Modal - LOV Type") {
            $SuccessCount++
        }
        $Driver.ExecuteScript("document.querySelector('#lovTypeModal .btn-close').click();")
        Start-Sleep -Milliseconds 500
    }
    
    if (Click-Element "button[data-bs-target='#lovCurrencyModal']") {
        Start-Sleep -Milliseconds 500
        $ScreenshotCount++
        if (Take-Screenshot "21_Modal_LOV_Currency" "Screenshot $ScreenshotCount/22: Modal - LOV Currency") {
            $SuccessCount++
        }
        $Driver.ExecuteScript("document.querySelector('#lovCurrencyModal .btn-close').click();")
        Start-Sleep -Milliseconds 500
    }
    
    if (Click-Element "button[data-bs-target='#lovUOMModal']") {
        Start-Sleep -Milliseconds 500
        $ScreenshotCount++
        if (Take-Screenshot "22_Modal_LOV_UOM" "Screenshot $ScreenshotCount/22: Modal - LOV UOM") {
            $SuccessCount++
        }
    }
}
catch {
    Write-Host "  X Error during screenshot capture: $_" -ForegroundColor Red
}

# CLEANUP
Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "CLEANUP" -ForegroundColor Cyan
Write-Host "============================================================================`n" -ForegroundColor Cyan

try {
    $Driver.Quit()
    Write-Host "  OK Browser closed" -ForegroundColor Green
}
catch {
    Write-Host "  X Error closing browser: $_" -ForegroundColor Red
}

# SUMMARY
Write-Host "`n============================================================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================================`n" -ForegroundColor Cyan

Write-Host "Total Screenshots Attempted: $ScreenshotCount/22" -ForegroundColor Yellow
Write-Host "Successfully Captured      : $SuccessCount/22" -ForegroundColor Green
Write-Host "Failed                     : $($ScreenshotCount - $SuccessCount)/22" -ForegroundColor Red
Write-Host "`nOutput Folder: $OutputPath" -ForegroundColor Cyan

if ($SuccessCount -eq 22) {
    Write-Host "`nALL SCREENSHOTS CAPTURED SUCCESSFULLY!" -ForegroundColor Green
}
elseif ($SuccessCount -gt 0) {
    Write-Host "`nPARTIAL SUCCESS - Some screenshots may need manual capture" -ForegroundColor Yellow
}
else {
    Write-Host "`nFAILED - Please check error messages above" -ForegroundColor Red
}

Write-Host "`n============================================================================`n" -ForegroundColor Cyan
