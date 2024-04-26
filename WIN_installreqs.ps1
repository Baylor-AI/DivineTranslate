Write-Host "[POWERSHELL] Setting permissions and path. About to install"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
$env:Path += ';C:\Program Files\nodejs'

Write-Host "[CHECK] Checking node and npm is installed"
node -v
npm -v

Write-Host "[INSTALL] Check complete...starting install"
npm install react-scripts --save
Write-Host "[COMPLETE] Installed react-scripts"

npm install bootstrap --save
Write-Host "[COMPLETE] Installed bootstrap"

Write-Host "[POWERSHELL] Powershell is done. Returning to Bash..."