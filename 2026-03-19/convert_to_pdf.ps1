# Convert HTML to PDF using Chrome
$htmlPath = "C:\Users\29210\.openclaw\workspace\徐宁波-简历.html"
$pdfPath = "C:\Users\29210\.openclaw\workspace\徐宁波-简历.pdf"

# Find Chrome
$chrome = "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chrome)) {
    $chrome = "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
}

Write-Host "Chrome path: $chrome"
Write-Host "HTML path: $htmlPath"
Write-Host "PDF path: $pdfPath"

# Use Chrome headless to print to PDF
& $chrome --headless --disable-gpu --print-to-pdf="$pdfPath" --no-paint-header --no-paint-footer --run-all-compositor-stages-before-draw "file:///$($htmlPath.Replace('\', '/'))"
Start-Sleep -Seconds 3

if (Test-Path $pdfPath) {
    Write-Host "PDF created successfully!"
    Get-Item $pdfPath
} else {
    Write-Host "PDF creation failed"
}
