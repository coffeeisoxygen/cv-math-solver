# Math Solver Computer Vision Project

This project uses computer vision to detect hand gestures and enable drawing on screen. It's designed to be integrated with AI for math problem solving in the future.

## Features

- Hand gesture detection
- Drawing with index finger
- Gesture controls:
  - Index finger only: Start drawing
  - Index + middle fingers: Pause drawing
  - Index + middle + ring fingers: Stop and clear drawing

## File Structure

- `main.py` - Entry point of the application
- `hand_detector.py` - Hand detection functionality
- `drawing.py` - Drawing management and canvas handling
- `utils.py` - Utility functions like camera setup

## Requirements

- Python 3.7+
- OpenCV
- CVZone

## Future Integration

This project is designed to be integrated with AI models that can:
- Recognize handwritten mathematical equations
- Solve these equations in real-time
- Display the solutions on screen
