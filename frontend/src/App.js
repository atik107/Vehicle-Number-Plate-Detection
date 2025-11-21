import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { FiUpload, FiImage, FiDownload, FiTrash2, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';
import { AiOutlineCar } from 'react-icons/ai';
import './App.css';

// API URL from environment variable or fallback to localhost
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      setSelectedFile(file);
      setPreview(URL.createObjectURL(file));
      setResults(null);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.bmp', '.webp']
    },
    multiple: false
  });

  const handleDetection = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(`${API_URL}/detect`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        setResults(response.data);
      } else {
        setError(response.data.message || 'Detection failed');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred during detection');
      console.error('Detection error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResults(null);
    setError(null);
  };

  const downloadResult = () => {
    if (results && results.output_url) {
      const link = document.createElement('a');
      link.href = `${API_URL}${results.output_url}`;
      link.download = results.output_image;
      link.click();
    }
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12 fade-in">
          <div className="flex items-center justify-center mb-4">
            <AiOutlineCar className="text-6xl text-white mr-4" />
            <h1 className="text-5xl font-bold text-white">
              Vehicle & Plate Detection
            </h1>
          </div>
          <p className="text-xl text-white opacity-90">
            AI-Powered Vehicle and Number Plate Recognition System
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel - Upload */}
          <div className="glass-effect rounded-2xl p-8 shadow-2xl fade-in">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <FiUpload className="mr-3" /> Upload Image
            </h2>

            {/* Dropzone */}
            <div
              {...getRootProps()}
              className={`border-3 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all hover-scale
                ${isDragActive ? 'border-blue-400 bg-blue-50 bg-opacity-20' : 'border-white border-opacity-40'}
                ${preview ? 'bg-opacity-10' : ''}`}
            >
              <input {...getInputProps()} />
              {!preview ? (
                <div>
                  <FiImage className="text-6xl text-white mx-auto mb-4 opacity-70" />
                  <p className="text-white text-lg mb-2">
                    {isDragActive ? 'Drop the image here' : 'Drag & drop an image here'}
                  </p>
                  <p className="text-white opacity-70">or click to select a file</p>
                  <p className="text-white opacity-50 text-sm mt-4">
                    Supports: JPG, PNG, BMP, WEBP
                  </p>
                </div>
              ) : (
                <div>
                  <img
                    src={preview}
                    alt="Preview"
                    className="max-h-96 mx-auto rounded-lg shadow-lg"
                  />
                  <p className="text-white mt-4 text-sm opacity-70">
                    Click or drag to change image
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 mt-6">
              <button
                onClick={handleDetection}
                disabled={!selectedFile || loading}
                className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-4 px-6 rounded-xl font-semibold 
                  hover:from-blue-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed
                  transition-all shadow-lg hover:shadow-xl flex items-center justify-center"
              >
                {loading ? (
                  <>
                    <div className="spinner mr-3"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <FiCheckCircle className="mr-2" />
                    Detect Vehicles
                  </>
                )}
              </button>

              <button
                onClick={handleReset}
                className="bg-red-500 text-white py-4 px-6 rounded-xl font-semibold 
                  hover:bg-red-600 transition-all shadow-lg hover:shadow-xl flex items-center"
              >
                <FiTrash2 className="mr-2" />
                Reset
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="mt-6 bg-red-500 bg-opacity-20 border border-red-400 text-white p-4 rounded-xl flex items-start">
                <FiAlertCircle className="mr-3 mt-1 flex-shrink-0" />
                <p>{error}</p>
              </div>
            )}
          </div>

          {/* Right Panel - Results */}
          <div className="glass-effect rounded-2xl p-8 shadow-2xl fade-in">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <FiImage className="mr-3" /> Detection Results
            </h2>

            {!results ? (
              <div className="text-center py-20">
                <FiImage className="text-6xl text-white opacity-30 mx-auto mb-4" />
                <p className="text-white opacity-70 text-lg">
                  Upload an image and click "Detect Vehicles" to see results
                </p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Result Image */}
                <div className="bg-white bg-opacity-10 rounded-xl p-4">
                  <img
                    src={`${API_URL}${results.output_url}`}
                    alt="Detection Result"
                    className="w-full rounded-lg shadow-lg"
                  />
                  <button
                    onClick={downloadResult}
                    className="w-full mt-4 bg-green-500 text-white py-3 px-6 rounded-lg font-semibold 
                      hover:bg-green-600 transition-all flex items-center justify-center"
                  >
                    <FiDownload className="mr-2" />
                    Download Result
                  </button>
                </div>

                {/* Summary */}
                <div className="bg-white bg-opacity-10 rounded-xl p-6">
                  <h3 className="text-xl font-bold text-white mb-4">Summary</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold text-blue-300">
                        {results.summary.total_vehicles}
                      </div>
                      <div className="text-white opacity-70 text-sm mt-1">Vehicles</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-green-300">
                        {results.summary.total_plates}
                      </div>
                      <div className="text-white opacity-70 text-sm mt-1">Plates</div>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold text-purple-300">
                        {results.summary.plates_with_text}
                      </div>
                      <div className="text-white opacity-70 text-sm mt-1">Recognized</div>
                    </div>
                  </div>
                </div>

                {/* Detected Plates */}
                {results.plates && results.plates.length > 0 && (
                  <div className="bg-white bg-opacity-10 rounded-xl p-6">
                    <h3 className="text-xl font-bold text-white mb-4">Detected Number Plates</h3>
                    <div className="space-y-3">
                      {results.plates.map((plate, index) => (
                        <div
                          key={index}
                          className="bg-white bg-opacity-10 rounded-lg p-4 flex justify-between items-center"
                        >
                          <div>
                            <div className="text-white font-semibold">
                              Vehicle #{plate.vehicle_index + 1}
                            </div>
                            <div className="text-white text-sm opacity-70">
                              Confidence: {(plate.confidence * 100).toFixed(1)}%
                            </div>
                            {plate.language && (
                              <div className="text-white text-xs mt-1">
                                <span className={`px-2 py-1 rounded ${
                                  plate.language === 'bangla' 
                                    ? 'bg-purple-500 bg-opacity-50' 
                                    : 'bg-blue-500 bg-opacity-50'
                                }`}>
                                  {plate.language === 'bangla' ? '🇧🇩 Bangla' : '🇬🇧 English'}
                                </span>
                              </div>
                            )}
                          </div>
                          <div className="text-right">
                            {plate.text ? (
                              <div>
                                <div className={`text-2xl font-bold font-mono ${
                                  plate.language === 'bangla' ? 'text-purple-300' : 'text-green-300'
                                }`}>
                                  {plate.text}
                                </div>
                                {plate.raw_text && plate.raw_text !== plate.text && (
                                  <div className="text-xs text-white opacity-50 mt-1">
                                    Raw: {plate.raw_text}
                                  </div>
                                )}
                              </div>
                            ) : (
                              <div className="text-sm text-yellow-300">
                                No text detected
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Vehicle Details */}
                {results.vehicles && results.vehicles.length > 0 && (
                  <div className="bg-white bg-opacity-10 rounded-xl p-6">
                    <h3 className="text-xl font-bold text-white mb-4">Vehicle Details</h3>
                    <div className="space-y-2">
                      {results.vehicles.map((vehicle, index) => (
                        <div
                          key={index}
                          className="bg-white bg-opacity-10 rounded-lg p-3 flex justify-between items-center"
                        >
                          <div className="text-white">
                            <span className="font-semibold">Vehicle #{index + 1}:</span>{' '}
                            <span className="capitalize">{vehicle.class}</span>
                          </div>
                          <div className="text-green-300 font-semibold">
                            {(vehicle.confidence * 100).toFixed(1)}%
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12">
          <p className="text-white opacity-70">
            Powered by YOLOv8 & EasyOCR | AI Vehicle Detection System
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
