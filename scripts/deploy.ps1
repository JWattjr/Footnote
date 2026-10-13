param([string]$Step='deploy')
$ErrorActionPreference='Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
$generated=Join-Path (Get-Location) 'deploy/deployScript.compiled.js'
if(Test-Path -LiteralPath $generated){Remove-Item -LiteralPath $generated}
$previousNodeOptions=$env:NODE_OPTIONS
try {
  $env:FOOTNOTE_STEP=$Step
  $env:NODE_OPTIONS=($previousNodeOptions+' --import=tsx').Trim()
  genlayer deploy
  if($LASTEXITCODE -ne 0){throw "Step stopped; inspect the output above. Resume any persisted transaction hash without resubmitting it."}
} finally {
  $env:NODE_OPTIONS=$previousNodeOptions
  if(Test-Path -LiteralPath $generated){Remove-Item -LiteralPath $generated}
}
