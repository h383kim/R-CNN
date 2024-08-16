import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import os
import cv2
import sys
import matplotlib.pyplot as plt
import matplotlib

# Ensure Matplotlib is set up to work well with Tkinter
matplotlib.use('TkAgg')

def ss_config(ss, img, mode):
    ss.setBaseImage(img)

    if mode == 's':
        ss.switchToSingleStrategy()
    elif mode == 'f':
        ss.switchToSelectiveSearchFast()
    elif mode == 'q':
        ss.switchToSelectiveSearchQuality()
    else:
        print("Re-enter the mode. s or f or q")
        sys.exit(1)


def selective_search(img_path, mode='q'):
    # Initiate Selective Search
    ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
    # Read image in color
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # Configure the mode and image
    ss_config(ss, img, mode)

    # Process Selective-Search
    bboxes = ss.process() # bboxes: listof [x, y, w, h]
    bboxes[:, 2] += bboxes[:, 0] # bboxes -> listof [x, y, x + w, h]
    bboxes[:, 3] += bboxes[:, 1] # bboxes -> listof [x, y, x + w, h + y]

    return bboxes

def open_image(file_path):
    try:
        # Open the image file
        image = Image.open(file_path)
        image.show()  # Show the image using the default image viewer
    except Exception as e:
        print(f"Error opening image: {e}")

def drop(event):
    file_path = event.data
    # Check if the dropped file is an image
    if file_path.lower().endswith(('.PNG', '.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        print(file_path)
        bboxes = selective_search(file_path)
        img = cv2.imread(file_path, cv2.IMREAD_COLOR)
        # Drawing the image and bounding boxes
        for bbox in bboxes[:50]:
            x1, y1, x2, y2 = bbox[0], bbox[1], bbox[2], bbox[3]
            img = cv2.rectangle(img, [x1, y1], [x2, y2], color=(0, 255, 0), thickness=2)
        # BGR -> RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Plot
        plt.figure(figsize=(10, 10))
        plt.imshow(img_rgb)
        plt.axis('off')
        plt.show()
    else:
        print("Please drop an image file.")


def on_closing():
    print("Closing the program...")
    plt.close('all')  # Close all matplotlib figures
    root.destroy()  # Properly destroy the Tkinter window and terminate the loop


def main():
    global root
    # Create the main window
    root = TkinterDnD.Tk()
    root.title("Drag and Drop Image Reader")
    root.geometry("400x200")

    # Label for instruction
    label = tk.Label(root, text="Drag and drop an image file here", font=("Arial", 14))
    label.pack(pady=50)

    # Enable drop functionality
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', drop)

    # Handle window close event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()