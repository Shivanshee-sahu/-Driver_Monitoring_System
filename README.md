# 🚗 Real-Time Driver Monitoring System  
### Embedded Software Simulation + Computer Vision

A real-time driver monitoring system that detects drowsiness using computer vision techniques and communicates alerts via a UART-style serial interface.

---

## 📌 Features

- 👁️ Eye closure detection using **Eye Aspect Ratio (EAR)**
- 😮 Yawning detection using **Mouth Aspect Ratio (MAR)**
- ⏱️ Temporal filtering to distinguish **blinking vs drowsiness**
- 🔌 UART-style serial communication (`0xFF` / `0x00`)
- ⚡ Real-time processing with FPS monitoring
- 🧠 Edge-triggered signaling to avoid redundant transmission

---

## 🧠 System Architecture
    +----------------------+
    |   Webcam (Input)     |
    +----------+-----------+
               |
               v
    +----------------------+
    |  Vision Processing   |
    | (OpenCV + Face Rec)  |
    +----------+-----------+
               |
               v
    +----------------------+
    | Feature Extraction   |
    |  EAR / MAR Compute   |
    +----------+-----------+
               |
               v
    +----------------------+
    | Decision Engine      |
    | Temporal Filtering   |
    | (Counter + Score)    |
    +----------+-----------+
               |
               v
    +----------------------+
    | Serial Interface     |
    | (PySerial - UART)    |
    +----------+-----------+
               |
               v
    +----------------------+
    | Embedded Controller  |
    | (Virtual / Simulated)|
    +----------------------+

---

## ⚙️ How It Works

### 1. Face & Landmark Detection
- Uses `face_recognition` to detect face and extract facial landmarks.

### 2. Feature Extraction
- **EAR (Eye Aspect Ratio)** → detects eye closure  
- **MAR (Mouth Aspect Ratio)** → detects yawning  

### 3. Temporal Filtering
- Uses:
  - **Frame-based counter** → detects sustained eye closure  
  - **Cumulative score** → tracks fatigue over time  

👉 Helps distinguish:
- Blink ❌  
- Drowsiness ✅  

---

### 4. Decision Logic

- If eyes closed for multiple frames OR fatigue score high:
  → **DROWSY state**

---

### 5. Serial Communication

- Sends:
  - `0xFF` → Drowsy  
  - `0x00` → Awake  

- Uses:
  - **UART-style protocol (9600 baud)**
  - **Edge-triggered signaling** (only sends on state change)

---

## 🔌 Virtual Hardware Setup

Since no physical hardware is used:

- Use **VSPE / com0com** to create virtual ports:
  - `COM3 ↔ COM4`

- Python sends data via COM3  
- Another program reads from COM4  

---

## 📊 Performance

- Real-time processing on webcam input  
- Stable FPS achieved via:
  - Frame resizing  
  - Controlled processing  

---

## 🛠️ Installation

```bash
pip install opencv-python face_recognition numpy pyserial

```

---

## 🛠 Embedded Systems Considerations
### Communication Protocol:
 - Lightweight 1-byte signaling (0xFF/0x00) for efficient embedded communication
### Temporal Debounce:
 - Filters noise from natural blinking using time-based logic
### Latency Awareness:
 - Designed for real-time responsiveness in safety-critical scenarios
### Edge-Triggered Signaling:
 - Prevents redundant serial transmission

---

## 🚀 Future Improvements
- Replace face_recognition with MediaPipe (faster)
- Add multi-threading
- Implement PERCLOS-based detection
- Integrate YOLO for phone/distraction detection
- Deploy on Raspberry Pi / Embedded Linux
  
