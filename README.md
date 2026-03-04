# ClassGuard: AI-Powered Attendance and Concentration Monitoring System

**SES World Engineering Day 2026** | Track: Digital Learning & Academic Innovation (SDG 4)

**Team:** John Khaemba, Just Sumba, Gigito | **Date:** March 6, 2026 | **Venue:** IPIC Center, JKUAT

## Features
- ✅ Automatic attendance with student names (LBPH face recognition)
- 📊 Real-time concentration score (0-1)
- 👀😴 Detects **Attentive** or **Sleeping** status
- 👥 Counts total people in classroom
- 📁 CSV logs (ready for Excel)
- 💰 Low-cost: Raspberry Pi 4 + Pi Camera v2

## Hardware
- Raspberry Pi 4 (4GB)
- Pi Camera v2
- 5V 3A power supply

## Installation (run once)

```bash
cd ~
git clone https://github.com/jhnnyjava/classguard-with-OpenCV.git
cd classguard-with-OpenCV

sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-pil

pip3 install pandas opencv-contrib-python-headless --break-system-packages

mkdir -p dataset logs trainer
```

## How to Run (for presenter)

### 1. Enroll Students
```bash
python3 enrollment.py
```
- Enter student name (e.g., `John_Khaemba`)
- Look at camera for ~5 seconds
- **Repeat for each student** (3-5 minimum for demo)

### 2. Train the Model
```bash
python3 train.py
```
Wait for: `✅ Model trained successfully!`

### 3. Start Monitoring
```bash
python3 classguard_main.py
```

**What you'll see:**
```
📍 2026-03-04 21:35:40
👥 Total People in Classroom: 3
✅ Recognized Students      : ['John_Khaemba', 'Just_Sumba', 'Gigito']
   Status:
      • John_Khaemba → Attentive 👀 (92.0% attention)
      • Just_Sumba → Attentive 👀 (88.0% attention)
      • Gigito → Sleeping 😴 (15.0% attention)
📊 Class Average Attention : 65.0%
```

Stop with `Ctrl+C`

### 4. View Logs
```bash
cat logs/attendance.csv
```

## Files
| File | Purpose |
|------|---------|
| `enrollment.py` | Enroll students (captures 30 face photos) |
| `train.py` | Train face recognition model |
| `classguard_main.py` | Main monitoring system |

## To Show Live Camera Feed (Optional)
- **Option 1:** Connect HDMI monitor to Pi and run directly (not via SSH)
- **Option 2:** Install GUI support: `sudo apt install -y libgtk2.0-dev pkg-config`

## Quick Start for Friend/Presenter

```bash
# SSH into Pi
ssh pi@raspberrypi.local

# Navigate to project
cd ~/classguard-with-OpenCV

# Enroll 3-5 people
python3 enrollment.py  # Repeat for each person

# Train model
python3 train.py

# Run demo
python3 classguard_main.py

# Show CSV after stopping
cat logs/attendance.csv
```

## How It Works
1. **Face Detection:** OpenCV Haar Cascade
2. **Recognition:** LBPH algorithm
3. **Eye Tracking:** Detects open/closed eyes
4. **Concentration Score:**
   - 2 eyes detected → 0.95 (Attentive 👀)
   - 1 eye detected → 0.55
   - 0 eyes detected → 0.15 (Sleeping 😴)

## Troubleshooting

**Camera not working?**
```bash
rpicam-hello  # Test camera
```

**"Unknown" for all students?**
- Re-enroll with better lighting
- Ensure face looks straight at camera

**Module errors?**
```bash
sudo apt install python3-opencv python3-picamera2
pip3 install pandas opencv-contrib-python-headless --break-system-packages
```

## Impact (SDG 4: Quality Education)
- Saves 10+ minutes per class on attendance
- Identifies disengaged students who need support
- Data-driven insights for educators
- Affordable for under-resourced schools

## Contact
**John Khaemba** | johnkhaemba710@gmail.com  
JKUAT | SES World Engineering Day 2026

---

Made with 🔥 for better education
