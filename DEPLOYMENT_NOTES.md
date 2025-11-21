# Important Notes for Deployment

## For Vercel Deployment

When deploying to Vercel, the `homepage` field in `frontend/package.json` should be removed or commented out. This field is specifically for GitHub Pages deployment and will cause routing issues on Vercel.

### Option 1: Comment out homepage (Recommended)
Edit `frontend/package.json`:
```json
{
  "name": "vehicle-detection-frontend",
  ...
  // "homepage": "https://atik107.github.io/Vehicle-Number-Plate-Detection",
  ...
}
```

### Option 2: Remove homepage field
Simply delete the line from `package.json`.

### Option 3: Use environment-specific builds
Keep the homepage field but build without it for Vercel:
```bash
# For Vercel (root path)
PUBLIC_URL=/ npm run build

# For GitHub Pages (with subdirectory)
npm run build
```

## For GitHub Pages Deployment

Keep the `homepage` field as-is in `frontend/package.json`:
```json
"homepage": "https://atik107.github.io/Vehicle-Number-Plate-Detection"
```

This ensures assets are loaded from the correct path when deployed to GitHub Pages.

## Current Configuration

The repository is currently configured for **both** deployment options:
- **Vercel**: Use the root `vercel.json` which builds from frontend directory
- **GitHub Pages**: Use the existing `homepage` field and `npm run deploy` script

### To deploy to Vercel:
1. The `vercel.json` at root handles the build correctly
2. Vercel will ignore the `homepage` field if you set the root directory to `frontend`
3. No changes needed to package.json

### To deploy to GitHub Pages:
1. Use the existing setup with `homepage` field
2. Run `npm run deploy` from the frontend directory
3. Works as currently configured

## Summary

✅ **For Vercel**: No changes needed! The root `vercel.json` handles everything.  
✅ **For GitHub Pages**: No changes needed! The current setup works.

Both deployment methods are supported with the current configuration.
