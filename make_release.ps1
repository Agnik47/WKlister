# Builds the page and packs everything the office laptop needs into releases\Wishkaro_Listing_Tool_<date>.zip
# Run it with make_release.bat on the developer PC (needs Node.js).
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location "$root\frontend"
if (-not (Test-Path node_modules)) { npm install; if ($LASTEXITCODE) { throw 'npm install failed' } }
npm run build
if ($LASTEXITCODE) { throw 'The page build failed. Fix the error above, then run this again.' }

Set-Location $root
$stamp = Get-Date -Format 'yyyy-MM-dd_HHmm'
$name = "Wishkaro_Listing_Tool_$stamp"
$stage = Join-Path $env:TEMP $name
if (Test-Path $stage) { Remove-Item -Recurse -Force $stage }

# leave out: developer-only folders, caches, test output, old templates and this PC's install markers
robocopy $root $stage /E /NFL /NDL /NJH /NJS /NP `
    /XD node_modules __pycache__ test_output releases old .git .claude Listing_Output output `
    /XF '.installed*' '*.zip' | Out-Null
if ($LASTEXITCODE -ge 8) { throw "Copy failed (robocopy code $LASTEXITCODE)" }

New-Item -ItemType Directory -Force "$root\releases" | Out-Null
$zip = "$root\releases\$name.zip"
Compress-Archive -Path "$stage\*" -DestinationPath $zip -Force
Remove-Item -Recurse -Force $stage

$mb = [math]::Round((Get-Item $zip).Length / 1MB, 1)
Write-Host ""
Write-Host "Release ready ($mb MB):" -ForegroundColor Green
Write-Host "  $zip"
Write-Host "Copy it to the office laptop and follow 'Updating the office laptop' in README.md."
