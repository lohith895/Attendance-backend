# 🚀 AI Face Attendance Backend API

An AI-powered backend service for the Automated Attendance Management System built with **FastAPI**, **InsightFace**, **YOLOv8**, and **Supabase**. This service handles face detection, feature extraction, liveness anti-spoofing checks, identity matching, student face embedding training, and WhatsApp notification alerts for absences.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Architecture](#-project-architecture)
- [Directory Structure](#-directory-structure)
- [Environment Variables](#-environment-variables)
- [Installation & Setup](#-installation--setup)
- [Running the Server](#-running-the-server)
- [API Documentation](#-api-documentation)
- [Anti-Spoofing & Liveness Mechanism](#-anti-spoofing--liveness-mechanism)

---

## ✨ Features

- 👤 **Single & Bulk Face Training**: Extracts facial embeddings using InsightFace (`buffalo_l`) and averages them across samples to store per student in Supabase.
- 🎯 **Face Recognition & Matching**: Computes cosine similarity between detected input faces and enrolled student face embeddings.
- 🛡️ **Liveness Detection & Anti-Spoofing**: Filters out photo/screen spoof attempts using Laplacian variance quality analysis and specular glare detection thresholds.
- 🔍 **YOLOv8 Face Detection**: Uses `yolov8n-face.pt` as a lightweight gatekeeper for single-face enrollment verification.
- 🔐 **Supabase JWT Authentication**: Validates requests via Supabase Auth Bearer tokens.
- 📱 **WhatsApp Alert Integration**: Sends automated absence notifications to parents via Twilio WhatsApp API (with automatic fallback to simulated logging).

---

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) / [Gunicorn](https://gunicorn.org/)
- **Computer Vision & AI**:
  - [InsightFace](https://github.com/deepinsight/insightface) (`buffalo_l` model)
  - [Ultralytics YOLOv8](https://docs.ultralytics.com/) (`yolov8n-face.pt`)
  - [OpenCV](https://opencv.org/) (`opencv-python-headless`)
  - [Scikit-Learn](https://scikit-learn.org/) (Cosine Similarity calculation)
- **Database & Auth**: [Supabase Python SDK](https://supabase.com/docs/reference/python/initializing)
- **Messaging**: [Twilio REST API](https://www.twilio.com/docs/whatsapp)
- **Environment Management**: `python-dotenv`, `certifi`

---

## 📁 Directory Structure

```
Attendance_backend/
├── app/
│   ├── ai/
│   │   ├── detector.py       # YOLOv8 face detection gatekeeper
│   │   ├── quality.py        # Laplacian variance & glare liveness checks
│   │   └── recognizer.py     # InsightFace embedding generator & face analysis
│   ├── routes/
│   │   ├── health.py         # Health check endpoint
│   │   ├── model.py          # Section model status & manual training endpoints
│   │   ├── recognition.py   # Main face recognition & WhatsApp alert endpoints
│   │   └── training.py      # Face enrollment (single & bulk training) endpoints
│   ├── utils/
│   │   ├── image.py          # Base64 image decode helper
│   │   └── sms.py            # Twilio WhatsApp messaging & simulation logger
│   ├── auth.py               # Supabase token verification middleware
│   ├── config.py             # Environment configuration variables
│   ├── database.py           # Supabase client instantiation
│   └── main.py               # FastAPI application initialization & CORS config
├── .env                      # Environment configuration file (secrets)
├── package.json              # Supabase JS dependency definitions
├── requirements.txt          # Python dependency list
├── yolov8n-face.pt           # Pre-trained YOLOv8 face detection weights
└── README.md                 # Project documentation
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory (`Attendance_backend/.env`) with the following settings:

```env
# Supabase Configuration
SUPABASE_URL=https://<your-project-id>.supabase.co
SUPABASE_ANON_KEY=<your-supabase-anon-key>
SUPABASE_KEY=<your-supabase-service-role-key>

# Face Matching Threshold (0.0 to 1.0)
FACE_SIMILARITY_THRESHOLD=0.7

# CORS Allowed Origins (comma-separated or * for development)
ALLOWED_ORIGINS=*

# Twilio WhatsApp API Credentials (Optional - Falls back to sms_logs.txt simulation if omitted)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
```

---

## 📥 Installation & Setup

### Prerequisites

- Python 3.9+ installed
- Git installed
- C++ Build Tools (required by InsightFace / ONNX runtime dependencies on Windows)

### Step-by-Step Installation

1. **Clone or Navigate to the Backend Project**:
   ```bash
   cd Attendance_backend
   ```

2. **Create and Activate Virtual Environment**:
   - **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Verify Weight Files**:
   Ensure `yolov8n-face.pt` is present in the `Attendance_backend/` root directory.

---

## 🚀 Running the Server

### Development Mode (with Hot Reloading)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

Using Gunicorn with Uvicorn workers:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

Once running, interactive API docs will be available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 🔌 API Endpoints Summary

### 1. Health Check
- `GET /health`
  - **Response**: `{"status": "ok", "version": "1.0.0"}`

### 2. Face Training & Enrollment
- `POST /api/face-training` (Single Student Training)
  - **Payload**: `{"student_id": "UUID", "images": ["base64_string", ...]}`
  - **Description**: Extracts embeddings for single image face submission and registers face in Supabase.
- `POST /api/face-training/bulk` (Bulk Student Training)
  - **Auth**: `Bearer <token>`
  - **Payload**: `{"students": [...], "images": {"1": "base64_string", ...}}`

### 3. Face Recognition & Attendance
- `POST /api/face-recognition` (Full Frame Recognition)
  - **Auth**: `Bearer <token>`
  - **Payload**: `{"image": "base64_string", "section_id": "UUID"}`
  - **Returns**: Recognized student list with bounding boxes and confidence scores + Spoof/Unrecognized list.
- `POST /api/face-recognition/crops` (Cropped Face Array Recognition)
  - **Auth**: `Bearer <token>`
  - **Payload**: `{"section_id": "UUID", "crops": [{"image": "base64_string", "bounding_box": {...}}]}`

### 4. WhatsApp Absence Alerts
- `POST /api/alerts/whatsapp`
  - **Auth**: `Bearer <token>`
  - **Payload**:
    ```json
    {
      "teacher_phone": "+919999999999",
      "parent_phone": "+918888888888",
      "student_name": "John Doe",
      "subject_name": "Mathematics",
      "subject_code": "MATH101"
    }
    ```
  - **Description**: Sends WhatsApp alert via Twilio or appends record to `sms_logs.txt` if in simulation mode.

### 5. Section Model Status
- `GET /api/model/status/{section_id}`
  - **Auth**: `Bearer <token>`
- `POST /api/model/train`
  - **Auth**: `Bearer <token>`

---

## 🛡️ Anti-Spoofing & Liveness Mechanism

The quality module (`app/ai/quality.py`) inspects cropped facial region pixels using:
1. **Laplacian Blur / Texture Check**: Computes image variance. Values `< 20.0` (blurred photo prints) or `> 5000.0` (digital screen grid / moiré patterns) flag spoof attempts.
2. **Specular Reflection / Glare Detection**: Measures high-intensity pixel ratio (`> 245` grayscale value). If glare percentage exceeds `20%`, it flags a screen reflection or photo print glare spoof attempt.

---

## 📄 License

This project is created for the Automated AI Face Attendance System. All rights reserved.
