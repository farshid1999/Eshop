param (
    [Parameter(Mandatory=$true)]
    [string]$RemoteUrl
)

Write-Host "Initializing git repo..." -ForegroundColor Cyan

git init
echo "to read" >> README.md
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin $RemoteUrl
git push -u origin main

Write-Host "Done ✅" -ForegroundColor Green
