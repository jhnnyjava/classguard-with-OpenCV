# ClassGuard: AI-Powered Attendance and Concentration Monitoring System

Enhanced Classroom Engagement for Sustainable Education (SDG 4)

**Event:** SES World Engineering Day 2026 | **Date:** March 6, 2026 | **Venue:** IPIC Center, JKUAT  
**Team:** John Khaemba, Just Sumba, Gigito

## Features
- Automatic attendance using facial recognition  
- Real-time concentration monitoring (0-1 score)  
- Detects **Attentive 👀** or **Sleeping 😴**  
- Counts total people in classroom  
- Logs everything to CSV (ready for Excel)  
- Low-cost Raspberry Pi 4 + Pi Camera v2

## Hardware Required
- Raspberry Pi 4 (4GB)
- Pi Camera v2 (or USB webcam)
- 5V power supply

## Installation (run once)

```bash
cd ~
git clone https://github.com/yourusername/ClassGuard.git
cd ClassGuard

sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-pil

pip3 install pandas opencv-contrib-python-headless --break-system-packages
```
