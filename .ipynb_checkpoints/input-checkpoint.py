import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
import os

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

def main():
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

    # Start the GUI loop
    root.mainloop()

if __name__ == "__main__":
    main()