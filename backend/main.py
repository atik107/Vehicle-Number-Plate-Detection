from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import cv2
import numpy as np
from ultralytics import YOLO
import easyocr
import os
from pathlib import Path
from datetime import datetime
import shutil
from typing import List, Dict
import base64

app = FastAPI(title="Vehicle & Number Plate Detection API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories
UPLOAD_DIR = Path("uploads")
RESULTS_DIR = Path("results")
MODELS_DIR = Path("models")

for directory in [UPLOAD_DIR, RESULTS_DIR, MODELS_DIR]:
    directory.mkdir(exist_ok=True)

# Mount static files
app.mount("/results", StaticFiles(directory="results"), name="results")

# Initialize models (will be loaded on first use)
vehicle_model = None
plate_model = None
ocr_reader = None

def load_models():
    """Lazy load models to improve startup time"""
    global vehicle_model, plate_model, ocr_reader
    
    if vehicle_model is None:
        print("Loading vehicle detection model...")
        vehicle_model = YOLO('yolov8n.pt')  # YOLOv8 nano for faster inference
    
    if plate_model is None:
        print("Loading number plate detection model...")
        # Using same model but will fine-tune detection for license plates
        plate_model = YOLO('yolov8n.pt')
    
    if ocr_reader is None:
        print("Loading OCR reader with Bangla and English support...")
        # Support both Bengali and English for number plates
        ocr_reader = easyocr.Reader(['bn', 'en'], gpu=True if cv2.cuda.getCudaEnabledDeviceCount() > 0 else False)
    
    return vehicle_model, plate_model, ocr_reader

def detect_vehicles(image: np.ndarray, model):
    """Detect vehicles in the image"""
    # Vehicle classes in COCO dataset: car, motorcycle, bus, truck
    vehicle_classes = [2, 3, 5, 7]  # car, motorcycle, bus, truck
    
    results = model(image, conf=0.3)
    detections = []
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            cls = int(box.cls[0])
            if cls in vehicle_classes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                class_name = result.names[cls]
                
                detections.append({
                    'bbox': [x1, y1, x2, y2],
                    'confidence': confidence,
                    'class': class_name
                })
    
    return detections

def detect_license_plates(image: np.ndarray, vehicle_boxes: List[Dict]):
    """Detect license plates within vehicle regions using multiple methods"""
    plates = []
    
    for idx, vehicle in enumerate(vehicle_boxes):
        x1, y1, x2, y2 = vehicle['bbox']
        
        # Add padding to vehicle ROI
        h, w = image.shape[:2]
        pad = 30
        x1_pad = max(0, x1 - pad)
        y1_pad = max(0, y1 - pad)
        x2_pad = min(w, x2 + pad)
        y2_pad = min(h, y2 + pad)
        
        vehicle_roi = image[y1_pad:y2_pad, x1_pad:x2_pad]
        
        # Try multiple detection methods
        detected_plates = []
        
        # Method 1: Contour-based detection
        gray = cv2.cvtColor(vehicle_roi, cv2.COLOR_BGR2GRAY)
        
        # Apply multiple preprocessing techniques
        blur = cv2.bilateralFilter(gray, 11, 17, 17)
        
        # Try multiple edge detection thresholds
        for low_thresh, high_thresh in [(30, 200), (50, 150), (70, 210)]:
            edged = cv2.Canny(blur, low_thresh, high_thresh)
            
            # Find contours
            contours, _ = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
            
            for contour in contours:
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
                
                # License plates typically have 4 corners
                if len(approx) == 4:
                    x, y, w_plate, h_plate = cv2.boundingRect(approx)
                    
                    # Relaxed aspect ratio for both Bangla and English plates
                    # Bangla plates: typically 1.8-3.5, English plates: 2.0-5.5
                    aspect_ratio = w_plate / float(h_plate)
                    if 1.5 <= aspect_ratio <= 6.0 and w_plate > 30 and h_plate > 12:
                        plate_x1 = x1_pad + x
                        plate_y1 = y1_pad + y
                        plate_x2 = plate_x1 + w_plate
                        plate_y2 = plate_y1 + h_plate
                        
                        detected_plates.append({
                            'bbox': [plate_x1, plate_y1, plate_x2, plate_y2],
                            'vehicle_index': idx,
                            'confidence': 0.85,
                            'area': w_plate * h_plate
                        })
        
        # Method 2: Morphological operations for better plate detection
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
        
        # Combine tophat and blackhat
        morph_combined = cv2.add(tophat, blackhat)
        _, thresh = cv2.threshold(morph_combined, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        for contour in contours:
            x, y, w_plate, h_plate = cv2.boundingRect(contour)
            aspect_ratio = w_plate / float(h_plate)
            
            if 1.5 <= aspect_ratio <= 6.0 and w_plate > 30 and h_plate > 12:
                plate_x1 = x1_pad + x
                plate_y1 = y1_pad + y
                plate_x2 = plate_x1 + w_plate
                plate_y2 = plate_y1 + h_plate
                
                detected_plates.append({
                    'bbox': [plate_x1, plate_y1, plate_x2, plate_y2],
                    'vehicle_index': idx,
                    'confidence': 0.80,
                    'area': w_plate * h_plate
                })
        
        # Select the best plate (largest area with good aspect ratio)
        if detected_plates:
            # Remove duplicates (plates too close to each other)
            unique_plates = []
            for plate in sorted(detected_plates, key=lambda x: x['area'], reverse=True):
                is_duplicate = False
                for unique_plate in unique_plates:
                    # Check IoU (Intersection over Union)
                    x1a, y1a, x2a, y2a = plate['bbox']
                    x1b, y1b, x2b, y2b = unique_plate['bbox']
                    
                    xi1, yi1 = max(x1a, x1b), max(y1a, y1b)
                    xi2, yi2 = min(x2a, x2b), min(y2a, y2b)
                    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)
                    
                    box1_area = (x2a - x1a) * (y2a - y1a)
                    box2_area = (x2b - x1b) * (y2b - y1b)
                    union_area = box1_area + box2_area - inter_area
                    
                    iou = inter_area / union_area if union_area > 0 else 0
                    
                    if iou > 0.5:  # Overlapping plates
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    unique_plates.append(plate)
                    if len(unique_plates) >= 2:  # Max 2 plates per vehicle
                        break
            
            for plate in unique_plates:
                del plate['area']  # Remove temporary field
                plates.append(plate)
        else:
            # Fallback: use bottom region of vehicle if no plate detected
            vehicle_height = y2 - y1
            vehicle_width = x2 - x1
            
            # Assume plate is in bottom 1/3 of vehicle
            plate_y1 = y1 + int(vehicle_height * 0.6)
            plate_y2 = y2
            plate_x1 = x1 + int(vehicle_width * 0.2)
            plate_x2 = x2 - int(vehicle_width * 0.2)
            
            plates.append({
                'bbox': [plate_x1, plate_y1, plate_x2, plate_y2],
                'vehicle_index': idx,
                'confidence': 0.5
            })
    
    return plates

def extract_plate_text(image: np.ndarray, plate_boxes: List[Dict], reader) -> List[Dict]:
    """Extract text from license plates using OCR with advanced preprocessing"""
    results = []
    
    for plate in plate_boxes:
        x1, y1, x2, y2 = plate['bbox']
        
        # Ensure coordinates are within image bounds
        h, w = image.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        plate_roi = image[y1:y2, x1:x2]
        
        if plate_roi.size == 0:
            continue
        
        # Try multiple preprocessing techniques for better OCR
        best_text = ""
        best_confidence = 0.0
        best_language = "unknown"
        
        preprocessing_methods = []
        
        # Method 1: Grayscale + Otsu threshold
        gray_plate = cv2.cvtColor(plate_roi, cv2.COLOR_BGR2GRAY)
        _, thresh1 = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        preprocessing_methods.append(thresh1)
        
        # Method 2: Adaptive threshold
        thresh2 = cv2.adaptiveThreshold(gray_plate, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY, 11, 2)
        preprocessing_methods.append(thresh2)
        
        # Method 3: Inverted Otsu (for dark plates)
        _, thresh3 = cv2.threshold(gray_plate, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        preprocessing_methods.append(thresh3)
        
        # Method 4: Contrast enhancement + threshold
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray_plate)
        _, thresh4 = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        preprocessing_methods.append(thresh4)
        
        # Method 5: Denoising + threshold
        denoised = cv2.fastNlMeansDenoising(gray_plate, None, 10, 7, 21)
        _, thresh5 = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        preprocessing_methods.append(thresh5)
        
        # Try OCR on each preprocessed version
        for processed_img in preprocessing_methods:
            # Resize for better OCR (larger is better for text recognition)
            scale_factor = 3
            height, width = processed_img.shape
            if height < 50:  # If too small, scale up more
                scale_factor = 4
            
            resized = cv2.resize(processed_img, None, fx=scale_factor, fy=scale_factor, 
                               interpolation=cv2.INTER_CUBIC)
            
            # Apply morphological operations to improve character separation
            kernel = np.ones((2, 2), np.uint8)
            resized = cv2.morphologyEx(resized, cv2.MORPH_CLOSE, kernel)
            
            # OCR with detail level 0 for better performance
            try:
                ocr_results = reader.readtext(resized, detail=1, paragraph=False,
                                             allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzঀঁংঃঅআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ়ািীুূৃেৈোৌ্ৎৗড়ঢ়য়০১২৩৪৫৬৭৮৯')
                
                if ocr_results:
                    # Combine all detected text segments
                    full_text = ""
                    total_confidence = 0.0
                    
                    for detection in ocr_results:
                        bbox, text, conf = detection
                        full_text += text
                        total_confidence += conf
                    
                    avg_confidence = total_confidence / len(ocr_results) if ocr_results else 0.0
                    
                    # Keep the best result
                    if avg_confidence > best_confidence:
                        best_confidence = avg_confidence
                        best_text = full_text.strip()
                        
                        # Detect language (simple heuristic)
                        if any('\u0980' <= char <= '\u09FF' for char in best_text):
                            best_language = "bangla"
                        else:
                            best_language = "english"
            except Exception as e:
                print(f"OCR error: {e}")
                continue
        
        # Format the text based on detected language
        formatted_text = best_text
        if best_language == "english":
            # Clean English text (remove extra spaces, keep alphanumeric)
            formatted_text = ''.join(best_text.split())
        # For Bangla, keep original formatting
        
        results.append({
            'bbox': plate['bbox'],
            'text': formatted_text,
            'raw_text': best_text,
            'confidence': best_confidence,
            'language': best_language,
            'vehicle_index': plate['vehicle_index']
        })
    
    return results

def draw_detections(image: np.ndarray, vehicles: List[Dict], plates: List[Dict]) -> np.ndarray:
    """Draw bounding boxes on image"""
    output = image.copy()
    
    # Draw vehicle boxes
    for idx, vehicle in enumerate(vehicles):
        x1, y1, x2, y2 = vehicle['bbox']
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Label
        label = f"{vehicle['class']} {vehicle['confidence']:.2f}"
        cv2.putText(output, label, (x1, y1 - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Add vehicle number
        cv2.putText(output, f"Vehicle #{idx + 1}", (x1, y1 - 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
        # Draw plate boxes
    for plate in plates:
        x1, y1, x2, y2 = plate['bbox']
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 0, 255), 2)
        
        # Plate text with language indicator
        if 'text' in plate and plate['text']:
            # Choose color based on language
            text_color = (255, 0, 255) if plate.get('language') == 'bangla' else (0, 0, 255)
            
            # Draw text background for better visibility
            text = plate['text']
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2
            
            (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
            cv2.rectangle(output, (x1, y1 - text_height - 15), 
                        (x1 + text_width + 10, y1 - 5), (255, 255, 255), -1)
            cv2.rectangle(output, (x1, y1 - text_height - 15), 
                        (x1 + text_width + 10, y1 - 5), text_color, 2)
            
            cv2.putText(output, text, (x1 + 5, y1 - 10),
                       font, font_scale, text_color, thickness)
    
    return output

@app.get("/")
async def root():
    return {
        "message": "Vehicle & Number Plate Detection API",
        "version": "1.0.0",
        "endpoints": {
            "/detect": "POST - Upload image for detection",
            "/health": "GET - Check API health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    """
    Detect vehicles and number plates in uploaded image
    """
    try:
        # Load models
        v_model, p_model, reader = load_models()
        
        # Save uploaded file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        input_filename = f"{timestamp}_{file.filename}"
        input_path = UPLOAD_DIR / input_filename
        
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read image
        image = cv2.imread(str(input_path))
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Detect vehicles
        vehicles = detect_vehicles(image, v_model)
        
        if not vehicles:
            return JSONResponse({
                "success": False,
                "message": "No vehicles detected in the image",
                "vehicles": [],
                "plates": []
            })
        
        # Detect license plates
        plates = detect_license_plates(image, vehicles)
        
        # Extract text from plates
        plates_with_text = extract_plate_text(image, plates, reader)
        
        # Draw detections
        output_image = draw_detections(image, vehicles, plates_with_text)
        
        # Save result image
        output_filename = f"result_{timestamp}.jpg"
        output_path = RESULTS_DIR / output_filename
        cv2.imwrite(str(output_path), output_image)
        
        # Prepare response
        response_data = {
            "success": True,
            "timestamp": timestamp,
            "input_image": input_filename,
            "output_image": output_filename,
            "output_url": f"/results/{output_filename}",
            "vehicles": vehicles,
            "plates": plates_with_text,
            "summary": {
                "total_vehicles": len(vehicles),
                "total_plates": len(plates_with_text),
                "plates_with_text": len([p for p in plates_with_text if p['text']])
            }
        }
        
        return JSONResponse(response_data)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cleanup")
async def cleanup_files():
    """Clean up uploaded and result files"""
    try:
        for directory in [UPLOAD_DIR, RESULTS_DIR]:
            for file in directory.glob("*"):
                if file.is_file():
                    file.unlink()
        
        return {"success": True, "message": "All files cleaned up"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
