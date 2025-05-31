import RPi.GPIO as GPIO
import time
import tkinter as tk
from tkinter import ttk
import threading

MOTOR_PIN = 4
motor_running = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_PIN, GPIO.OUT)

def run_motor(duration):
    global motor_running
    if not motor_running:
        motor_running = True
        status_label.config(text="Status: Running", foreground="green")
        button.config(state="disabled")
        duration_scale.config(state="disabled")
        
        # Update progress bar
        progress_bar["maximum"] = duration
        for i in range(duration + 1):
            if not motor_running:  # Check if we should stop
                break
            progress_bar["value"] = i
            root.update()
            time.sleep(1)
            
        GPIO.output(MOTOR_PIN, GPIO.LOW)
        status_label.config(text="Status: Stopped", foreground="red")
        button.config(state="normal")
        duration_scale.config(state="normal")
        progress_bar["value"] = 0
        motor_running = False

def button_callback():
    duration = int(duration_scale.get())
    GPIO.output(MOTOR_PIN, GPIO.HIGH)
    # Run motor in a separate thread to keep UI responsive
    thread = threading.Thread(target=run_motor, args=(duration,))
    thread.daemon = True
    thread.start()

def stop_motor():
    global motor_running
    motor_running = False
    GPIO.output(MOTOR_PIN, GPIO.LOW)
    status_label.config(text="Status: Stopped", foreground="red")
    button.config(state="normal")
    duration_scale.config(state="normal")
    progress_bar["value"] = 0

# Create the main window
root = tk.Tk()
root.title("Motor Control Interface")
root.geometry("400x500")
root.configure(padx=20, pady=20)

# Create main frame
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Title
title_label = ttk.Label(main_frame, text="Motor Control Panel", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Status indicator
status_label = ttk.Label(main_frame, text="Status: Stopped", foreground="red")
status_label.pack(pady=10)

# Duration control
duration_frame = ttk.LabelFrame(main_frame, text="Motor Duration (seconds)")
duration_frame.pack(fill="x", pady=10)

duration_value_label = ttk.Label(duration_frame, text="10 seconds")  # Default value
duration_value_label.pack(pady=(0, 5))

def update_duration_label(event):
    duration_value_label.config(text=f"{int(duration_scale.get())} seconds")

duration_scale = ttk.Scale(duration_frame, from_=1, to=30, orient="horizontal")
duration_scale.set(10)  # Default value
duration_scale.pack(fill="x", padx=10, pady=5)
duration_scale.bind("<Motion>", update_duration_label)  # Update while dragging
duration_scale.bind("<ButtonRelease-1>", update_duration_label)  # Update after click

# Progress bar
progress_frame = ttk.LabelFrame(main_frame, text="Progress")
progress_frame.pack(fill="x", pady=10)
progress_bar = ttk.Progressbar(progress_frame, mode="determinate")
progress_bar.pack(fill="x", padx=10, pady=5)

# Button frame
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=20)

# Start button
button = ttk.Button(
    button_frame,
    text="Start Motor",
    command=button_callback,
    style="Accent.TButton"
)
button.pack(side="left", padx=5)

# Stop button
stop_button = ttk.Button(
    button_frame,
    text="Stop Motor",
    command=stop_motor,
    style="Stop.TButton"
)
stop_button.pack(side="left", padx=5)

# Create custom styles
style = ttk.Style()
style.configure("Accent.TButton", background="green")
style.configure("Stop.TButton", background="red")

# Start the application
root.mainloop()

# Cleanup GPIO on exit
GPIO.cleanup() 



