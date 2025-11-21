# 🚀 Vercel Deployment Guide

## Overview

This guide explains how to deploy the Vehicle Number Plate Detection system to Vercel.

**Architecture:**
- **Frontend**: Deployed to Vercel (React app)
- **Backend**: Deployed to Render/Railway (FastAPI with ML models)

**Why this split?**
Vercel is optimized for frontend applications and serverless functions. The backend uses heavy ML models (YOLOv8, EasyOCR) that require:
- Large model files (~300MB+)
- Python dependencies with system libraries (OpenCV, PyTorch)
- Longer processing times than Vercel's serverless timeout allows

Therefore, we deploy the frontend to Vercel and the backend to a Python-friendly platform.

---

## Step 1: Deploy Backend to Render

**Why Render?**
- Free tier with 750 hours/month
- Supports Python and Docker
- No timeout limits for processing
- Easy GitHub integration

### Instructions:

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `atik107/Vehicle-Number-Plate-Detection`
   - Click "Connect"

3. **Configure the Service**
   ```
   Name: vehicle-detection-api
   Region: Choose closest to your location (e.g., Oregon USA)
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Advanced Settings (Optional)**
   ```
   Environment Variables:
   - PYTHON_VERSION: 3.11.0
   
   Health Check Path: /health
   ```

5. **Create Web Service**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first deployment
   - Note your backend URL (e.g., `https://vehicle-detection-api-xxx.onrender.com`)

6. **Test Backend**
   - Visit: `https://your-backend-url.onrender.com/health`
   - You should see: `{"status": "healthy"}`
   - API Docs: `https://your-backend-url.onrender.com/docs`

---

## Step 2: Deploy Frontend to Vercel

### Method 1: Using Vercel Dashboard (Recommended)

1. **Sign up for Vercel**
   - Go to https://vercel.com
   - Sign up with your GitHub account

2. **Import Project**
   - Click "Add New..." → "Project"
   - Select your repository: `Vehicle-Number-Plate-Detection`
   - Click "Import"

3. **Configure Project**
   ```
   Framework Preset: Create React App (auto-detected)
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. **Add Environment Variables**
   - Click "Environment Variables"
   - Add the following:
     ```
     Name: REACT_APP_API_URL
     Value: https://your-backend-url.onrender.com
     ```
   - Make sure to use your actual backend URL from Step 1

5. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build and deployment
   - Your site will be live at: `https://vehicle-number-plate-detection.vercel.app`
   - (Or custom domain if configured)

### Method 2: Using Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Navigate to Frontend**
   ```bash
   cd frontend
   ```

4. **Set Environment Variable**
   Create `.env.production.local`:
   ```env
   REACT_APP_API_URL=https://your-backend-url.onrender.com
   ```

5. **Deploy**
   ```bash
   vercel --prod
   ```

6. **Set Environment Variable in Vercel Dashboard**
   - Go to your project settings on vercel.com
   - Add `REACT_APP_API_URL` environment variable
   - Redeploy if needed

---

## Step 3: Update Backend CORS Settings

After deploying the frontend, you need to update the backend to allow requests from your Vercel domain.

1. **Get Your Vercel URL**
   - From Vercel dashboard: `https://your-app.vercel.app`

2. **Update Backend CORS** (if needed)
   - The backend is already configured to allow all origins (`"*"`)
   - For production, you may want to restrict to specific domains
   - Edit `backend/main.py` and update the `allowed_origins` list
   - Redeploy to Render

---

## Step 4: Test Your Deployment

1. **Visit Your Frontend**
   - Go to: `https://your-app.vercel.app`

2. **Test Upload**
   - Try uploading an image
   - Click "Detect Vehicles"
   - Wait for results (first request may take longer due to Render cold start)

3. **Check for Errors**
   - Open browser DevTools (F12)
   - Check Console for any errors
   - Verify API calls are going to correct backend URL

---

## Configuration Files

The following files are configured for Vercel deployment:

### Root `vercel.json`
```json
{
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/build",
  "framework": null,
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Frontend `vercel.json`
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

### Frontend `.env.production`
```env
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

---

## Automatic Deployments

Once configured, both platforms will auto-deploy on git push:

- **Vercel**: Deploys on every push to `main` branch
- **Render**: Deploys on every push to `main` branch

To disable auto-deploy, adjust settings in respective dashboards.

---

## Custom Domain (Optional)

### For Vercel:
1. Go to Project Settings → Domains
2. Add your custom domain
3. Configure DNS records as instructed
4. Wait for SSL certificate provisioning

### For Render:
1. Go to Service Settings → Custom Domain
2. Add your custom domain
3. Configure DNS records
4. SSL certificate auto-provisions

---

## Environment Variables Reference

### Frontend (Vercel)
| Variable | Value | Description |
|----------|-------|-------------|
| `REACT_APP_API_URL` | `https://your-backend.onrender.com` | Backend API URL |

### Backend (Render)
| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.11.0` | Python version (optional) |
| `PORT` | Auto-set by Render | Server port |

---

## Troubleshooting

### Frontend Issues

**Issue: "Failed to fetch" error**
- **Cause**: Backend URL not configured or incorrect
- **Solution**: Check `REACT_APP_API_URL` in Vercel environment variables
- **Test**: Visit backend URL directly in browser

**Issue: Build fails on Vercel**
- **Cause**: Missing dependencies or build errors
- **Solution**: Check Vercel build logs
- **Fix**: Ensure `package.json` has all dependencies

**Issue: App shows but doesn't work**
- **Cause**: Environment variable not loaded
- **Solution**: Redeploy after setting environment variables
- **Note**: Environment variables require redeploy to take effect

### Backend Issues

**Issue: Backend timeout on first request**
- **Cause**: Render free tier sleeps after 15 minutes of inactivity
- **Solution**: First request takes 30-60 seconds to wake up
- **Workaround**: Keep-alive service or upgrade to paid tier

**Issue: Model download timeout**
- **Cause**: Models download on first request (~300MB)
- **Solution**: Build time may exceed free tier limits
- **Fix**: Consider paid tier or pre-downloaded models in Docker image

**Issue: Out of memory**
- **Cause**: ML models require significant RAM
- **Solution**: Free tier has 512MB RAM limit
- **Fix**: Upgrade to paid tier with more memory

### CORS Issues

**Issue: CORS error in browser**
- **Cause**: Backend not allowing frontend origin
- **Solution**: Backend already allows all origins (`"*"`)
- **Check**: Verify backend is actually running and accessible

---

## Cost Breakdown

### Free Tier (Recommended for Testing)
- **Vercel**: Free (Generous limits for personal projects)
  - 100 GB bandwidth
  - 100 GB-hours compute time
  - Unlimited websites
  
- **Render**: Free
  - 750 hours/month (31 days)
  - 512 MB RAM
  - Auto-sleep after 15 min inactivity
  
**Total: $0/month**

### Paid Tier (For Production)
- **Vercel Pro**: $20/month
  - Unlimited bandwidth
  - Custom domains
  - Analytics
  
- **Render Starter**: $7/month
  - Always-on (no sleep)
  - Better memory limits
  - Custom domain
  
**Total: $27/month**

---

## Performance Tips

1. **Backend Cold Start**
   - First request after sleep: 30-60 seconds
   - Keep backend alive with cron job (https://cron-job.org)
   - Or upgrade to paid tier for always-on

2. **Image Size**
   - Compress images before upload for faster processing
   - Backend processes images efficiently

3. **Caching**
   - Vercel automatically caches static assets
   - API responses are not cached by default

---

## Monitoring

### Vercel
- Dashboard → Your Project → Analytics
- Real-time deployment logs
- Performance metrics

### Render
- Dashboard → Your Service → Logs
- Real-time application logs
- Metrics and health checks

---

## CI/CD Pipeline

Both platforms automatically deploy on git push:

1. Push code to GitHub
2. Vercel detects change → builds frontend → deploys
3. Render detects change → builds backend → deploys
4. Both deployments complete in 2-5 minutes

---

## Next Steps

After successful deployment:

1. ✅ Update README.md with live URLs
2. ✅ Test all features thoroughly
3. ✅ Set up custom domain (optional)
4. ✅ Configure monitoring alerts
5. ✅ Add usage analytics
6. ✅ Consider upgrading to paid tiers for production

---

## Support

**Issues?**
1. Check Vercel deployment logs
2. Check Render service logs
3. Test backend health endpoint: `/health`
4. Review browser console for frontend errors

**Need Help?**
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs

---

## Quick Reference

### Your Deployed URLs

**Frontend (Vercel):**
```
https://your-app.vercel.app
```

**Backend (Render):**
```
https://vehicle-detection-api-xxx.onrender.com
```

**API Documentation:**
```
https://vehicle-detection-api-xxx.onrender.com/docs
```

### Important Commands

**Redeploy Frontend:**
```bash
cd frontend
vercel --prod
```

**Test Backend Locally:**
```bash
cd backend
uvicorn main:app --reload
```

**Test Frontend Locally:**
```bash
cd frontend
npm start
```

---

**Happy Deploying! 🚀**
