# Testing Guide

## Test the Application

Your vehicle detection system is ready! Here are some ways to test it:

## Quick Test

1. **Open the application**: http://localhost:3000
2. **Find a test image**: Any image with vehicles (cars, trucks, motorcycles, buses)
3. **Upload and test!**

## Where to Get Test Images

### Option 1: Use Your Own Photos
- Take a photo of your car
- Screenshot from Google Street View
- Download parking lot images

### Option 2: Free Image Sources
- **Unsplash**: https://unsplash.com/s/photos/car
- **Pexels**: https://www.pexels.com/search/cars/
- **Pixabay**: https://pixabay.com/images/search/vehicle/

### Option 3: Sample Scenarios

**Easy Test** (Best for first try):
- Single car in clear view
- Good lighting
- Front or rear view (where plates are visible)

**Medium Test**:
- Multiple vehicles
- Parking lot scene
- Side angle views

**Hard Test**:
- Vehicles at distance
- Poor lighting conditions
- Motion blur

## Expected Results

### Good Detection
✅ Vehicle boundaries clearly marked (green boxes)
✅ Number plate region identified (red boxes)
✅ Text extracted (displayed on image and in results panel)
✅ High confidence scores (>70%)

### Challenging Cases
⚠️ Distant vehicles may not be detected
⚠️ Plates at extreme angles may not be recognized
⚠️ Very dirty or damaged plates may fail OCR
⚠️ Non-standard plate formats may not parse correctly

## API Testing

Test the backend API directly:

### Health Check
```powershell
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-11-21T..."
}
```

### API Documentation
Open http://localhost:8000/docs in your browser to see:
- Interactive API documentation
- Try out endpoints
- See request/response schemas

### Test Detection via API

```powershell
curl -X POST "http://localhost:8000/detect" `
  -F "file=@path/to/your/image.jpg"
```

## Performance Testing

### Typical Response Times
- Small image (< 1MB): 2-3 seconds
- Medium image (1-3MB): 3-5 seconds
- Large image (> 3MB): 5-10 seconds

### First Detection
⚠️ **Note**: The very first detection will be slower (10-15 seconds) because:
- Models need to be loaded into memory
- YOLOv8 initializes
- EasyOCR loads language data

Subsequent detections will be much faster!

## Sample Test Results

What to expect:

### Example 1: Single Car
```
Input: 1 car, clearly visible plate
Output:
- 1 vehicle detected (confidence: 95%)
- 1 plate detected
- Text: "ABC123" (confidence: 82%)
```

### Example 2: Parking Lot
```
Input: 5 cars, various angles
Output:
- 5 vehicles detected (confidence: 75-98%)
- 3-4 plates detected
- 2-3 texts recognized
```

## Troubleshooting Test Issues

### "No vehicles detected"
- Ensure image has clear vehicle(s)
- Try a different image
- Check image quality and size

### "Plate detected but no text"
- Plate may be too small in image
- Text may be obscured or blurry
- Try uploading a higher resolution image

### "Slow detection"
- First detection is always slower (model loading)
- Large images take longer to process
- Check if GPU is being utilized

## Best Practices for Good Results

1. **Image Quality**: Use high-resolution images (1920x1080 or better)
2. **Lighting**: Well-lit scenes work best
3. **Angle**: Front/rear views better than side views
4. **Distance**: Closer vehicles detect better
5. **Clarity**: Sharp, focused images preferred

## Advanced Testing

### Test Cleanup Endpoint
```powershell
curl -X DELETE http://localhost:8000/cleanup
```

This removes all uploaded and result files.

### Monitor Logs

**Backend logs**:
- Check the terminal where backend is running
- Look for detection times and confidence scores

**Frontend logs**:
- Open browser DevTools (F12)
- Check Console tab for any errors
- Network tab shows API requests

## Success Criteria

✅ Frontend loads without errors
✅ Image uploads successfully
✅ Detection completes in < 10 seconds
✅ Results display correctly
✅ Can download processed image
✅ Reset button works
✅ Multiple detections work in sequence

---

**Enjoy testing your vehicle detection system!** 🚗🔍
