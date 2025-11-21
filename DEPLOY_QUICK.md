# 🚀 Deployment Quick Reference

## One-Click Deploy

[![Deploy to Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fatik107%2FVehicle-Number-Plate-Detection&project-name=vehicle-detection&repository-name=vehicle-detection&root-directory=frontend&env=REACT_APP_API_URL)

---

## ⚡ Quick Steps

### 1️⃣ Deploy Backend (5 min)
```
Platform: Render.com (Free)
URL: https://render.com
Root: backend
Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### 2️⃣ Deploy Frontend (3 min)
```
Platform: Vercel (Free)
URL: https://vercel.com
Root: frontend
Env: REACT_APP_API_URL = <your-backend-url>
```

---

## 📋 Configuration Files

✅ `vercel.json` - Vercel build configuration  
✅ `.vercelignore` - Files to exclude  
✅ `frontend/vercel.json` - React app routing  
✅ `frontend/.env.production` - Environment variables  
✅ `backend/Dockerfile` - Backend container  
✅ `render.yaml` - Render configuration  

---

## 🔗 Important URLs

**After Deployment:**
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-api.onrender.com`
- API Docs: `https://your-api.onrender.com/docs`

---

## 📚 Documentation

- [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md) - Complete guide
- [DEPLOY_TO_VERCEL.md](DEPLOY_TO_VERCEL.md) - Quick reference
- [DEPLOYMENT.md](DEPLOYMENT.md) - All platforms
- [DEPLOYMENT_NOTES.md](DEPLOYMENT_NOTES.md) - Technical notes

---

## ✅ Pre-Deployment Checklist

- [ ] Backend deployed to Render
- [ ] Backend URL copied
- [ ] Frontend deployed to Vercel
- [ ] Environment variable `REACT_APP_API_URL` set in Vercel
- [ ] Test image upload
- [ ] Test vehicle detection
- [ ] Check browser console for errors

---

## 🆘 Quick Troubleshooting

**Frontend not loading?**
→ Check Vercel deployment logs

**API calls failing?**
→ Verify REACT_APP_API_URL is set correctly

**Backend timeout?**
→ First request takes 30-60s on free tier (cold start)

**CORS errors?**
→ Backend allows all origins by default

---

## 💡 Tips

- Free tier: Backend sleeps after 15 min
- First API call: May take 30-60 seconds
- Models: Download on first request (~300MB)
- Build time: Frontend ~3 min, Backend ~5-10 min

---

**Total Time:** 10-15 minutes  
**Total Cost:** $0 (Free tier)

---

Made with ❤️ | [Report Issue](https://github.com/atik107/Vehicle-Number-Plate-Detection/issues)
