# Tải package BRMods từ GitHub release về %APPDATA%\BRMods\pkg
# Sửa REPO thành repo của bạn rồi chạy: powershell -ExecutionPolicy Bypass -File download.ps1
$REPO = "hoanganh-alex/BRMODS"
$TAG = "v1"
$DIR = "$env:APPDATA\BRMods\pkg"
$FILES = @("ok.dll", "minduin.dll", "brmod_loader.dll", "inject_all.py")

New-Item -ItemType Directory -Path $DIR -Force | Out-Null
foreach ($f in $FILES) {
  $url = "https://github.com/$REPO/releases/download/$TAG/$f"
  $out = Join-Path $DIR $f
  Write-Host "GET $url"
  Invoke-WebRequest -Uri $url -OutFile $out
  Write-Host ("OK {0} {1} bytes" -f $f, (Get-Item $out).Length)
}
Write-Host "Xong. Chay admin: python $DIR\inject_all.py"
