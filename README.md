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
