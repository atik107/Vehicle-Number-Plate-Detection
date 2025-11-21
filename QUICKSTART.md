# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Option 1: Automatic Start (Recommended)

Simply run the main startup script:

```powershell
.\start.ps1
```

This will automatically:
- Start the backend server on port 8000
- Start the frontend server on port 3000
- Open both in separate PowerShell windows

### Option 2: Manual Start

**Terminal 1 - Backend:**
```powershell
cd backend
.\start.ps1
```

**Terminal 2 - Frontend:**
```powershell
cd frontend
.\start.ps1
```

### Option 3: First Time Setup

If the automatic script doesn't work, follow these steps:

**1. Setup Backend:**
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

**2. Setup Frontend (in new terminal):**
```powershell
cd frontend
npm install
npm start
```

## 📋 Requirements

- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ Internet connection (for downloading models on first run)
- ✅ ~500MB free disk space (for models and dependencies)

## 🎯 Using the Application

1. Open your browser to `http://localhost:3000`
2. Drag and drop an image with vehicles
3. Click "Detect Vehicles"
4. View the results with detected vehicles and number plates!

## 🔧 Troubleshooting

**Backend won't start:**
- Make sure Python is installed: `python --version`
- Try: `pip install -r requirements.txt --upgrade`

**Frontend won't start:**
- Make sure Node.js is installed: `node --version`
- Try: `npm cache clean --force` then `npm install`

**Models not downloading:**
- Check your internet connection
- Models will auto-download on first detection (~150MB)

## 📞 Need Help?

Check the full README.md for detailed documentation.

---

**Happy Detecting! 🚗📸**
