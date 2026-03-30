$localFiles = Get-ChildItem 'g:\dev\sw-auto-redeem' -File | Where-Object { $_.Name -notmatch '\.(log|log\.\d+)$' } | Sort-Object Name
$remoteFiles = Get-ChildItem '\\192.168.0.14\固态盘\docker\sw-auto-redeem' -File | Where-Object { $_.Name -notmatch '\.(log|log\.\d+)$' } | Sort-Object Name

Write-Host "=== 本地独有文件 ===" -ForegroundColor Green
$localOnly = $localFiles | Where-Object { $_.Name -notin $remoteFiles.Name }
$localOnly | ForEach-Object { Write-Host $_.Name }

Write-Host "`n=== 远程独有文件 ===" -ForegroundColor Yellow
$remoteOnly = $remoteFiles | Where-Object { $_.Name -notin $localFiles.Name }
$remoteOnly | ForEach-Object { Write-Host $_.Name }

Write-Host "`n=== 文件内容差异 ===" -ForegroundColor Cyan
$commonFiles = $localFiles | Where-Object { $_.Name -in $remoteFiles.Name }
foreach ($file in $commonFiles) {
    $localPath = "g:\dev\sw-auto-redeem\$($file.Name)"
    $remotePath = "\\192.168.0.14\固态盘\docker\sw-auto-redeem\$($file.Name)"
    if (Test-Path $remotePath) {
        $localContent = Get-Content $localPath -Raw
        $remoteContent = Get-Content $remotePath -Raw
        if ($localContent -ne $remoteContent) {
            Write-Host "差异: $($file.Name)" -ForegroundColor Red
        }
    }
}
