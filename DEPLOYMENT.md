# Deployment Guide - Vehicle & Number Plate Detection System

## 🚀 Deployment Options

Your project has 2 components that need hosting:
1. **Frontend (React)** - Static files
2. **Backend (FastAPI)** - Python API server

## Option 1: Recommended Setup (Free Tier)

### Frontend: Vercel/Netlify
### Backend: Render/Railway

---

## 📦 Deploy Frontend to Vercel (Free)

### Step 1: Prepare Frontend for Production

1. Create a `vercel.json` in the frontend folder:
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/" }
  ]
}
```

2. Update environment variable for API URL

### Step 2: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Navigate to frontend
cd frontend

# Deploy
vercel

# Follow prompts:
# - Login with GitHub
# - Link to your project
# - Deploy
```

**Or use Vercel Dashboard:**
1. Go to https://vercel.com
2. Import your GitHub repository
3. Set root directory to `frontend`
4. Deploy

---

## 🐳 Deploy Backend to Render (Free Tier)

### Step 1: Create Dockerfile for Backend

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 2: Create render.yaml

Create `render.yaml` in root:
```yaml
services:
  - type: web
    name: vehicle-detection-backend
    env: python
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

### Step 3: Deploy to Render

1. Go to https://render.com
2. Sign up with GitHub
3. New Web Service
4. Connect your repository
5. Select branch: `main`
6. Build Command: `cd backend && pip install -r requirements.txt`
7. Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
8. Deploy

---

## 🌐 Alternative: Deploy Both to Railway

Railway provides both frontend and backend hosting.

### Step 1: Create railway.json

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### Step 2: Deploy

1. Go to https://railway.app
2. Login with GitHub
3. New Project → Deploy from GitHub repo
4. Select your repository
5. Deploy

---

## 📱 Option 2: GitHub Pages + Free Backend

### Frontend on GitHub Pages

1. **Add homepage to package.json:**
```json
"homepage": "https://atik107.github.io/Vehicle-Number-Plate-Detection"
```

2. **Install gh-pages:**
```bash
cd frontend
npm install --save-dev gh-pages
```

3. **Add deploy scripts to package.json:**
```json
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build",
  ...
}
```

4. **Deploy:**
```bash
npm run deploy
```

5. **Enable GitHub Pages:**
   - Go to repo Settings → Pages
   - Source: gh-pages branch
   - Save

### Backend Options (Free Tier):

**A. Render.com** (Recommended)
- 750 hours/month free
- Auto-deploy from GitHub
- Easy setup

**B. Railway.app**
- $5 free credit monthly
- Auto-deploy
- Simple dashboard

**C. Fly.io**
- Free tier available
- Global deployment
- Command-line focused

**D. PythonAnywhere**
- Free tier with limitations
- Python-specific hosting

---

## 🔧 Configuration Updates Needed

### Frontend Environment Variables

Create `frontend/.env.production`:
```env
REACT_APP_API_URL=https://your-backend-url.onrender.com
```

Update `frontend/src/App.js`:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Update axios calls:
await axios.post(`${API_URL}/detect`, formData, {
```

### Backend CORS Update

Update `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://atik107.github.io",
        "https://your-frontend-url.vercel.app",
        # Add your deployed URLs
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🎯 Quick Deploy Commands

### Deploy Frontend to Vercel
```bash
cd frontend
npm install -g vercel
vercel --prod
```

### Deploy Frontend to GitHub Pages
```bash
cd frontend
npm install --save-dev gh-pages
npm run deploy
```

### Deploy Backend to Render
```bash
# Push to GitHub, then:
# 1. Connect Render to your GitHub repo
# 2. Select backend directory
# 3. Deploy automatically
```

---

## 📊 Deployment Comparison

| Service | Type | Free Tier | Best For | Setup Difficulty |
|---------|------|-----------|----------|-----------------|
| Vercel | Frontend | ✅ Unlimited | React apps | ⭐ Easy |
| Netlify | Frontend | ✅ 100GB/mo | Static sites | ⭐ Easy |
| GitHub Pages | Frontend | ✅ Unlimited | Open source | ⭐ Easy |
| Render | Backend | ✅ 750hrs/mo | Python APIs | ⭐⭐ Medium |
| Railway | Both | ✅ $5/mo credit | Full-stack | ⭐⭐ Medium |
| Fly.io | Backend | ✅ Limited | Global apps | ⭐⭐⭐ Hard |

---

## ⚠️ Important Notes

### Model Files
- YOLOv8 model (~6MB) will download on first request
- EasyOCR models (~150MB) may cause timeout on free tier
- Consider uploading pre-downloaded models to deployment

### Memory Limits
- Free tiers have memory limits (512MB - 1GB)
- PyTorch + models may exceed limits
- Consider paid tier or optimized deployment

### Cold Starts
- Free tier backends sleep after inactivity
- First request after sleep may take 30-60 seconds
- Keep alive with cron jobs or upgrade to paid

---

## 🚀 Recommended Deployment Path

**For Quick Demo:**
1. Frontend → Vercel (1 command)
2. Backend → Render (connect GitHub)
3. Total time: ~10 minutes

**For Production:**
1. Frontend → Vercel Pro ($20/mo)
2. Backend → Railway Pro ($5/mo)
3. CDN for model files
4. Database for results storage

---

## 📝 Next Steps After Deployment

1. Update README with live URLs
2. Add deployment badges
3. Set up CI/CD with GitHub Actions
4. Monitor with error tracking (Sentry)
5. Add analytics (Google Analytics)

---

**Need help with specific deployment? Let me know which platform you prefer!**
