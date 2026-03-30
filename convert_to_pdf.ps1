$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$htmlPath = "D:\AI_Files\徐宁波-简历-优化版.html"
$pdfPath = "D:\AI_Files\徐宁波-简历-优化版.pdf"

Write-Host "Chrome: $chrome"
Write-Host "HTML: $htmlPath"
Write-Host "PDF: $pdfPath"

$args = @(
    "--headless",
    "--disable-gpu",
    "--no-paint-header",
    "--no-paint-footer",
    "--print-to-pdf=`"$pdfPath`"",
    "file:///$($htmlPath.Replace('\', '/'))"
)

Write-Host "Args: $args"

& $chrome @args

Start-Sleep -Seconds 3

if (Test-Path $pdfPath) {
    Write-Host "SUCCESS: PDF created"
    Get-Item $pdfPath
} else {
    Write-Host "FAILED: PDF not created"
}
