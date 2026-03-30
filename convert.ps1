$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$htmlPath = "D:\AI_Files\徐宁波-简历-优化版.html"
$pdfPath = "D:\AI_Files\徐宁波-简历-优化版.pdf"

$args = @(
    "--headless",
    "--disable-gpu",
    "--no-paint-header",
    "--no-paint-footer",
    "--print-to-pdf=$pdfPath",
    "file:///$($htmlPath.Replace('\', '/'))"
)

$pinfo = Start-Process -FilePath $chrome -ArgumentList $args -PassThru -Wait -NoNewWindow
$pinfo.WaitForExit()

Start-Sleep -Seconds 2

if (Test-Path $pdfPath) {
    Write-Host "SUCCESS"
    Get-Item $pdfPath | Select-Object Name, Length
} else {
    Write-Host "FAILED"
}
