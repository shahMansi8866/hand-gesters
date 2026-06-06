# ✋ Hand Gesture Mouse Control

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-green)](https://mediapipe.dev/)
[![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-0.9.54-orange)](https://pyautogui.readthedocs.io/)

Control your computer mouse using real-time hand gestures from your webcam. No physical mouse or touchpad needed – just wave your fingers!


## 🚀 Features

| Gesture | Action |
|---------|--------|
| ☝️ Index finger only | Move mouse cursor (absolute mapping) |
| ✌️ Two fingers (index + middle) | Left click |
| 🤏 Pinch (thumb + index close together) | Drag & drop (mouse down / up) |
| 🖖 Three fingers | Scroll down (continuous) |
| 🖐️ Four fingers + move hand up/down | Vertical scroll (move hand up → scroll up, down → scroll down) |

All gestures work with real-time visual feedback – hand landmarks and skeleton are drawn on the camera feed.

---

## 📦 Requirements

- Python 3.7 or higher
- A working webcam
- Operating system: Windows / Linux / macOS (PyAutoGUI works on all)

### Python Libraries

- opencv-python – video capture and image processing
- mediapipe – hand landmark detection (21 points)
- pyautogui – OS mouse control
- math – distance calculations (built-in)

---

## 🔧 Installation

### 1. Clone the repository

git clone https://github.com/shahMansi8866/hand-gesters.git
cd hand-gesters

### 2. (Recommended) Create a virtual environment

Windows:
python -m venv venv
venv\Scripts\activate

macOS / Linux:
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

If you don't have a requirements.txt file yet, create one with:

opencv-python>=4.5
mediapipe>=0.10.9
pyautogui>=0.9.54

Then run the install command again.

---

## 🎮 Usage

Run the main script:

python main.py

A window titled "Hand Gesture Mouse Control" will open showing your webcam feed with hand landmarks overlaid.

### How to control

- Move cursor – raise only your index finger, keep others folded. Move your hand around.
- Click – raise index and middle fingers together.
- Drag – bring thumb and index finger tips very close (pinch), then move your hand. Release pinch to drop.
- Scroll down – raise three fingers.
- Vertical scroll – raise four fingers, then move your whole hand up (scroll up) or down (scroll down).

### Exiting the program

- Press the ESC key on your keyboard, or
- Move the mouse cursor to any corner of the screen (PyAutoGUI failsafe).

---

## 📁 Project Structure

hand-gesters/
├── main.py                 # Main application code
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Ignored files (venv, cache, etc.)
└── demo.gif                # Optional: short demo animation

---

## 🧠 How It Works

1. OpenCV captures each frame from the webcam and flips it horizontally (mirror view).
2. The frame is converted from BGR to RGB and passed to MediaPipe Hands.
3. MediaPipe returns 21 landmarks (x, y, z coordinates) for each detected hand.
4. The script calculates:
   - Which fingers are raised (using y-coordinate comparison between fingertip and PIP joint).
   - Distance between thumb tip and index tip (for pinch detection).
   - Vertical palm movement (for 4-finger scroll).
5. Based on finger count and pinch status, the state machine decides the action.
6. PyAutoGUI performs the corresponding mouse operation (move, click, drag, scroll).
7. The processed frame is displayed with drawn landmarks and on-screen mode text.

### Smoothing

Cursor movement uses exponential smoothing to reduce jitter:
current = previous + (raw - previous) / smooth_factor

### Cooldowns

- Click action has a 12-frame cooldown to avoid accidental double clicks.
- After releasing a drag, a short 10-frame cooldown prevents immediate re-drag.

---

## ⚠️ Troubleshooting

| Problem | Likely solution |
|---------|------------------|
| Camera not opening | Check if another app is using the camera. Change cv2.VideoCapture(0) to 1 or 2 if you have multiple cameras. |
| Hand not detected | Ensure good lighting. Keep your hand fully inside the frame. Background should not be too cluttered. |
| Cursor jumps erratically | Reduce the smooth value (e.g., 4) or try to keep hand movements slower. |
| PyAutoGUI permission errors (macOS) | Go to System Settings → Privacy & Security → Accessibility and allow your terminal/IDE to control the computer. |
| Deprecation warnings from MediaPipe | These are harmless. You can ignore them or add warnings.filterwarnings("ignore") at the top of main.py. |

---

## 🧪 Future Improvements (Ideas)

- [ ] Two-hand support (left hand for modifiers / shortcuts)
- [ ] Volume control via thumb-index distance
- [ ] On-screen gesture guide overlay
- [ ] Configurable thresholds (pinch distance, smoothing) via trackbars
- [ ] Record and replay gesture macros
- [ ] Multi-screen support

Pull requests and new ideas are welcome!

---

## 📄 License

This project is licensed under the MIT License – you are free to use, modify, and distribute it.

---

## 🙏 Acknowledgements

- Google MediaPipe for the fast, accurate hand tracking model.
- PyAutoGUI for cross-platform mouse control.
- OpenCV for video capture and display.

---

## 📬 Connect

Author: Mansi Shah
GitHub: @shahMansi8866
LinkedIn: [(https://www.linkedin.com/in/mansi-shah-8b0162296/)]

If you like this project, please ⭐ star the repo and share it!
