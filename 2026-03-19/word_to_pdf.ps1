$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("D:\AI_Files\2026-03-19\徐宁波-简历-优化版.docx")
$doc.SaveAs([ref]"D:\AI_Files\2026-03-19\徐宁波-简历-优化版.pdf", [ref]17)
$doc.Close()
$word.Quit()
Write-Host "PDF转换成功！"
