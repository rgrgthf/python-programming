# ============================================
# 恢复 Copilot Chat 聊天记录（工作区重命名后）
# 使用前请完全关闭 VS Code！
# ============================================
$ErrorActionPreference = 'Stop'

$storageRoot = Join-Path $env:APPDATA 'Code\User\workspaceStorage'
$oldHash = '93ff142e24a714fd3c4b83cc31c087ff'   # 旧路径: python程序库
$newHash = '81cd8a3968c5a2d7fe2ef68dd2c073da'   # 新路径: Python药学学习体系
$old = Join-Path $storageRoot $oldHash
$new = Join-Path $storageRoot $newHash

if (Get-Process -Name 'Code' -ErrorAction SilentlyContinue) {
    Write-Host '[错误] VS Code 正在运行，请先完全退出 VS Code 再运行本脚本。' -ForegroundColor Red
    Read-Host '按回车键退出'
    exit 1
}
if (-not (Test-Path $old)) { Write-Host '[错误] 找不到旧聊天记录文件夹。' -ForegroundColor Red; Read-Host '按回车键退出'; exit 1 }
if (-not (Test-Path $new)) { Write-Host '[错误] 找不到新工作区文件夹。' -ForegroundColor Red; Read-Host '按回车键退出'; exit 1 }

# 1. 备份新文件夹当前数据（以防万一）
$backup = Join-Path $new 'backup-before-restore'
if (-not (Test-Path $backup)) { New-Item -ItemType Directory -Path $backup | Out-Null }
Get-ChildItem $new -Force | Where-Object { $_.Name -ne 'workspace.json' -and $_.Name -ne 'backup-before-restore' } | ForEach-Object {
    if ($_.PSIsContainer) {
        Copy-Item (Join-Path $_.FullName '*') (Join-Path $backup $_.Name) -Recurse -Force -ErrorAction SilentlyContinue
    } else {
        Copy-Item $_.FullName (Join-Path $backup $_.Name) -Force -ErrorAction SilentlyContinue
    }
}
Write-Host "[完成] 已备份当前数据 -> $backup" -ForegroundColor Green

# 2. 从旧文件夹复制聊天数据到新文件夹（覆盖）
Get-ChildItem $old -Force | Where-Object { $_.Name -ne 'workspace.json' } | ForEach-Object {
    if ($_.PSIsContainer) {
        $destDir = Join-Path $new $_.Name
        if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir | Out-Null }
        Copy-Item (Join-Path $_.FullName '*') $destDir -Recurse -Force
    } else {
        Copy-Item $_.FullName (Join-Path $new $_.Name) -Force
    }
}

Write-Host ''
Write-Host '============================================' -ForegroundColor Cyan
Write-Host ' 聊天记录恢复完成！' -ForegroundColor Green
Write-Host ' 现在重新打开 VS Code，聊天记录就会回来。' -ForegroundColor Green
Write-Host '============================================' -ForegroundColor Cyan
Read-Host '按回车键退出'
