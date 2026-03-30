$localPath = 'g:\dev\sw-auto-redeem'
$remotePath = '\\192.168.0.14\固态盘\docker\sw-auto-redeem'

$localFiles = Get-ChildItem $localPath -File | Where-Object { $_.Name -notmatch '\.(log|log\.\d+)$' } | Sort-Object Name
$remoteFiles = Get-ChildItem $remotePath -File | Where-Object { $_.Name -notmatch '\.(log|log\.\d+)$' } | Sort-Object Name

Write-Host "=== 本地独有文件 ===" -ForegroundColor Green
$localOnly = $localFiles | Where-Object { $_.Name -notin $remoteFiles.Name }
foreach ($f in $localOnly) {
    Write-Host $f.Name
}

Write-Host "`n=== 远程独有文件 ===" -ForegroundColor Yellow
$remoteOnly = $remoteFiles | Where-Object { $_.Name -notin $localFiles.Name }
foreach ($f in $remoteOnly) {
    Write-Host $f.Name
}

Write-Host "`n=== 文件内容差异 ===" -ForegroundColor Cyan
$commonFiles = $localFiles | Where-Object { $_.Name -in $remoteFiles.Name }
foreach ($file in $commonFiles) {
    $localContent = Get-Content "$localPath\$($file.Name)" -Raw
    $remoteContent = Get-Content "$remotePath\$($file.Name)" -Raw
    if ($localContent -ne $remoteContent) {
        Write-Host "差异: $($file.Name)"
    }
}
