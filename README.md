# 🖐️ Gesture-Controlled Temple Run Game Player

Control Temple Run (or any similar web-based game like the one on [Poki.com](https://poki.com)) using your **hand gestures** and a **webcam**, with no additional hardware required.

This project uses **Python**, **OpenCV**, **cvzone**, **MediaPipe**, and **Pynput** to detect specific hand gestures and map them to keyboard keys that work seamlessly with games like Temple Run.

---

## ✨ Features

- ✌️ Peace Sign → Jump (`↑ Up arrow`)
- ☝️ Index Finger Up → Slide (`↓ Down arrow`)
- ✋ Left Palm Open → Turn Left (`← Left arrow`)
- 🤚 Right Palm Open → Turn Right (`→ Right arrow`)
- 👌 OK Sign → Mouse Click (Optional)
- ✊ Both Fists → No action (pause)

Works in **real-time** using your webcam.

---

## 🛠️ Installation

Make sure Python 3.7 to 3.10 is installed.

Install required packages:-
pip install opencv-python cvzone mediapipe pynput

### 1. Clone this Repository

```bash
git clone https://github.com/Saha-Manav/Gesture-Controlled-Temple-Run-Game-Player.git
cd Gesture-Controlled-Temple-Run-Game-Player
