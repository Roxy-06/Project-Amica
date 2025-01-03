import tkinter as tk
from PIL import Image, ImageTk

def on_button_click(event):
    print("Button clicked!")

# Create the main window
root = tk.Tk()
root.title("Circular Button with Mic")
root.geometry("200x200")  # Set the window size to 200x200 pixels

# Create a Canvas widget
canvas = tk.Canvas(root, width=200, height=200, bg="black", highlightthickness=0)
canvas.pack()

# Draw a circle (as a button) with a solid color (white)
x, y, r = 100, 100, 40  # Center (x, y) and radius r
canvas.create_oval(x - r, y - r, x + r, y + r, fill="white", outline="black", width=2)  # Solid color

# Load the microphone image
mic_image = Image.open("m.png")  # Make sure to provide the correct path to your mic image
mic_image = mic_image.resize((80, 80), Image.LANCZOS)  # Resize the image to fit within the circle
mic_photo = ImageTk.PhotoImage(mic_image)

# Add the microphone image on top of the circle
canvas.create_image(x, y, image=mic_photo)

# Bind the click event
canvas.bind("<Button-1>", on_button_click)

# Run the application
root.mainloop()