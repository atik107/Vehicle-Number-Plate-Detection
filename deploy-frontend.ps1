# Quick Deploy to GitHub Pages
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Deploying Frontend to GitHub Pages" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to frontend
cd frontend

# Check if gh-pages is installed
Write-Host "Installing deployment dependencies..." -ForegroundColor Yellow
npm install --save-dev gh-pages

Write-Host ""
Write-Host "Building production version..." -ForegroundColor Yellow
npm run build

Write-Host ""
Write-Host "Deploying to GitHub Pages..." -ForegroundColor Green
npm run deploy

Write-Host ""
Write-Host "======================================" -ForegroundColor Green
Write-Host "✓ Deployment Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your site will be available at:" -ForegroundColor Cyan
Write-Host "https://atik107.github.io/Vehicle-Number-Plate-Detection" -ForegroundColor Yellow
Write-Host ""
Write-Host "Note: It may take a few minutes for changes to appear." -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Go to GitHub repo Settings → Pages" -ForegroundColor White
Write-Host "2. Ensure source is set to 'gh-pages' branch" -ForegroundColor White
Write-Host "3. Deploy backend to Render/Railway" -ForegroundColor White
Write-Host "4. Update REACT_APP_API_URL with backend URL" -ForegroundColor White
Write-Host ""
