# 🚀 Quick Deployment Steps

## Deploy in 5 Minutes

### Step 1: Deploy Backend to Render (Free)

1. **Go to Render.com:**
   - Visit: https://render.com
   - Sign up with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect GitHub account
   - Select: `Vehicle-Number-Plate-Detection` repository

3. **Configure Service:**
   ```
   Name: vehicle-detection-api
   Region: Choose closest to you
   Branch: main
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Click "Create Web Service"**
   - Wait 5-10 minutes for deployment
   - Note your backend URL: `https://vehicle-detection-api-xxx.onrender.com`

---

### Step 2: Deploy Frontend to Vercel (Free)

1. **Go to Vercel:**
   - Visit: https://vercel.com
   - Sign up with GitHub

2. **Import Project:**
   - Click "Add New..." → "Project"
   - Import `Vehicle-Number-Plate-Detection`
   - Framework Preset: Create React App
   - Root Directory: `frontend`

3. **Add Environment Variable:**
   ```
   REACT_APP_API_URL = https://vehicle-detection-api-xxx.onrender.com
   ```
   (Use your backend URL from Step 1)

4. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your site: `https://vehicle-number-plate-detection.vercel.app`

---

### Alternative: Deploy Frontend to GitHub Pages

1. **Update backend URL in `.env.production`:**
   ```bash
   # Edit frontend/.env.production
   REACT_APP_API_URL=https://your-backend-url.onrender.com
   ```

2. **Run deployment script:**
   ```powershell
   .\deploy-frontend.ps1
   ```

3. **Enable GitHub Pages:**
   - Go to: https://github.com/atik107/Vehicle-Number-Plate-Detection/settings/pages
   - Source: `gh-pages` branch
   - Click "Save"

4. **Access your site:**
   - URL: https://atik107.github.io/Vehicle-Number-Plate-Detection

---

## 🔧 Configuration Checklist

After deployment:

- [ ] Backend deployed and running
- [ ] Backend URL copied
- [ ] Frontend environment variable updated
- [ ] Frontend deployed
- [ ] Test file upload works
- [ ] Test detection works
- [ ] Update README with live URLs

---

## 📝 Update Backend URL

### If using Vercel:
1. Go to Vercel dashboard
2. Select your project
3. Settings → Environment Variables
4. Add: `REACT_APP_API_URL` = `https://your-backend.onrender.com`
5. Redeploy

### If using GitHub Pages:
1. Edit `frontend/.env.production`
2. Update URL
3. Run `.\deploy-frontend.ps1` again

---

## 🎯 Your Live URLs

After deployment:

**Frontend (Choose one):**
- Vercel: `https://vehicle-number-plate-detection.vercel.app`
- GitHub Pages: `https://atik107.github.io/Vehicle-Number-Plate-Detection`

**Backend:**
- Render: `https://vehicle-detection-api-xxx.onrender.com`

**API Docs:**
- `https://your-backend-url.onrender.com/docs`

---

## ⚠️ Important Notes

**Free Tier Limitations:**

- **Render:** Backend sleeps after 15 min of inactivity
  - First request takes 30-60 seconds to wake up
  - Keep alive with cron job or upgrade

- **Model Downloads:** 
  - Models download on first request (~150MB)
  - May timeout on free tier
  - Consider pre-downloading models

**Solutions:**
1. Upgrade to paid tier ($7/month for Render)
2. Use cron job to keep backend alive
3. Pre-download models in Docker image

---

## 🚀 Advanced: Docker Deployment

If you want to deploy with Docker:

```bash
# Build
docker build -t vehicle-detection-backend ./backend

# Run locally
docker run -p 8000:8000 vehicle-detection-backend

# Deploy to Render/Railway with Dockerfile
```

---

## Need Help?

1. Check `DEPLOYMENT.md` for detailed guide
2. Review Render logs if backend fails
3. Check browser console for frontend errors
4. Test API directly: `https://your-backend/health`

---

**Estimated Time:** 10-15 minutes total
**Cost:** $0 (Free tier)
**Ready to deploy? Let's go! 🚀**
