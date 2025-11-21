#!/bin/bash

# Pre-Deployment Verification Script
# This script helps verify the setup before deploying to Vercel

set -e

echo "🚀 Vehicle Number Plate Detection - Pre-Deployment Verification"
echo "================================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "vercel.json" ]; then
    echo -e "${RED}❌ Error: vercel.json not found. Please run this script from the project root.${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Checking Prerequisites...${NC}"
echo ""

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js installed:${NC} $NODE_VERSION"
else
    echo -e "${RED}❌ Node.js not found. Please install Node.js 16 or higher.${NC}"
    exit 1
fi

# Check npm
if command -v npm &> /dev/null; then
    NPM_VERSION=$(npm --version)
    echo -e "${GREEN}✅ npm installed:${NC} $NPM_VERSION"
else
    echo -e "${RED}❌ npm not found.${NC}"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python installed:${NC} $PYTHON_VERSION"
else
    echo -e "${YELLOW}⚠️  Python not found (required for backend).${NC}"
fi

echo ""
echo -e "${YELLOW}📦 Checking Frontend Dependencies...${NC}"
echo ""

cd frontend

if [ -f "package.json" ]; then
    echo -e "${GREEN}✅ package.json found${NC}"
else
    echo -e "${RED}❌ package.json not found in frontend directory${NC}"
    exit 1
fi

# Install frontend dependencies
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📥 Installing frontend dependencies...${NC}"
    npm install
    echo -e "${GREEN}✅ Frontend dependencies installed${NC}"
else
    echo -e "${GREEN}✅ Frontend dependencies already installed${NC}"
fi

echo ""
echo -e "${YELLOW}🔧 Checking Configuration Files...${NC}"
echo ""

# Check vercel.json
if [ -f "../vercel.json" ]; then
    echo -e "${GREEN}✅ Root vercel.json exists${NC}"
else
    echo -e "${RED}❌ Root vercel.json not found${NC}"
fi

if [ -f "vercel.json" ]; then
    echo -e "${GREEN}✅ Frontend vercel.json exists${NC}"
else
    echo -e "${RED}❌ Frontend vercel.json not found${NC}"
fi

# Check .env.production
if [ -f ".env.production" ]; then
    echo -e "${GREEN}✅ .env.production exists${NC}"
    if grep -q "your-backend-url" .env.production; then
        echo -e "${YELLOW}⚠️  Warning: .env.production still has placeholder URL${NC}"
        echo -e "${YELLOW}   Update REACT_APP_API_URL after deploying backend${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  .env.production not found (will use default)${NC}"
fi

echo ""
echo -e "${YELLOW}🏗️  Testing Frontend Build...${NC}"
echo ""

# Test build
if npm run build; then
    echo -e "${GREEN}✅ Frontend build successful!${NC}"
    echo -e "${GREEN}   Build output: frontend/build${NC}"
else
    echo -e "${RED}❌ Frontend build failed. Please fix errors before deploying.${NC}"
    exit 1
fi

cd ..

echo ""
echo -e "${YELLOW}📊 Project Structure Check...${NC}"
echo ""

REQUIRED_FILES=(
    "README.md"
    "vercel.json"
    ".vercelignore"
    "VERCEL_DEPLOYMENT.md"
    "DEPLOY_TO_VERCEL.md"
    "frontend/package.json"
    "frontend/vercel.json"
    "backend/main.py"
    "backend/requirements.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅${NC} $file"
    else
        echo -e "${RED}❌${NC} $file (missing)"
    fi
done

echo ""
echo -e "${GREEN}================================================================${NC}"
echo -e "${GREEN}✅ Pre-Deployment Verification Complete!${NC}"
echo -e "${GREEN}================================================================${NC}"
echo ""
echo -e "${YELLOW}📝 Next Steps:${NC}"
echo ""
echo "1. Deploy Backend to Render:"
echo "   - Visit: https://render.com"
echo "   - Create Web Service from this repository"
echo "   - Set root directory to 'backend'"
echo "   - Copy backend URL"
echo ""
echo "2. Deploy Frontend to Vercel:"
echo "   - Visit: https://vercel.com"
echo "   - Import this repository"
echo "   - Set root directory to 'frontend'"
echo "   - Add environment variable: REACT_APP_API_URL = <backend-url>"
echo "   - Deploy"
echo ""
echo "3. Read the guides:"
echo "   - VERCEL_DEPLOYMENT.md - Complete deployment guide"
echo "   - DEPLOY_TO_VERCEL.md - Quick reference"
echo ""
echo -e "${GREEN}🚀 Ready to deploy!${NC}"
echo ""
