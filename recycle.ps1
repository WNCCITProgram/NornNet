param(
  [string]$PoolName = "NornNetPool"
)

# Require elevation
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
  Write-Error "This script must be run as Administrator."
  exit 1
}

# Clear Python cache
Write-Output "Clearing Python bytecode cache..."
.\clear_bytecode.ps1

Write-Output "Recycling IIS application pool '$PoolName'..."

# Try PowerShell WebAdministration first
try {
  Import-Module WebAdministration -ErrorAction Stop
  Restart-WebAppPool -Name $PoolName -ErrorAction Stop
  Write-Output "Recycle succeeded via Restart-WebAppPool."
  exit 0
} catch {
  Write-Warning "Restart-WebAppPool failed or WebAdministration not available: $($_.Exception.Message)"
}

# Fallback to appcmd.exe
$appcmd = Join-Path $env:windir "system32\inetsrv\appcmd.exe"
if (Test-Path $appcmd) {
  & $appcmd recycle apppool /apppool.name:"$PoolName"
  if ($LASTEXITCODE -eq 0) {
    Write-Output "Recycle succeeded via appcmd."
    exit 0
  } else {
    Write-Error "appcmd failed with exit code $LASTEXITCODE."
    exit $LASTEXITCODE
  }
} else {
  Write-Error "appcmd.exe not found at $appcmd. Cannot recycle application pool."
  exit 2
}
