mport sys
import threading
from io import BytesIO

from PIL import ImageGrab
import pytesseract
import pyttsx3
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import simpledialog

# Ensure Tesseract is installed and pytesseract.pytesseract.tesseract_cmd is set if needed
# Example: pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class ScreenReader:
    def __init__(self):
        self.listening = False
        self.engine = pyttsx3.init()
        self.icon = None

    def start(self):
        # Create tray icon
        image = Image.new('RGB', (64, 64), color=(200, 200, 200))
        d = ImageDraw.Draw(image)
        d.ellipse((16, 16, 48, 48), fill='red')  # record button icon

        menu = (item('Toggle Capture & Read', self.toggle), item('Quit', self.stop))
        self.icon = pystray.Icon('screen_reader', image, 'Screen Reader', menu)
        self.icon.run()

    def toggle(self, icon, item):
        # Pause icon loop and launch capture
        if not self.listening:
            self.listening = True
            threading.Thread(target=self.capture_and_read).start()
        else:
            self.listening = False

    def capture_and_read(self):
        # Freeze screen and allow selection
        root = tk.Tk()
        root.attributes('-alpha', 0.3)
        root.attributes('-fullscreen', True)
        root.config(cursor='crosshair')

        def on_click(event):
            x1, y1 = event.x, event.y
            root.destroy()
            # Ask for second corner
            x2 = simpledialog.askinteger("Selección", "X2:")
            y2 = simpledialog.askinteger("Selección", "Y2:")
            self.process_region((x1, y1, x2, y2))

        root.bind('<Button-1>', on_click)
        root.mainloop()

    def process_region(self, bbox):
        # bbox = (x1, y1, x2, y2)
        img = ImageGrab.grab(bbox)
        text = pytesseract.image_to_string(img, lang='spa')
        if text.strip():
            self.engine.say(text)
            self.engine.runAndWait()

    def stop(self, icon, item):
        self.icon.stop()
        sys.exit()

if __name__ == '__main__':
    app = ScreenReader()
    app.start()
