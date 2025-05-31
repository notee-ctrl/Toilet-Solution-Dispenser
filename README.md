# Toilet-Solution-Dispenser
This project is a GUI-based system that controls a motor (dispenser) for a custom time. It uses a Raspberry Pi, GPIO, and Tkinter for the interface.

## Features
- Adjustable motor duration (1–30 seconds)
- Start/Stop control
- Live status + progress bar

## Hardware
- Raspberry Pi
- Motor or pump
- Jumper wires
- External power (if motor requires more current)

## How to Run
1. Connect motor to GPIO 4 via relay/transistor
2. Run: `python3 smart_dispenser.py`
3. Use the GUI to control the motor
