# Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fatik107%2FVehicle-Number-Plate-Detection&project-name=vehicle-detection&repository-name=vehicle-detection&root-directory=frontend&env=REACT_APP_API_URL&envDescription=Backend%20API%20URL%20from%20Render%20deployment&envLink=https%3A%2F%2Fgithub.com%2Fatik107%2FVehicle-Number-Plate-Detection%2Fblob%2Fmain%2FVERCEL_DEPLOYMENT.md)

## Quick Deploy

1. **Deploy Backend First**
   - Go to [Render.com](https://render.com)
   - Create new Web Service
   - Connect this repository
   - Set root directory to `backend`
   - Copy your backend URL

2. **Deploy Frontend to Vercel**
   - Click the "Deploy to Vercel" button above
   - OR follow manual steps below

## Manual Deployment

### Prerequisites
- GitHub account
- Vercel account (sign up at https://vercel.com)
- Backend deployed to Render (see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md))

### Steps

1. **Fork or Clone this repository**

2. **Deploy to Vercel**
   ```bash
   # Install Vercel CLI
   npm install -g vercel

   # Login
   vercel login

   # Navigate to frontend
   cd frontend

   # Deploy
   vercel --prod
   ```

3. **Set Environment Variable**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add: `REACT_APP_API_URL` = `https://your-backend-url.onrender.com`
   - Redeploy

4. **Access Your App**
   - Frontend: `https://your-app.vercel.app`
   - Backend: `https://your-backend.onrender.com`

## Configuration

This project is configured with:
- `vercel.json` - Vercel build and routing configuration
- `.vercelignore` - Files to exclude from deployment
- `frontend/.env.production` - Production environment variables

## Architecture

```
┌─────────────────────┐
│   Vercel (Frontend) │
│   React App         │
└──────────┬──────────┘
           │
           │ HTTPS
           │
           ▼
┌─────────────────────┐
│   Render (Backend)  │
│   FastAPI + ML      │
└─────────────────────┘
```

## Documentation

- **Full Deployment Guide**: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- **General Deployment**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Quick Start**: [DEPLOY_NOW.md](DEPLOY_NOW.md)

## Features

✅ One-click deploy to Vercel  
✅ Automatic deployments on git push  
✅ Environment variable management  
✅ Custom domain support  
✅ SSL certificates included  
✅ CDN and edge caching  

## Support

For detailed instructions and troubleshooting, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
