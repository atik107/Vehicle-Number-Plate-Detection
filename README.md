# Vehicle & Number Plate Detection System

A production-level AI-powered system for detecting vehicles and extracting number plate information from images using YOLOv8 and EasyOCR.

## Features

- 🚗 **Vehicle Detection**: Detects cars, motorcycles, buses, and trucks using YOLOv8
- 🔍 **Number Plate Detection**: Automatically locates license plates on detected vehicles with multiple detection algorithms
- 🌐 **Multilingual OCR**: Supports both **Bangla (বাংলা)** and **English** number plates
- 📝 **Text Extraction**: Advanced OCR with multiple preprocessing methods for maximum accuracy
- 🎨 **Modern UI**: Responsive React frontend with drag-and-drop image upload
- ⚡ **Fast Processing**: Optimized for production use with pretrained models
- 📊 **Detailed Results**: Visual annotations, language detection, and comprehensive statistics
- 🔄 **Robust Detection**: Multiple preprocessing and detection methods for challenging conditions

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **YOLOv8**: State-of-the-art object detection
- **EasyOCR**: Optical character recognition
- **OpenCV**: Image processing
- **PyTorch**: Deep learning framework

### Frontend
- **React**: Modern UI library
- **TailwindCSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **React Dropzone**: File upload component
- **React Icons**: Beautiful icon library

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- pip (Python package manager)
- npm or yarn (Node package manager)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn
- YOLOv8 (Ultralytics)
- EasyOCR
- OpenCV
- PyTorch and TorchVision
- Other required packages

**Note**: The first time you run the backend, it will automatically download pretrained models:
- YOLOv8 nano model (~6MB)
- EasyOCR English model (~150MB)
- EasyOCR Bangla model (~140MB)
- Total first-time download: ~300MB

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node dependencies:
```bash
npm install
```

This will install:
- React and React DOM
- TailwindCSS
- Axios
- React Dropzone
- React Icons
- Other required packages

## Running the Application

### Start the Backend Server

1. Navigate to the backend directory:
```bash
cd backend
```

2. Activate your virtual environment (if not already activated)

3. Run the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start on `http://localhost:8000`

**API Endpoints:**
- `GET /`: API information
- `GET /health`: Health check
- `POST /detect`: Upload image for detection
- `DELETE /cleanup`: Clean up uploaded files

API documentation available at: `http://localhost:8000/docs`

### Start the Frontend Application

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Start the React development server:
```bash
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

## Usage

1. **Upload an Image**:
   - Drag and drop an image onto the upload area, or
   - Click the upload area to select an image file
   - Supported formats: JPG, PNG, BMP, WEBP

2. **Detect Vehicles**:
   - Click the "Detect Vehicles" button
   - Wait for the AI to process the image (usually 2-5 seconds)

3. **View Results**:
   - See detected vehicles with bounding boxes
   - View extracted number plate text
   - Check detection confidence scores
   - Download the annotated image

4. **Reset**:
   - Click "Reset" to clear and start over with a new image

## Project Structure

```
Number Plate Detection Project/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── uploads/                # Uploaded images
│   ├── results/                # Processed images
│   └── models/                 # Downloaded models
│
├── frontend/
│   ├── public/
│   │   └── index.html         # HTML template
│   ├── src/
│   │   ├── App.js             # Main React component
│   │   ├── App.css            # Component styles
│   │   ├── index.js           # React entry point
│   │   └── index.css          # Global styles
│   ├── package.json           # Node dependencies
│   ├── tailwind.config.js     # TailwindCSS config
│   └── postcss.config.js      # PostCSS config
│
└── README.md                   # This file
```

## How It Works

### Detection Pipeline

1. **Image Upload**: User uploads an image through the frontend
2. **Vehicle Detection**: YOLOv8 detects vehicles (cars, motorcycles, buses, trucks)
3. **Plate Localization**: Multi-method detection algorithm:
   - Contour-based detection with multiple edge thresholds
   - Morphological operations (tophat/blackhat)
   - Aspect ratio filtering (1.5-6.0 to support both Bangla and English plates)
   - Duplicate removal using IoU (Intersection over Union)
4. **Image Preprocessing**: Multiple techniques applied:
   - Otsu thresholding
   - Adaptive thresholding
   - CLAHE contrast enhancement
   - Noise reduction
   - Morphological operations
5. **Text Extraction**: EasyOCR with Bangla and English support
   - Tries multiple preprocessing methods
   - Selects best result based on confidence
   - Automatic language detection
6. **Visualization**: Results annotated with color-coded boxes
   - Green boxes: Vehicles
   - Red/Magenta boxes: Plates (magenta for Bangla)
7. **Response**: JSON data with language info and annotated image sent to frontend

### Model Details

- **YOLOv8 Nano**: Fast and lightweight object detection model
  - Classes: car (2), motorcycle (3), bus (5), truck (7) from COCO dataset
  - Confidence threshold: 30%
  
- **EasyOCR**: Multilingual OCR with Bangla and English language support
  - Automatic GPU acceleration if available
  - Multiple preprocessing: grayscale, thresholding, CLAHE, denoising
  - Language detection and formatting

## Configuration

### Backend Configuration (`.env`)

```env
HOST=0.0.0.0
PORT=8000
UPLOAD_DIR=uploads
RESULTS_DIR=results
MODELS_DIR=models
```

### Detection Parameters

You can modify these in `backend/main.py`:

```python
# Vehicle detection confidence threshold
vehicle_detection_confidence = 0.3  # 30%

# Plate aspect ratio range (width/height)
min_aspect_ratio = 1.5  # Narrower plates (Bangla)
max_aspect_ratio = 6.0  # Wider plates (English)

# Minimum plate size (pixels)
min_plate_width = 30
min_plate_height = 12

# OCR languages
ocr_languages = ['bn', 'en']  # Bangla and English

# Number of preprocessing methods
num_preprocessing_methods = 5  # More methods = better accuracy, slower speed
```

### Frontend Configuration

The frontend uses a proxy to connect to the backend. In `package.json`:
```json
"proxy": "http://localhost:8000"
```

## Performance Optimization

- **Lazy Loading**: Models are loaded only when first needed
- **YOLOv8 Nano**: Smallest YOLO model for faster inference
- **GPU Support**: Automatically uses GPU if available
- **Image Preprocessing**: Optimized for better OCR accuracy
- **Async Processing**: Non-blocking API endpoints

## Troubleshooting

### Backend Issues

**Import errors or missing packages:**
```bash
pip install -r requirements.txt --upgrade
```

**Port already in use:**
```bash
# Change port in main.py or use:
uvicorn main:app --port 8001
```

**Model download fails:**
- Check internet connection
- Models will auto-download on first use
- YOLOv8: ~6MB, EasyOCR: ~150MB

### Frontend Issues

**Dependencies not installing:**
```bash
npm cache clean --force
npm install
```

**Port 3000 already in use:**
- React will prompt to use another port
- Or set PORT environment variable:
```bash
set PORT=3001
npm start
```

**CORS errors:**
- Ensure backend is running on port 8000
- Check proxy setting in package.json

## API Examples

### Detect Vehicles and Plates

```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/image.jpg"
```

Response:
```json
{
  "success": true,
  "timestamp": "20231121_143025",
  "output_url": "/results/result_20231121_143025.jpg",
  "vehicles": [
    {
      "bbox": [100, 200, 500, 600],
      "confidence": 0.95,
      "class": "car"
    }
  ],
  "plates": [
    {
      "bbox": [200, 500, 400, 550],
      "text": "ABC123",
      "confidence": 0.87,
      "vehicle_index": 0
    }
  ],
  "summary": {
    "total_vehicles": 1,
    "total_plates": 1,
    "plates_with_text": 1
  }
}
```

## Future Enhancements

- [ ] Support for multiple number plate formats (US, EU, Asia, etc.)
- [ ] Real-time video processing
- [ ] Database integration for storing results
- [ ] User authentication and history
- [ ] Batch processing for multiple images
- [ ] Custom model training interface
- [ ] Export results to CSV/PDF
- [ ] Mobile app version

## License

This project is for educational and demonstration purposes.

## Credits

- **YOLOv8**: Ultralytics
- **EasyOCR**: JaidedAI
- **FastAPI**: Sebastián Ramírez
- **React**: Meta/Facebook

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Verify all dependencies are installed correctly

---

**Built with ❤️ using AI and Modern Web Technologies**
