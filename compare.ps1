$localPath = "g:\dev\sw-auto-redeem"
$remotePath = "\\192.168.0.14\固态盘\docker\sw-auto-redeem"

$localFiles = Get-ChildItem $localPath -File | Where-Object { $_.Name -notmatch '\.(log|log\.\d+)$' } | Select-Object -ExpandProperty Name
$remoteFiles = Get-ChildItem $remotePath -File | Where-Object { $_.Name -notmatch '\.(log|log\.\d+)$' } | Select-Object -ExpandProperty Name

Write-Host "=== 本地独有文件 ===" -ForegroundColor Green
Compare-Object $localFiles $remoteFiles | Where-Object { $_.SideIndicator -eq '<=' } | Select-Object -ExpandProperty InputObject

Write-Host "`n=== 远程独有文件 ===" -ForegroundColor Yellow
Compare-Object $localFiles $remoteFiles | Where-Object { $_.SideIndicator -eq '=>' } | Select-Object -ExpandProperty InputObject

Write-Host "`n=== 文件内容差异 ===" -ForegroundColor Cyan
$commonFiles = $localFiles | Where-Object { $_ -in $remoteFiles }
foreach ($file in $commonFiles) {
    $localContent = Get-Content "$localPath\$file" -Raw
    $remoteContent = Get-Content "$remotePath\$file" -Raw
    if ($localContent -ne $remoteContent) {
        Write-Host "差异: $file"
    }
}
