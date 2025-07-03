import threading
import time
from io import BytesIO
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyautogui
import pygetwindow as gw
import pytesseract
import pyttsx3


def list_windows():
    titles = [w.title for w in gw.getAllWindows() if w.title]
    return titles


def capture_window(title):
    win = gw.getWindowsWithTitle(title)[0]
    bbox = win.left, win.top, win.width, win.height
    return pyautogui.screenshot(region=bbox)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack OCR Helper")
        self.geometry("800x600")
        self.start_x = self.start_y = 0
        self.rect = None
        self.selected_image = None
        self.screenshot = None
        self.engine = pyttsx3.init()
        self.create_widgets()
        self.refresh_windows()

    def create_widgets(self):
        frame = ttk.Frame(self)
        frame.pack(pady=10)
        ttk.Label(frame, text="Select game window:").pack(side=tk.LEFT)
        self.win_var = tk.StringVar()
        self.win_combo = ttk.Combobox(frame, textvariable=self.win_var)
        self.win_combo.pack(side=tk.LEFT)
        ttk.Button(frame, text="Capture", command=self.capture).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Read", command=self.read_selection).pack(side=tk.LEFT)
        self.canvas = tk.Canvas(self, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

    def refresh_windows(self):
        titles = list_windows()
        self.win_combo['values'] = titles
        if titles:
            self.win_var.set(titles[0])

    def capture(self):
        title = self.win_var.get()
        if title:
            self.screenshot = capture_window(title)
        else:
            self.screenshot = pyautogui.screenshot()
        img = self.screenshot.resize((800, int(800 * self.screenshot.height / self.screenshot.width)))
        self.selected_image = img
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.config(width=self.tk_img.width(), height=self.tk_img.height())
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

    def on_mouse_down(self, event):
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_up(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def read_selection(self):
        if not self.screenshot or not self.rect:
            return
        coords = self.canvas.coords(self.rect)
        scale_x = self.screenshot.width / self.tk_img.width()
        scale_y = self.screenshot.height / self.tk_img.height()
        x1, y1, x2, y2 = [int(c * scale_x if i % 2 == 0 else c * scale_y) for i, c in enumerate(coords)]
        cropped = self.screenshot.crop((x1, y1, x2, y2))
        text = pytesseract.image_to_string(cropped)
        self.engine.say(text)
        self.engine.runAndWait()
        tk.messagebox.showinfo("OCR Result", text)


if __name__ == "__main__":
    App().mainloop()
