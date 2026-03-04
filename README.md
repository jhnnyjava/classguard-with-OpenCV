# ClassGuard: AI-Powered Attendance and Concentration Monitoring System

Enhanced Classroom Engagement for Sustainable Education (SDG 4)

**Event:** SES World Engineering Day 2026 | **Date:** March 6, 2026 | **Venue:** IPIC Center, JKUAT  
**Team:** John Khaemba, Just Sumba, Gigito

## Features
- ✅ Automatic attendance using facial recognition (LBPH algorithm)
- 📊 Real-time concentration monitoring (0-1 score)
- 😴 Detects **Attentive 👀** or **Sleeping 😴** status
- 👥 Counts total people in classroom
- 📁 Logs everything to CSV (ready for Excel/data analysis)
- 💰 Low-cost solution: Raspberry Pi 4 + Pi Camera v2

## Hardware Required
- Raspberry Pi 4 (4GB recommended)
- Pi Camera v2 (or USB webcam)
- 5V 3A power supply
- MicroSD card (16GB+)
- Optional: HDMI monitor for live preview

## Installation (run once on Raspberry Pi)

### Step 1: Clone the repository
```bash
cd ~
git clone https://github.com/jhnnyjava/classguard-with-OpenCV.git
cd classguard-with-OpenCV
```

### Step 2: Install system dependencies
```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-pil
```

### Step 3: Install Python packages
```bash
pip3 install pandas opencv-contrib-python-headless --break-system-packages
```

### Step 4: Create necessary folders
```bash
mkdir -p dataset logs trainer
```

## How to Use ClassGuard

### 1. Enroll Students (First Time Setup)

Run the enrollment script for each student:
```bash
python3 enrollment.py
```

**What happens:**
- You'll be prompted to enter a student name (e.g., `John_Khaemba`)
- The student should look at the camera
- The system automatically captures 30 photos of their face
- Photos are saved in `dataset/[student_name]/`

**Repeat this for every student** (3-5 minimum for demo, 30+ for real classroom).

### 2. Train the Recognition Model

After enrolling all students, train the model:
```bash
python3 train.py
```

**What happens:**
- Processes all enrolled faces from `dataset/` folder
- Trains LBPH face recognizer
- Saves model to `trainer/trainer.yml`
- Saves name mapping to `trainer/names.npy`

You'll see: `✅ Model trained successfully!`

### 3. Run the Monitoring System

Start the live monitoring:
```bash
python3 classguard_main.py
```

**What happens:**
- Camera starts capturing live video
- Detects faces in real-time
- Recognizes enrolled students by name
- Tracks eye state (open = Attentive, closed = Sleeping)
- Every 8 seconds, displays:
  - 👥 Total people in classroom
  - ✅ List of recognized students
  - 😴/👀 Attentive or Sleeping status for each student
  - 📊 Class average attention score
- Logs all data to `logs/attendance.csv`

**To stop:** Press `Ctrl + C`

### 4. View the Attendance Logs

The CSV file contains timestamped records:
```bash
cat logs/attendance.csv
```

**Sample output:**
```
timestamp,student_name,attendance,concentration_score,status
2026-03-04 21:35:40,John_Khaemba,Present,0.92,Attentive 👀
2026-03-04 21:35:48,Just_Sumba,Present,0.55,Attentive 👀
2026-03-04 21:35:56,Gigito,Present,0.15,Sleeping 😴
```

You can open this file in Excel, Google Sheets, or any data analysis tool.

## For Presenters: Quick Reference

If your friend is presenting and needs to train the model from scratch:

1. **SSH into the Pi:**
   ```bash
   ssh pi@raspberrypi.local
   # or use the Pi's IP: ssh pi@192.168.1.xxx
   ```

2. **Navigate to project:**
   ```bash
   cd ~/classguard-with-OpenCV
   ```

3. **Enroll 3-5 people** (team members or audience volunteers):
   ```bash
   python3 enrollment.py
   # Enter name → look at camera → wait ~5 seconds
   # Repeat for each person
   ```

4. **Train the model:**
   ```bash
   python3 train.py
   ```

5. **Run the demo:**
   ```bash
   python3 classguard_main.py
   ```

6. **Show the results:**
   - Point to the console output (names, people count, status)
   - Show CSV file: `cat logs/attendance.csv`
   - Optional: Connect HDMI monitor to show live camera feed

## System Architecture

### Files in This Repository

| File | Purpose |
|------|---------|
| `enrollment.py` | Captures student face images for training |
| `train.py` | Trains LBPH face recognition model |
| `classguard_main.py` | Main monitoring system (attendance + concentration) |
| `dataset/` | Stores enrolled student photos (not in repo) |
| `trainer/` | Stores trained model files (not in repo) |
| `logs/` | CSV attendance records (not in repo) |
| `README.md` | This documentation |

### How It Works

1. **Face Detection:** Uses OpenCV Haar Cascade (haarcascade_frontalface_default.xml)
2. **Face Recognition:** LBPH (Local Binary Pattern Histogram) algorithm
3. **Eye Tracking:** Haar Cascade eye detector (haarcascade_eye.xml)
4. **Concentration Score:**
   - 2 eyes detected → 0.95 (Attentive)
   - 1 eye detected → 0.55 (Partially attentive)
   - 0 eyes detected → 0.15 (Possibly sleeping)
5. **Sleeping Detection:** If score < 0.3 for 5 consecutive frames → "Sleeping 😴"

## Viewing Live Camera Feed

### Option 1: Connect Monitor (Recommended for Presentation)
1. Connect HDMI monitor + keyboard/mouse to Raspberry Pi
2. Run directly on Pi (not via SSH)
3. Live window will show camera feed with bounding boxes and names

### Option 2: SSH with X11 Forwarding
```bash
ssh -X pi@raspberrypi.local
cd ~/classguard-with-OpenCV
python3 classguard_main.py
```

## Troubleshooting

### "No module named 'cv2'"
```bash
sudo apt install python3-opencv
```

### "No module named 'picamera2'"
```bash
sudo apt install python3-picamera2
```

### Camera not working
Check cable connection and run:
```bash
rpicam-hello
```

### "Unknown" for all students
- Confidence threshold too strict
- Re-enroll with better lighting
- Ensure face is looking straight at camera during enrollment

### "externally-managed-environment" error
Add `--break-system-packages` flag:
```bash
pip3 install [package] --break-system-packages
```

## Future Enhancements
- Web dashboard for remote monitoring
- Email/SMS alerts for low attendance
- Integration with school management systems
- Deep learning models (when Pi 5 becomes more available)
- Multi-camera support for large classrooms

## Technical Specifications
- **Language:** Python 3.11+
- **Computer Vision:** OpenCV 4.10+
- **Camera Interface:** Picamera2
- **Recognition:** LBPH (opencv-contrib)
- **Platform:** Raspberry Pi OS (Bookworm/Trixie)
- **Hardware:** Raspberry Pi 4, Pi Camera v2 (IMX219 sensor)

## Contributing to Education (SDG 4)
ClassGuard supports UN Sustainable Development Goal 4: Quality Education by:
- Automating attendance (saves 10+ minutes per class)
- Providing data-driven insights on student engagement
- Identifying students who need support
- Low-cost solution accessible to under-resourced schools

## License
MIT License - Free for educational use

## Contact
**John Khaemba** | johnkhaemba710@gmail.com  
**Team:** Just Sumba, Gigito  
**Institution:** JKUAT  
**Event:** SES World Engineering Day 2026

---

🔥 **Ready to revolutionize classroom engagement!** 🔥
